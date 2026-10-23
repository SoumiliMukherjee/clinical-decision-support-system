from fastapi import FastAPI
from pydantic import BaseModel

from backend.model import predict_patient_admission_risk

app = FastAPI(
    title='mergency Department Admission Risk API',
    description='Predicts patient admission risk using XGBoost',
    version='1.0'
)

class PatientData(BaseModel):
    age: float
    patients_number_per_hour: float

    sbp: float
    dbp: float
    hr: float
    rr: float
    bt: float
    nrs_pain: float

    arrival_mode: int
    mental: int
    sex: int
    injury: int

@app.get('/')
def home():
    return{'message':'Emergency Department Admission Risk API is running'}

@app.post('/predict')
def predict(patient : PatientData):
    result = predict_patient_admission_risk(
        patient.model_dump(),
        threshold=0.25
    )
    return result