from fastapi import APIRouter, Depends
from typing import List
from app.schemas import SavedQueryCreate, SavedQueryOut
from app.security import get_current_user_optional

router = APIRouter(prefix="/saved-queries", tags=["Saved Queries"])

MOCK_SAVED = []

@router.get("", response_model=List[SavedQueryOut])
async def list_saved_queries(user=Depends(get_current_user_optional)):
    return MOCK_SAVED

@router.post("", response_model=SavedQueryOut)
async def create_saved_query(sq: SavedQueryCreate, user=Depends(get_current_user_optional)):
    res = {"id": f"S-{len(MOCK_SAVED)+1}", "name": sq.name, "sql_text": sq.sql_text, "data_source_id": sq.data_source_id}
    MOCK_SAVED.append(res)
    return res
