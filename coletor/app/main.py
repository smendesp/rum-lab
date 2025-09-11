from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

from app.lib.logger import Logger
from app.services.utils import Utils
from app.routes import health, rum, node_graph

# from app.lib.metrics import Metrics


log = Logger()
utils = Utils()
# metrics = Metrics()

pyproject = utils.get_pyproject()

# inicializar API (app)
app = FastAPI(
    title=pyproject['project']['name'],
    description=pyproject['project']['description'],
    version=pyproject['project']['version'],
    docs_url='/docs',
    redoc_url='/redoc',
    default_response_class=ORJSONResponse,
)

origins = [
    '*',  # Allow requests from all Development only
    'http://localhost',  # Allow requests from localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],  # Allow all standard HTTP methods, including OPTIONS
    allow_headers=['*'],  # Allow all headers
)

# Carregar Rotas
app.include_router(health.router)
app.include_router(rum.router)
app.include_router(node_graph.router)

# Eventos
@app.on_event('startup')
async def startup_event():
    log.logger.info('Application startup')


@app.on_event('shutdown')
async def shutdown_event():
    log.logger.info('Application shutdown')
