# Clinical Decision Support System for Emergency Room Admission

An AI-powered clinical decision-support prototype that estimates the likelihood of emergency room admission using patient demographic information and initial vital signs.

## Overview

Emergency departments need to assess patients efficiently and identify those who may require urgent medical attention. This project uses a machine learning model to estimate admission risk from selected patient features and return a risk category with a suggested next step.

**This project is an experimental prototype for educational purposes. It is not a substitute for professional medical judgment, and its predictions must not be used to make real patient-care decisions.**

## Key Features

- Machine learning-based admission-risk prediction using XGBoost.
- FastAPI backend for model inference through a REST API.
- Streamlit frontend for entering patient information and viewing predictions.
- Risk categorization and recommendation display.
- Calculated vital-sign indicators, including Shock Index, Mean Arterial Pressure (MAP), and Pulse Pressure.

## Tech Stack

- **Language:** Python
- **Machine Learning:** XGBoost, scikit-learn
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **API Testing:** Swagger UI
- **Model Storage:** Joblib / Pickle

## Project Structure

```text
Clinical Decision Support System/
├── backend/
│   ├── main.py
│   ├── model.py
│   └── requirements.txt
├── frontend/
│   └── app.py
├── models/
│   └── best_xgb_pipeline.pkl
├── .gitignore
└── README.md
```

## Input Features

The model accepts selected patient information, including:

- Age and sex
- Systolic and diastolic blood pressure
- Heart rate and respiratory rate
- Body temperature
- Pain score
- Arrival mode
- Mental status
- Injury indicator
- Patient volume per hour

## Model Evaluation

The current experimental model has the following reported evaluation results:

| Metric | Result |
|---|---:|
| Accuracy | 72% |
| ROC-AUC | 0.795 |
| Class 1 precision | 66% |
| Class 1 recall | 49% |

These results reflect the current test evaluation and do not establish clinical safety or real-world effectiveness. Performance may vary across populations and settings.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SoumiliMukherjee/clinical-decision-support-system.git
cd clinical-decision-support-system
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r backend/requirements.txt
pip install streamlit requests
```

If a dependency is already included in the requirements file, pip will handle it.

### 4. Start the FastAPI backend

From the project root, run:

```powershell
uvicorn backend.main:app --reload
```

If the import path in `backend/main.py` has not been configured for root-level execution, open a second terminal and run the backend from its directory instead:

```powershell
cd backend
uvicorn main:app --reload
```

Open Swagger UI at:

http://127.0.0.1:8000/docs

### 5. Start the Streamlit frontend

In a separate terminal from the project root, activate the virtual environment if needed, then run:

```powershell
streamlit run frontend/app.py
```

## Future Improvements

- Expand model evaluation and validate performance on independent datasets.
- Improve recall and assess false-negative predictions.
- Add explainability using SHAP or similar methods.
- Add automated tests and input validation.
- Explore secure deployment and monitoring.

## Disclaimer

This software is an educational machine learning prototype. It has not been established as a clinically validated medical device. It must not be used to diagnose, triage, admit, discharge, or treat real patients.

## Author

**Soumili Mukherjee**

GitHub: [SoumiliMukherjee](https://github.com/SoumiliMukherjee)
