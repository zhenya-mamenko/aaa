from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import make_routers_list
from app.config import settings


app = FastAPI(
    title=f"{settings.app_name} API",
    description=f"See more on {settings.github_link}",
    version=settings.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers_list = make_routers_list("v1")
for r in routers_list:
    app.include_router(r["router"], prefix=f"/api/v1{r['path']}")
