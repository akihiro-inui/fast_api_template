from fastapi import APIRouter
from starlette.responses import RedirectResponse
router = APIRouter()


@router.get("/")
def main():
    return RedirectResponse(url="/docs/")
