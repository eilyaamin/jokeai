from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from config.logging_config import setup_logging

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = setup_logging()

@router.get("/")
async def dashboard(request: Request):
    logger.info("Dashboard accessed")
    return templates.TemplateResponse("index.html", {"request": request})
