from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Issue(BaseModel):
    object_id: str = Field(None, alias="_id")
    id: Optional[int] = None
    app_id: int
    created_on: datetime = None
    updated_on: datetime = None
    summary: str = None
    type: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str]
    weightage: int = 1
    remarks: Optional[str] = None
    expectations: Optional[str] = None
    estimate: Optional[str] = None
    remaining: Optional[str] = None

class IssuePg(BaseModel):
    page:int
    total:int
    data:List[Issue]
