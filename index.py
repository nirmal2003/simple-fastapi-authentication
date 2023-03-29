from fastapi import FastAPI
from routes import user, admin

app = FastAPI(docs_url=None)


app.include_router(user.router)
app.include_router(admin.router)
