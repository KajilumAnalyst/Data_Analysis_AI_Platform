from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from app.schemas import DataSourceCreate, DataSourceOut
from app.security import get_current_user_optional

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])

MOCK_DATA_SOURCES = [
    {
        "id": "ds1",
        "name": "Sales warehouse",
        "type": "PostgreSQL",
        "status": "Connected",
        "last_refreshed_at": datetime.utcnow()
    }
]

@router.get("", response_model=List[DataSourceOut])
async def list_data_sources(user=Depends(get_current_user_optional)):
    return MOCK_DATA_SOURCES

@router.post("", response_model=DataSourceOut)
async def create_data_source(ds: DataSourceCreate, user=Depends(get_current_user_optional)):
    new_ds = {
        "id": f"ds{len(MOCK_DATA_SOURCES) + 1}",
        "name": ds.name,
        "type": ds.type,
        "status": "Connected",
        "last_refreshed_at": datetime.utcnow()
    }
    MOCK_DATA_SOURCES.append(new_ds)
    return new_ds

@router.post("/{ds_id}/refresh-schema")
async def refresh_schema(ds_id: str, user=Depends(get_current_user_optional)):
    for ds in MOCK_DATA_SOURCES:
        if ds["id"] == ds_id:
            ds["last_refreshed_at"] = datetime.utcnow()
            ds["status"] = "Connected"
            return {"status": "success", "message": "Schema refreshed"}
    raise HTTPException(status_code=404, detail="Data source not found")

@router.get("/{ds_id}/schema")
async def get_schema(ds_id: str, user=Depends(get_current_user_optional)):
    return {
        "tables": [
            {"name": "customers", "protected": False, "columns": [["id", "integer", "Primary key", "public"], ["email", "text", "Customer email", "confidential"]]},
            {"name": "orders", "protected": False, "columns": [["id", "integer", "Primary key", "public"], ["total", "numeric", "Order amount", "internal"]]},
            {"name": "employees", "protected": True, "columns": [["salary", "numeric", "Salary", "restricted"]]}
        ]
    }
