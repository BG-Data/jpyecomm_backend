import uvicorn
from init import init_app
from settings import Config

app = init_app()

app_base_configs = {
    "host": "0.0.0.0",
    "port": Config.PORT,
    "workers": Config.UVICORN_WORKERS,
    "access_log": True,
    "reload": Config.RELOAD
}
if __name__ == '__main__':
    uvicorn.run("main:app", **app_base_configs)
