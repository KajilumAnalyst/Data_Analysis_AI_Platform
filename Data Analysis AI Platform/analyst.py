from fastapi import APIRouter, Depends
from app.schemas import MessageCreate
from app.agent import AIAgentService
from app.security import get_current_user_optional

router = APIRouter(prefix="/analyst", tags=["Analyst"])

@router.post("/conversations")
async def create_conversation(user=Depends(get_current_user_optional)):
    return {"id": "conv-101", "title": "New Analysis"}

@router.post("/conversations/{conv_id}/messages")
async def send_message(conv_id: str, msg: MessageCreate, user=Depends(get_current_user_optional)):
    sql = await AIAgentService.generate_sql_from_nl(msg.content, [])
    return {
        "id": "msg-202",
        "role": "bot",
        "content": f"Generated SQL for: {msg.content}",
        "sql": sql,
        "query_id": "Q-1001"
    }
