import uuid
from datetime import datetime
from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def gen_uuid():
    return str(uuid.uuid4())

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active")

class Membership(Base):
    __tablename__ = "memberships"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String, default="Analyst") # Admin, Analyst, Viewer, Approver

class DataSource(Base):
    __tablename__ = "data_sources"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    encrypted_config: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String, default="Pending schema")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_refreshed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class SchemaObject(Base):
    __tablename__ = "schema_objects"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    data_source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id"))
    schema_name: Mapped[str] = mapped_column(String, default="public")
    object_name: Mapped[str] = mapped_column(String, nullable=False)
    object_type: Mapped[str] = mapped_column(String, default="table")
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_protected: Mapped[bool] = mapped_column(Boolean, default=False)
    last_refreshed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SchemaColumn(Base):
    __tablename__ = "schema_columns"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    schema_object_id: Mapped[str] = mapped_column(ForeignKey("schema_objects.id"))
    column_name: Mapped[str] = mapped_column(String, nullable=False)
    data_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    sensitivity: Mapped[str] = mapped_column(String, default="public") # public, internal, confidential, restricted

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    data_source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id"))
    title: Mapped[str] = mapped_column(String, default="New Conversation")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class QueryRecord(Base):
    __tablename__ = "queries"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"), nullable=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    data_source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id"))
    natural_language_question: Mapped[str] = mapped_column(Text, nullable=False)
    sql_text: Mapped[str] = mapped_column(Text, nullable=False)
    validation_status: Mapped[str] = mapped_column(String, default="pending") # passed, failed
    approval_status: Mapped[str] = mapped_column(String, default="none") # none, required, pending, approved, rejected
    execution_status: Mapped[str] = mapped_column(String, default="not_run") # not_run, running, success, failed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class QueryResult(Base):
    __tablename__ = "query_results"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    query_id: Mapped[str] = mapped_column(ForeignKey("queries.id"))
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    result_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    explanation: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SavedQuery(Base):
    __tablename__ = "saved_queries"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    data_source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    sql_text: Mapped[str] = mapped_column(Text, nullable=False)

class Dashboard(Base):
    __tablename__ = "dashboards"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    widgets: Mapped[dict] = mapped_column(JSON, default=list)

class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    query_id: Mapped[str] = mapped_column(ForeignKey("queries.id"))
    requested_by: Mapped[str] = mapped_column(String, nullable=False)
    approved_by: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending")
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    actor_id: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
