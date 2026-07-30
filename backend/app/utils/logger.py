import logging
import json
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system_name": "ai-ecosystem-backend",
            "log_level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "filename": record.filename,
            "lineno": record.lineno
        }
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_object.update(record.extra_data)
        return json.dumps(log_object, ensure_ascii=False)

def get_logger(name: str = "ai_ecosystem"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
    return logger

logger = get_logger()
