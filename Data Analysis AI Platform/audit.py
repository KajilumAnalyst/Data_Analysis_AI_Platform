from fastapi import APIRouter, Depends
from app.security import get_current_user_optional

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.get("")
async def list_audit_logs(user=Depends(get_current_user_optional)):
    return [
        {
            "id": "A-1",
            "time": "2026-10-05T18:00:00Z",
            "actor": "Maya",
            "action": "query_executed",
            "entity": "Q-1001",
            "meta": "5 rows in 142 ms"
        }
    ]
