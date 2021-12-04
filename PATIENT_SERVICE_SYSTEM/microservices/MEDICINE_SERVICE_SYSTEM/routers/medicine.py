"""
FastAPI
"""
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import List
import pprint
from datetime import datetime
from PATIENT_SERVICE_SYSTEM.microservices.MEDICINE_SERVICE_SYSTEM.pydantic_models.models import Medicine, MedicinePg
from PATIENT_SERVICE_SYSTEM.commons.mongodb_connector import get_mongodb

def get_medicine_db() -> AsyncIOMotorDatabase:
    return get_mongodb()

app = APIRouter()

@app.post("/medicine-service-system/medicines", response_model=Medicine)
async def create_medicine(medicine: Medicine):
    medicine_db = get_medicine_db()

    result = await medicine_db.medicines_sequence.update_one({'key': 'MED'},
        {'$inc': {'next': 1}})
    print('updated %s document' % result.modified_count)

    document = await medicine_db.medicines_sequence.find_one({'key' : 'MED'})
    pprint.pprint(document)
    medicine.id = document.get('next')
    medicine.createdOn = datetime.now()
    medicine.updatedOn = datetime.now()
    med_dict = medicine.dict()
    pprint.pprint(med_dict)
    result = await medicine_db.medicines.insert_one(med_dict)
    medicine.object_id = str(result.inserted_id)
    return medicine

@app.get("/medicine-service-system/medicines", response_model=MedicinePg)
async def get_medicines(page_number: int = 1, limit: int = 10):
    medicine_db = get_medicine_db()
    total = await medicine_db.medicines.count_documents({})
    cursor = medicine_db.medicines.find().skip((( page_number - 1 ) * limit )
        if page_number > 0 else 0 ).limit( limit )
    data:List[Medicine] = []
    async for document in cursor:
        medicine = Medicine(name=document.get('name'), generic=document.get('generic'),
            strength=document.get('strength'))
        medicine.object_id = str(document.get('_id'))
        medicine.id = document.get('id')
        medicine.type = document.get('type')
        medicine.createdOn = document.get('createdOn')
        medicine.updatedOn = document.get('updatedOn')
        data.append(medicine)

    return MedicinePg(page=page_number, total=total, data=data)

@app.get("/medicine-service-system/medicines/{medicine_id}", response_model=Medicine)
async def get_medicine(medicine_id: int):
    medicine_db = get_medicine_db()

    document = await medicine_db.medicines.find_one( {'id' : medicine_id})
    medicine = Medicine(name=document.get('name'), generic=document.get('generic'),
        strength=document.get('strength'))
    medicine.object_id = str(document.get('_id'))
    medicine.id = document.get('id')
    medicine.type = document.get('type')
    medicine.createdOn = document.get('createdOn')
    medicine.updatedOn = document.get('updatedOn')
    return medicine

@app.put("/medicine-service-system/medicines/{medicine_id}", response_model=Medicine)
async def update_medicine(medicine_id: int, updates: dict):
    medicine_db = get_medicine_db()

    updates['updatedOn'] = datetime.now()
    result = await medicine_db.medicines.update_one( {'id' : medicine_id},
        {'$set': updates})
    print('updated %s document' % result.modified_count)


    document = await medicine_db.medicines.find_one( {'id' : medicine_id})
    medicine = Medicine(name=document.get('name'), generic=document.get('generic'),
        strength=document.get('strength'))
    medicine.object_id = str(document.get('_id'))
    medicine.id = document.get('id')
    medicine.type = document.get('type')
    medicine.createdOn = document.get('createdOn')
    medicine.updatedOn = document.get('updatedOn')
    return medicine

@app.delete("/medicine-service-system/medicines/{medicine_id}", response_model=dict)
async def del_medicine(medicine_id: int):
    medicine_db = get_medicine_db()

    result = await medicine_db.medicines.delete_many( {'id' : medicine_id})
    print('deleted %s document' % result.deleted_count)

    return {'message' : 'SUCCESS'}
