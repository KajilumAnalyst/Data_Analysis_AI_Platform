from fastapi import APIRouter, Depends
from typing import List
from app.schemas import DashboardCreate, DashboardOut
from app.security import get_current_user_optional

router = APIRouter(prefix="/dashboards", tags=["Dashboards"])

MOCK_DASHBOARDS = []

@router.get("", response_model=List[DashboardOut])
async def list_dashboards(user=Depends(get_current_user_optional)):
    return MOCK_DASHBOARDS

@router.post("", response_model=DashboardOut)
async def create_dashboard(db: DashboardCreate, user=Depends(get_current_user_optional)):
    res = {"id": f"D-{len(MOCK_DASHBOARDS)+1}", "name": db.name, "widgets": db.widgets}
    MOCK_DASHBOARDS.append(res)
    return res
