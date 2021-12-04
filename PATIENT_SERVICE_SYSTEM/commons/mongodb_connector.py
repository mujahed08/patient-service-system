from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

def get_patient_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient('mongodb://root:example@localhost:27017')
    return client.mvppatientdb

def get_mongodb() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient('mongodb://root:example@localhost:27017')
    return client.mvppatientdb
    