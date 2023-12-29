import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.constants import (
    FAQ_UPDATE_INTERVAL_MINUTES,
    TOKEN_UPDATE_HOURS,
    AdminWorkTime,
)
from handlers.faq import update_faq
from core.requests_db import get_token
from core.services import send_delayed_questions


def scheduller_initial(bot) -> AsyncIOScheduler:
    timezone = pytz.timezone(AdminWorkTime.TIMEZONE)
    scheduller = AsyncIOScheduler(timezone=timezone)
    scheduller.add_job(
        func=update_faq,
        trigger="interval",
        minutes=FAQ_UPDATE_INTERVAL_MINUTES,
    )
    scheduller.add_job(
        func=get_token,
        trigger="interval",
        hours=TOKEN_UPDATE_HOURS,
    )

    scheduller.add_job(
        func=send_delayed_questions,
        trigger="cron",
        hour=AdminWorkTime.START_H,
        minute=AdminWorkTime.START_MIN,
        kwargs={"bot": bot},
    )

    return scheduller
