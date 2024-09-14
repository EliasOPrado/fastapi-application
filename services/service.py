import os
import requests
from typing import Type, Union
from db.session import Base
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import User, Purchase, Report

# External API URLs
TOKEN_URL = "https://api-onecloud.multicloud.tivit.com/fake/token"
USER_URL = "https://api-onecloud.multicloud.tivit.com/fake/user"
ADMIN_URL = "https://api-onecloud.multicloud.tivit.com/fake/admin"

def get_jwt_token(username: str, password: str):
    token_url = f"{TOKEN_URL}?username={username}&password={password}"
    response = requests.post(token_url, verify=False)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    
    raise HTTPException(status_code=400, detail="Invalid credentials")

def fetch_user_and_insert_into_db(db: Session, user_type: str):
    # Define mappings for URLs, tokens, and roles
    user_config = {
        "user": {
            "url": USER_URL,
            "password": os.getenv("USER_PASSWORD"),
            "role": "user"
        },
        "admin": {
            "url": ADMIN_URL,
            "password": os.getenv("ADMIN_PASSWORD"),
            "role": "admin"
        }
    }

    if user_type not in user_config:
        raise HTTPException(status_code=400, detail="Invalid user type")

    config = user_config[user_type]
    
    # Get the JWT token
    token = get_jwt_token(user_type, config["password"])
    headers = {"Authorization": f"Bearer {token}"}
    
    # Fetch data from the external service
    response = requests.get(config["url"], headers=headers, verify=False)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

    user_data = response.json()
    
    # Create the User object
    user = User(
        name=user_data["data"]["name"],
        email=user_data["data"]["email"],
        role=config["role"]
    )
    db.add(user)
    db.commit()  # Commit to generate user.id
    
    # Add related data
    if user_type == 'user':
        for purchase in user_data["data"].get("purchases", []):
            db.add(Purchase(id=purchase["id"], item=purchase["item"], price=purchase["price"], user_id=user.id))

    elif user_type == 'admin':
        for report in user_data["data"].get("reports", []):
            db.add(Report(id=report["id"], title=report["title"], status=report["status"], user_id=user.id))
    
    db.commit()
    return db.query(User).order_by(User.id.desc()).first()

def get_object_or_404(model: Type[Base], db: Session, item_id: int) -> Union[Base, None]:
    _model = db.query(model).filter(model.id == item_id).first()
    if _model is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return _model