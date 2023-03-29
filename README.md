# simple-fastapi-authentication
A simple FastAPI Login, Register application with admin

## Setup
```
pip install -r requirements.txt
```

## Run Alembic migrations
  ```
  alembic upgrade head
  ```

### Admin - add user_id manually to admin table

## Routes
  ### user
    /login    - Login
    /register - create user
    /         - proteced route
  
  ### admin
    /admin/user - To see all users
