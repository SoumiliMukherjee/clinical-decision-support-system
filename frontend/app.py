import streamlit as st
import requests

st.set_page_config(
    page_title='ED Admission Risk Predictor',
    page_icon='🏥',
    layout='wide'
)

st.title('Emergency Department Admission Risk')
st.subheader('Clinical Desicion Support system')

st.write("Enter the patient's clinical information below to estimate admission risk")

st.divider()

st.header("Patient's Information")
col1 , col2 , col3 = st.columns(3)

with col1:
    age = st.number_input(
        'Age',
        min_value= 0,
        max_value= 120,
        value= 30
    )

with col2:
    sex = st.selectbox(
        'Sex',
        options=[1 , 2],
        format_func=lambda x:'Male' if x == 1 else 'Female'
    )

with col3:
    mental = st.selectbox(
        'Mental Status',
        options=[1 , 2],
        format_func=lambda x:'Alert' if x == 1 else 'Verbal/Altered'
    )
col1 , col2 , col3  = st.columns(3)

with col1:
    arrival_mode = st.selectbox(
        'Arival Mode',
        options=[1 , 2],
        format_func=lambda x: 'Walk-in' if x == 1 else 'Ambulance'
    )
with col2:
    injury = st.selectbox(
        'Injury',
        options=[1,2],
        format_func=lambda x: 'Injury' if x== 1 else 'Non Injury / Medical'
    )
with col3:
    nrs_pain = st.number_input(
        'NRS-Pain',
        min_value=0,
        max_value=10,
        value=0
    )
st.header('Vital Sign')
col1 , col2 , col3 , col4 = st.columns(4)

with col1:
    sbp = st.number_input(
        'Systolic BP (SBP)',
        min_value=40.0,
        max_value=250.0,
        value= 120.0
    )

with col2:
    dbp = st.number_input(
        'Diastolic BP',
        min_value=20.0,
        max_value=150.0,
        value=80.0
    )

with col3:
    hr = st.number_input(
        'Heart Rate',
        min_value=20.0,
        max_value=250.0,
        value=75.0
    )

with col4:
    rr = st.number_input(
        'Respiratory Rate',
        min_value= 5.0,
        max_value=80.0,
        value=16.0
    )


col1 , col2 = st.columns(2)

with col1:
    bt = st.number_input(
        'Body Temperature',
        min_value=30.0,
        max_value=45.0,
        value=36.6
    )

with col2:
    patients_no_per_hour = st.number_input(
        'Patients per Hour',
        min_value=0.0,
        max_value=100.0,
        value=8.0
    )
st.divider()

if st.button(
    'Predict Admission Risk',
    use_container_width=True
):
    patient_data = {
        'age': age,
        'sex': sex,
        'mental' : mental,
        'arrival_mode' : arrival_mode,
        'injury' : injury,
        'nrs_pain' : nrs_pain,
        'sbp': sbp,
        'dbp' : dbp,
        'bt' : bt,
        'rr' : rr,
        'hr':hr,
        'patients_number_per_hour':patients_no_per_hour

    }

    try:
        response = requests.post(
            'https://clinical-decision-support-system-83wq.onrender.com/predict',
            json=patient_data,
            timeout=60
        )
        if response.status_code== 200:
            result = response.json()
            probability = result['admission_probability'] * 100
            risk_tier = result['risk_tier']
            action = result['recommended_action']
            st.divider()

            st.header('prediction Result')
            col1 , col2 , col3 = st.columns(3)

            with col1:
                st.metric(
                    'Admission Probability',
                    f"{probability:.2f}%"
                )
                st.metric(
                    'Risk Tier',
                    risk_tier
                )
                st.metric(
                    'Decison',
                    'Admission'
                    if result['predicted_class'] == 1 else 'Potential Discharge'
                )
                st.subheader("Clinical Recommendation")

                st.info(action)

                st.subheader('Calculated Clinical Indicators')
                vitals = result['calculated_vitals']
                col1 , col2 , col3 = st.columns(3)
                with col1:
                    st.metric(
                        'Shock Index',
                        vitals['Shock Index']
                    )
                with col2:
                    st.metric(
                        'Mean Arterial Pressure (MAP)',
                        vitals['Mean Arterial Pressure (MAP)']
                    )
                with col3:
                    st.metric(
                        'Pulse Pressure',
                        vitals['Pulse Pressure']
                    )
        else:
            st.error(
                f"API Error: {response.status_code}"
            )

            st.code(response.text)
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI. "
            "Make sure the backend server is running.")
    except requests.exceptions.Timeout:
        st.error("The prediction request timed out.")
    except Exception as e:
         st.error(
            f"Unexpected error: {str(e)}"
        )
st.divider()

st.caption(
    "⚠️ This system is a clinical decision-support prototype "
    "and is not a substitute for professional medical judgment."
)

