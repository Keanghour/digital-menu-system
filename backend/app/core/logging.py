import logging
import os
import time
import uuid
import json
from logging.handlers import TimedRotatingFileHandler
from fastapi import Request
from starlette.responses import Response, JSONResponse, StreamingResponse
from datetime import datetime

# --------------------------
# Log folder setup
# --------------------------
LOG_FOLDER = "app/logs"
os.makedirs(LOG_FOLDER, exist_ok=True)
today_str = datetime.now().strftime("%d%m%Y")
LOG_FILE = os.path.join(LOG_FOLDER, f"{today_str}.log")

# --------------------------
# Logger Configuration
# --------------------------
logger = logging.getLogger("fastapi_project")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler
file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=30)
file_handler.setFormatter(formatter)
file_handler.suffix = "%d%m%Y.log"
logger.addHandler(file_handler)

# --------------------------
# Middleware Helpers
# --------------------------
MAX_BODY_LENGTH = 2000  # truncate large bodies
STREAM_PREVIEW_LENGTH = 500  # preview for streaming responses

def mask_sensitive(data):
    """Mask sensitive info like passwords."""
    if isinstance(data, dict):
        return {k: ("****" if k.lower() == "password" else mask_sensitive(v)) for k, v in data.items()}
    elif isinstance(data, list):
        return [mask_sensitive(i) for i in data]
    return data

def safe_json_loads(data):
    """Try decode JSON, else return placeholder"""
    try:
        return json.loads(data.decode("utf-8")) if data else {}
    except Exception:
        return "[hidden / non-serializable]"

def truncate_body(data):
    """Truncate large bodies"""
    s = str(data)
    if len(s) > MAX_BODY_LENGTH:
        return s[:MAX_BODY_LENGTH] + "...[truncated]"
    return data

# --------------------------
# Middleware for Request/Response Logging
# --------------------------
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    # Read and mask request body
    body_bytes = await request.body()
    request_data = truncate_body(mask_sensitive(safe_json_loads(body_bytes)))

    # Process request
    response: Response = await call_next(request)
    process_time = round((time.time() - start_time) * 1000, 2)

    # Capture response body safely
    response_data = "[hidden / non-serializable]"
    try:
        if isinstance(response, JSONResponse):
            # JSONResponse has .body
            response_data = truncate_body(mask_sensitive(json.loads(response.body.decode("utf-8"))))
        elif isinstance(response, StreamingResponse):
            # Don’t consume the whole stream, just note it
            response_data = f"[streaming content, preview hidden]"
        elif hasattr(response, "body") and response.body:
            response_data = truncate_body(mask_sensitive(safe_json_loads(response.body)))
        else:
            response_data = "[no body content]"
    except Exception:
        response_data = "[hidden / non-serializable]"

    log_prefix = f"[{request_id}] [{response.status_code}] [{process_time}ms] [{request.method}]"
    logger.info(f"{log_prefix} Request: {request.url} Body: {request_data}")
    logger.info(f"{log_prefix} Response: {response_data}")

    return response
