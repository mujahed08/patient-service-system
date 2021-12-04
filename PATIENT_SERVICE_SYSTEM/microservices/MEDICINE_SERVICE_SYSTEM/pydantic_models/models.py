from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Medicine(BaseModel):

    object_id: str = Field(None, alias="_id")
    id: Optional[int] = None
    createdOn: datetime = None
    updatedOn: datetime = None
    type: Optional[str] = None
    name: str
    generic: str
    strength: List[str]


class MedicinePg(BaseModel):
    page:int
    total:int
    data:List[Medicine]
