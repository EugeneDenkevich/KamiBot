from kami.bot_admin.handlers.sending.run_photo_sending import (
    router as photo_sending_router,
)
from kami.bot_admin.handlers.sending.run_text_sending import (
    router as text_sending_router,
)
from kami.bot_admin.handlers.sending.run_video_note_sending import (
    router as video_note_sending_router,
)
from kami.bot_admin.handlers.sending.run_video_sending import (
    router as video_sending_router,
)
from kami.bot_admin.handlers.sending.start_sending import router as sending_start_router

__all__ = (
    "sending_start_router",
    "text_sending_router",
    "photo_sending_router",
    "video_sending_router",
    "video_note_sending_router",
)
