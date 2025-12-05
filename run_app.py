import uvicorn

from app.utilities.config import Config

app = "app.main:app"
host = Config.HOST
port = Config.PORT
reload = Config.RELOAD

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port, reload=reload)

    # uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8181
