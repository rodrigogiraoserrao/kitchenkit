from datetime import datetime
import logging
import time

from rich.logging import RichHandler
from rich.text import Text

from .context import started_at


def format_elapsed_time(_: datetime) -> Text:
    start = started_at.get() or time.perf_counter()
    elapsed = round(time.perf_counter() - start)
    h, m = divmod(elapsed, 60)
    return Text(f"[{h:02}:{m:02}]")

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    handlers=[
        RichHandler(
            show_path=False,
            omit_repeated_times=True,
            log_time_format=format_elapsed_time,
        )
    ],
)

logger = logging.getLogger("kitchenkit")
