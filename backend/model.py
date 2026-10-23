import numpy as np
import pandas as pd
import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'models',
    'best_xgb_pipeline.pkl'
)
pipeline_model = joblib.load(MODEL_PATH)
print("Model loaded successfully!")
print(type(pipeline_model))

def predict_patient_admission_risk(patient_dict, threshold=0.25):
    """
    Takes a raw patient dictionary, computes clinical features,
    and returns admission probability and triage recommendations.
    """
    # Convert dictionary to a single-row DataFrame
    df_patient = pd.DataFrame([patient_dict])

    # Derive required physiological features & ratios
    df_patient['pulse_pressure'] = df_patient['sbp'] - df_patient['dbp']
    df_patient['mean_arterial_pressure'] = (2 * df_patient['dbp'] + df_patient['sbp']) / 3

    # Safe Shock Index calculation (handle potential zero/null SBP)
    safe_sbp = df_patient['sbp'].replace(0, np.nan)
    df_patient['shock_index'] = df_patient['hr'] / safe_sbp

    # Safe Modified Shock Index
    safe_map = df_patient['mean_arterial_pressure'].replace(0, np.nan)
    df_patient['modified_shock_index'] = df_patient['hr'] / safe_map

    # Binary physiological flags
    df_patient['is_shock_risk'] = (df_patient['shock_index'] > 0.9).astype(int)
    df_patient['is_tachycardic'] = (df_patient['hr'] > 100).astype(int)
    df_patient['is_hypotensive'] = (df_patient['sbp'] < 90).astype(int)

    # Predict admission probability
    admission_prob = pipeline_model.predict_proba(df_patient)[0, 1]

    # Clinical risk tier and recommendation
    if admission_prob >= 0.50:
        risk_tier = "High Risk (Critical / Severe)"
        action = "Immediate Physician Evaluation & Bed Assignment"
    elif admission_prob >= threshold:
        risk_tier = "Moderate Risk (Observation Required)"
        action = "Hold for Diagnostic Workup / Lab Monitoring"
    else:
        risk_tier = "Low Risk (Potential Discharge)"
        action = "Standard Ambulatory Care / Routine Outpatient Protocol"

    return {
        "admission_probability": round(float(admission_prob), 4),
        "predicted_class": int(admission_prob >= threshold),
        "clinical_decision_threshold": threshold,
        "risk_tier": risk_tier,
        "recommended_action": action,
        "calculated_vitals": {
            "Shock Index": round(float(df_patient['shock_index'].iloc[0]), 2),
            "Mean Arterial Pressure (MAP)": round(float(df_patient['mean_arterial_pressure'].iloc[0]), 2),
            "Pulse Pressure": round(float(df_patient['pulse_pressure'].iloc[0]), 2)
        }
    }