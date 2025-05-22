from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import dashboard, websocket

# Create FastAPI application instance
app = FastAPI()

# Mount the 'templates' directory to serve static files at '/templates' URL
app.mount("/templates", StaticFiles(directory="templates"), name="static")

# Set up Jinja2 templates directory for rendering HTML templates
templates = Jinja2Templates(directory="templates")

# Register the dashboard and websocket routers with the FastAPI app
app.include_router(dashboard.router)
app.include_router(websocket.router)
