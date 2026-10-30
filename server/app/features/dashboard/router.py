from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.dashboard import services
from app.features.dashboard.schemas import DashboardRead
from app.models.db import User
from app.shared.dependencies.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "",
    response_model=DashboardRead,
)
def get_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DashboardRead:
    return services.get_dashboard(db, user)
