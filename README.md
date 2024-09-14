# FastAPI Application

Link:
http://localhost:8000/docs

### How to run the application:
If you have docker installed just run the following command:
```bash
docker compose up --build
```

If you prefer using the default way of start a fastapi application you can follow the next steps:

1 Create a virtual environment and activate it
```bash
python3 -m venv venv && source venv/bin/activate
```
2 Install the packages:
```bash
pip install -r requirements.txt
```
3. Once it is installed you can initiate the wsgi server from fastapi using uvcorn:
```bash
uvicorn main:app --reload
```
ps: remember you should be in the root directory to run this command. 

### Operations

There are all the CRUD opertions as:
1. `/api/fetch-user/` (POST)
2. `/api/fetch-admin/` (POST)
3. `/api/users/` Read all users (GET)
4. `/api/users/{user_id}` Get user (GET)
5. `/api/purchases/` Read all purchases (GET)
6. `/api/purchases/{purchase_id}` Get purchase (GET)
5. `/api/reports/` Read all reports (GET)
6. `/api/reports/{report_id}` Get report (GET)