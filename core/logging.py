import json
import logging
import sys
from datetime import datetime, timezone

logger = logging.getLogger("meridian")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)

def log_event(event: dict):
    event["timestamp"] = datetime.now(timezone.utc).isoformat()
    logger.info(json.dumps(event))