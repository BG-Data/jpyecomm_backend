import uvicorn
from routes import init_app
from settings import cfg


app, Base = init_app()

app_base_configs = {
    "host": "0.0.0.0",
    "port": cfg.PORT,
    "workers": cfg.UVICORN_WORKERS,
    "access_log": True,
    "reload": cfg.RELOAD
}
if __name__ == '__main__':
    uvicorn.run("main:app", **app_base_configs)
