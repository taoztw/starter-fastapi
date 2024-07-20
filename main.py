from app import app
import warnings
from config import settings



warnings.filterwarnings("ignore")


if __name__ == "__main__":
    import uvicorn

    if settings.PROJECT_ENV == "LOCAL":
        uvicorn.run(app='main:app', host="0.0.0.0", port=settings.PROJECT_PORT, reload=True, forwarded_allow_ips="*",
                    proxy_headers=True)
    else:
        uvicorn.run(app='main:app', host="0.0.0.0", port=settings.PROJECT_PORT, reload=False, forwarded_allow_ips="*",
                    proxy_headers=True, workers=4)
