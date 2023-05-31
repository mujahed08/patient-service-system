"""
FastAPI
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydrapp.commons.logger import get_logger
from pydrapp.pylidate.enviornment import Settings
from .routers.patient import app as patient_router
from .microservices.medicine.routers.medicine import app as medicine_router
from .microservices.catch.routers.issue import app as issue_router

logger = get_logger('main.py')
run_env:str = 'dev' #os.environ['RUN_ENV']
settings = Settings(_env_file=f'{run_env}.env', _env_file_encoding='utf-8')

logger.info('   Initiliazing Fast API app')
app = FastAPI(title="FastAPI")
app.include_router(patient_router)
app.include_router(medicine_router)
app.include_router(issue_router)
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

logger.info('   End of the main file')
