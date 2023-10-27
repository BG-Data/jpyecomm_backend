from fastapi import FastAPI
from api.users import UserApi
import uvicorn
from structure.connectors import Base, engine
from structure.models import UserModel
from structure.schemas import UserSchema, UserInsert
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(UserApi(),
                   tags=['Usuarios'],
                   prefix='/user')

app_base_configs = {
    "host": "0.0.0.0",
    "port": 5000,
    "workers": 1,
    "access_log": True,
    "reload": True
}
if __name__ == '__main__':
    uvicorn.run("main:app", **app_base_configs)
