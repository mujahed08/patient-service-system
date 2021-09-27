"""
FastAPI
"""
import os
import pprint
from datetime import datetime
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from PATIENT_SERVICE_SYSTEM.commons.logger import get_logger
from PATIENT_SERVICE_SYSTEM.pydantic_models.enviornment import Settings
from PATIENT_SERVICE_SYSTEM.pydantic_models.models import Patient, PatientPg

logger = get_logger('main.py')
run_env:str = os.environ['RUN_ENV']
settings = Settings(_env_file=f'{run_env}.env', _env_file_encoding='utf-8')

logger.info('   Initiliazing Fast API app')
app = FastAPI(title="FastAPI")
origins = [
    "http://localhost:8030",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_patient_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient('mongodb://root:example@localhost:27017')
    return client.mvppatientdb

@app.post("/patient-service-system/patients", response_model=Patient)
async def create_patient(patient: Patient):
    patient_db = get_patient_db()

    result = await patient_db.patients_sequence.update_one({'key': 'PAT'},
        {'$inc': {'next': 1}})
    print('updated %s document' % result.modified_count)

    document = await patient_db.patients_sequence.find_one({'key' : 'PAT'})
    pprint.pprint(document)
    patient.id = document.get('next')
    patient.app_id = 100
    patient.patient_no = document.get('next')
    patient.created_on = datetime.now()
    patient.updated_on = datetime.now()
    pat_dict = patient.dict()
    pprint.pprint(pat_dict)
    result = await patient_db.patients.insert_one(pat_dict)
    patient.object_id = str(result.inserted_id)
    return patient

@app.get("/patient-service-system/patients", response_model=PatientPg)
async def get_patients(page_number: int = 1, limit: int = 10):
    patient_db = get_patient_db()
    total = await patient_db.patients.count_documents({})
    cursor = patient_db.patients.find().skip((( page_number - 1 ) * limit )
        if page_number > 0 else 0 ).limit( limit )
    data:List[Patient] = []
    async for document in cursor:
        patient = Patient(name=document.get('name'), app_id=document.get('app_id'),
            patient_no=str(document.get('id')))
        patient.object_id = str(document.get('_id'))
        patient.id = document.get('id')
        patient.app_id = document.get('app_id')
        patient.created_on = document.get('created_on')
        patient.updated_on = document.get('updated_on')
        patient.gender = document.get('gender')
        patient.age = document.get('age')
        patient.age_in = document.get('age_in')
        patient.country_code = document.get('country_code')
        patient.mobile_no = document.get('mobile_no')
        patient.address = document.get('address')
        patient.diagnosis = document.get('diagnosis')
        data.append(patient)

    return PatientPg(page=page_number, total=total, data=data)

@app.get("/patient-service-system/patients/{patient_id}", response_model=Patient)
async def get_patient(patient_id: int):
    patient_db = get_patient_db()

    document = await patient_db.patients.find_one( {'id' : patient_id})
    patient = Patient(name=document.get('name'), app_id=document.get('app_id'), 
        patient_no=str(document.get('id')))
    patient.object_id = str(document.get('_id'))
    patient.id = document.get('id')
    patient.app_id = document.get('app_id')
    patient.created_on = document.get('created_on')
    patient.updated_on = document.get('updated_on')
    patient.gender = document.get('gender')
    patient.age = document.get('age')
    patient.age_in = document.get('age_in')
    patient.country_code = document.get('country_code')
    patient.mobile_no = document.get('mobile_no')
    patient.address = document.get('address')
    patient.diagnosis = document.get('diagnosis')
    return patient

@app.put("/patient-service-system/patients/{patient_id}", response_model=Patient)
async def update_patient(patient_id: int, updates: dict):
    patient_db = get_patient_db()

    updates['updated_on'] = datetime.now()
    result = await patient_db.patients.update_one( {'id' : patient_id},
        {'$set': updates})
    print('updated %s document' % result.modified_count)


    document = await patient_db.patients.find_one( {'id' : patient_id})
    patient = Patient(name=document.get('name'), app_id=document.get('app_id'), 
        patient_no=str(document.get('id')))
    patient.object_id = str(document.get('_id'))
    patient.id = document.get('id')
    patient.app_id = document.get('app_id')
    patient.created_on = document.get('created_on')
    patient.updated_on = document.get('updated_on')
    patient.gender = document.get('gender')
    patient.age = document.get('age')
    patient.age_in = document.get('age_in')
    patient.country_code = document.get('country_code')
    patient.mobile_no = document.get('mobile_no')
    patient.address = document.get('address')
    return patient

@app.delete("/patient-service-system/patients/{patient_id}", response_model=dict)
async def del_patient(patient_id: int):
    patient_db = get_patient_db()

    result = await patient_db.patients.delete_many( {'id' : patient_id})
    print('deleted %s document' % result.deleted_count)

    return {'message' : 'SUCCESS'}

logger.info('   End of the main file')
