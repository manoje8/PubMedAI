import logging
import time

from fastapi import FastAPI

from shared.logger import setup_logging
setup_logging()
logger= logging.getLogger(__name__)

class AppState():
    def __init__(self):
        self.start_time = time.time()


app_state = AppState()

app = FastAPI(
    title="Medical Research Assistance",
    description="AI powered medical research and diagnosis support system",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()

    logger.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(f"Response: {response.status_code} {process_time:.3f}s")

    return response



# TODO: Add routes

@app.get("/")
async def root():
    return {
        "name": "Medical Research Assistance",
        "version": "0.0.1",
        "status": "development",
        "health_check": "/health"
    }


@app.get("/health")
async def health():
    uptime = time.time() - app_state.start_time

    return {
        "uptime": uptime,
        "memory": "N/A",
    }