import uvicorn
from routes import init_app
from settings import config


app, Base = init_app()

app_base_configs = {
    "host": "0.0.0.0",
    "port": config.PORT,
    "workers": config.UVICORN_WORKERS,
    "access_log": True,
    "reload": config.RELOAD
}
if __name__ == '__main__':
    uvicorn.run("main:app", **app_base_configs)
