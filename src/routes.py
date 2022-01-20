from fastapi import APIRouter

from rewordle.views import router as rewordle_router
from service.views import router as service_router

main_router = APIRouter()
main_router.include_router(service_router, tags=["service"])
main_router.include_router(rewordle_router, tags=["rewordle"])
