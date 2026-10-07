from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.auth import router as auth_router
from app.api.datasources import router as datasources_router
from app.api.analyst import router as analyst_router
from app.api.queries import router as queries_router
from app.api.saved_queries import router as saved_queries_router
from app.api.dashboards import router as dashboards_router
from app.api.audit import router as audit_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach routes required by PRD and index.html
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(datasources_router, prefix=settings.API_V1_STR)
app.include_router(analyst_router, prefix=settings.API_V1_STR)
app.include_router(queries_router, prefix=settings.API_V1_STR)
app.include_router(saved_queries_router, prefix=settings.API_V1_STR)
app.include_router(dashboards_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.VERSION}
