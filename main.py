"""
Main FastAPI application entry point.
University Research Data and Thesis Management Portal - Foundation Phase
"""

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import engine, Base, get_db
from routers import auth, thesis, users

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="University Research Thesis Portal",
    description="Foundation phase - Core security and authentication",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(thesis.router, tags=["Thesis"])
app.include_router(users.router, tags=["Users"])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint - redirects to login or dashboard based on auth status"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Dashboard page - shows user-specific content based on role.
    Note: Authentication is handled client-side via JavaScript with JWT token.
    Server-side authentication can be added using cookies if needed.
    """
    # For now, render the dashboard template without server-side auth
    # The template uses JavaScript to fetch user data with the JWT token
    # TODO: Implement cookie-based auth for server-side rendering
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user_email": "",  # Will be populated by JavaScript
            "user_role": "",
            "clearance_level": 0
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

