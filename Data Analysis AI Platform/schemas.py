from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: Optional[str] = "Analyst"

class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str
    status: str
    class Config:
        from_attributes = True

class DataSourceCreate(BaseModel):
    name: str
    type: str
    host: str
    db: str
    username: str
    password: str

class DataSourceOut(BaseModel):
    id: str
    name: str
    type: str
    status: str
    last_refreshed_at: Optional[datetime]
    class Config:
        from_attributes = True

class ColumnSchema(BaseModel):
    column_name: str
    data_type: str
    description: Optional[str]
    sensitivity: str

class TableSchema(BaseModel):
    object_name: str
    description: Optional[str]
    is_protected: bool
    columns: List[ColumnSchema]

class MessageCreate(BaseModel):
    content: str

class QueryValidationCheck(BaseModel):
    name: str
    pass_: bool
    detail: str

class QueryValidationResult(BaseModel):
    ok: bool
    checks: List[dict]
    needs_approval: bool
    reasons: List[str]

class QueryOut(BaseModel):
    id: str
    natural_language_question: str
    sql_text: str
    validation_status: str
    approval_status: str
    execution_status: str
    created_at: datetime
    class Config:
        from_attributes = True

class SavedQueryCreate(BaseModel):
    name: str
    sql_text: str
    data_source_id: str

class SavedQueryOut(BaseModel):
    id: str
    name: str
    sql_text: str
    data_source_id: str
    class Config:
        from_attributes = True

class DashboardCreate(BaseModel):
    name: str
    widgets: List[str]

class DashboardOut(BaseModel):
    id: str
    name: str
    widgets: List[Any]
    class Config:
        from_attributes = True
