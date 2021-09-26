from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Patient(BaseModel):

    object_id: str = Field(None, alias="_id")
    id: Optional[int] = None
    app_id: int
    created_on: datetime = None
    updated_on: datetime = None
    gender: Optional[str] = None
    name: str
    age: Optional[str] = None
    age_in: Optional[str] = None
    patient_no: str = None
    country_code: Optional[str] = None
    mobile_no: Optional[str] = None
    address: Optional[str] = None
    diagnosis: Optional[str] = None
    


class PatientPg(BaseModel):
    page:int
    total:int
    data:List[Patient]
