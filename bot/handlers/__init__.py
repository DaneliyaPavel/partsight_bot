from aiogram import Dispatcher

from .start import router as start_router
from .inline import router as inline_router
from .upload import router as upload_router
from .admin_catalog import router as admin_router
from .repeat import router as repeat_router  # используем только repeat_router


def register_all_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(inline_router)
    dp.include_router(upload_router)
    dp.include_router(admin_router)
    dp.include_router(repeat_router)  # last_act_router убрали
