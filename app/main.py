import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import init_db
from app.api.v1 import auth, books, reviews, recommendations

#
# Define Lifespan
#
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    pass

#
# FastAPI constructor
#
app = FastAPI(
    title="Intelligent Book Management System", 
    version="1.0.0",
    lifespan=lifespan
)

#
# CORS configuration
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
# Include API Routers
#
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(reviews.router, prefix="/api/v1/books", tags=["reviews"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])

#
# Run app
#
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
