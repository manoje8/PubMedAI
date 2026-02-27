import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.context_engineering.context_engineer import ContextEngineer
from app.core.prompt_engineering.prompt_engineer import PromptEngineer
from app.core.rag_pipeline import RAGPipeline
from shared.logger import setup_logging
from config import Config

setup_logging()
logger= logging.getLogger(__name__)

class AppState():
    def __init__(self):
        self.rag_pipeline = None
        self.context_engineer = None
        self.prompt_engineer = None
        self.start_time = time.time()


app_state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Medical research assistance")

    try:
        logger.info("Initializing...")
        app_state.rag_pipeline = RAGPipeline()
        app_state.context_engineer = ContextEngineer()
        app_state.prompt_engineer = PromptEngineer()

        logger.info("Initialization completed")
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise

    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Medical Research Assistance",
    description="AI powered medical research and diagnosis support system",
    version=Config.APP_VERSION,
    lifespan=lifespan,
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
        "version": Config.APP_VERSION,
        "status": "development",
        "health_check": "/health"
    }


@app.get("/health")
async def health_check():
    return {
        "name": "Medical research assistance",
        "version": Config.APP_VERSION,
        "uptime": time.time() - app_state.start_time,
        "components": {
            "rag": app_state.rag_pipeline is not None,
            "context": app_state.context_engineer is not None,
            "prompt": app_state.prompt_engineer is not None
        }
    }

@app.get("/metrics")
async def get_metric():
    uptime = time.time() - app_state.start_time

    return {
        "uptime": uptime,
        "memory": "N/A",
        "active_connections": len(app.state.active_connections) if hasattr(app.state, 'active_connections') else 0
    }