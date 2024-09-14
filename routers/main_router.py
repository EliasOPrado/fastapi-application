import requests
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from db.session import get_db
from db.models import User, Purchase, Report
from starlette import status
from services.service import get_object_or_404, fetch_user_and_insert_into_db

router = APIRouter(prefix="/api", tags=["API"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/fetch-user/", status_code=status.HTTP_200_OK)
def fetch_user(db: Session = Depends(get_db)):
    return fetch_user_and_insert_into_db(db, user_type="user")


@router.post("/fetch-admin/", status_code=status.HTTP_200_OK)
def fetch_admin(db: Session = Depends(get_db)):
    return fetch_user_and_insert_into_db(db, user_type="admin")


@router.get("/users/", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency):
    return db.query(User).all()


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user_id: int = Path(gt=0)):
    return get_object_or_404(User, db, user_id)


@router.get("/purchases/", status_code=status.HTTP_200_OK)
async def read_all_purchases(db: db_dependency):
    return db.query(Purchase).all()


@router.get("/purchases/{purchase_id}", status_code=status.HTTP_200_OK)
async def get_purchase(db: db_dependency, purchase_id: int = Path(gt=0)):
    return get_object_or_404(Purchase, db, purchase_id)


@router.get("/reports/", status_code=status.HTTP_200_OK)
async def read_all_reports(db: db_dependency):
    return db.query(Report).all()


@router.get("/reports/{report_id}", status_code=status.HTTP_200_OK)
async def get_report(db: db_dependency, report_id: int = Path(gt=0)):
    return get_object_or_404(Report, db, report_id)
