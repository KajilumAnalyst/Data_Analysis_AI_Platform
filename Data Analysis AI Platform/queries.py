from fastapi import APIRouter, Depends, HTTPException
from app.security import get_current_user_optional
from app.sql_policy import validate_sql_policy
from app.agent import AIAgentService

router = APIRouter(prefix="/queries", tags=["Queries"])

MOCK_SCHEMA = [
    {"name": "customers", "protected": False},
    {"name": "orders", "protected": False},
    {"name": "employees", "protected": True}
]

@router.post("/{query_id}/validate")
async def validate_query(query_id: str, payload: dict = None, user=Depends(get_current_user_optional)):
    sql = payload.get("sql", "SELECT * FROM orders") if payload else "SELECT * FROM orders"
    ok, checks, needs_approval, reasons = validate_sql_policy(sql, MOCK_SCHEMA)
    return {"ok": ok, "checks": checks, "needs_approval": needs_approval, "reasons": reasons}

@router.post("/{query_id}/execute")
async def execute_query(query_id: str, user=Depends(get_current_user_optional)):
    mock_rows = [{"region": "North America", "revenue": 482000}, {"region": "Europe", "revenue": 351000}]
    explanation = await AIAgentService.generate_explanation("Revenue by region", "", mock_rows)
    return {
        "query_id": query_id,
        "execution_status": "success",
        "duration_ms": 142,
        "row_count": len(mock_rows),
        "rows": mock_rows,
        "explanation": explanation
    }

@router.get("/{query_id}")
async def get_query_details(query_id: str, user=Depends(get_current_user_optional)):
    return {
        "id": query_id,
        "natural_language_question": "Revenue by region",
        "sql_text": "SELECT region, SUM(total) FROM orders GROUP BY region",
        "validation_status": "passed",
        "approval_status": "none",
        "execution_status": "success"
    }

@router.get("/{query_id}/results")
async def get_query_results(query_id: str, user=Depends(get_current_user_optional)):
    return {
        "query_id": query_id,
        "rows": [{"region": "North America", "revenue": 482000}],
        "explanation": "Summary grounded in data."
    }
