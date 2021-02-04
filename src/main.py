import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.database.base import engine, Base
from src.endpoints import docs, organizations, annotators, annotation_types, audio_format, audio, audio_annotations, datasets
from src.utils.common_logger import logger

Base.metadata.create_all(bind=engine)

# Create API Application
app = FastAPI()


# Global error handler
@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    logger.error(base_error_message)
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}", "detail": f"{err}"})

# Add endpoints
app.include_router(docs.router)
app.include_router(organizations.router)
app.include_router(annotators.router)
app.include_router(annotation_types.router)
app.include_router(audio_format.router)
app.include_router(audio.router)
app.include_router(audio_annotations.router)
app.include_router(datasets.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
