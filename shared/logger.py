import logging
import sys
import json
from datetime import datetime, timezone
from typing import Any

class JSONFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:

        log_data: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno

        }

        if hasattr(record, "request_id"):
            log_data['request_id'] = record.request_id

        if hasattr(record, "user_id"):
            log_data['user_id'] = record.user_id
        if hasattr(record, "duration_ms"):
            log_data['duration_ms'] = record.duration_ms

        if record.exc_info:
            log_data['exc_info'] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("app")
    logger.setLevel(getattr(logging, level.upper()))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    logging.getLogger("unicorn.access").setLevel(logging.WARNING)

    return logger


logger = setup_logging()