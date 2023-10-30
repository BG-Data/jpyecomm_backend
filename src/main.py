import uvicorn
from init import init_app

app = init_app()

app_base_configs = {
    "host": "0.0.0.0",
    "port": 5000,
    "workers": 1,
    "access_log": True,
    "reload": True
}
if __name__ == '__main__':
    uvicorn.run("main:app", **app_base_configs)
