import os
import uuid
import time
from flask import current_app, session, request, g as app_ctx


def log_after_request(response):
    total_time = time.perf_counter() - app_ctx.start
    latency_ms = int(total_time * 1000)

    id = os.getenv("ENVIRONMENT") + "_testID"
    resp = current_app.posthog.identify(
        id, {"display_name": "TEST VALUE"}
    )
    print(resp)

    current_app.logger.info(
        "%s %s %s %s %s",
        request.remote_addr,
        request.method,
        request.path,
        response.status,
        latency_ms,
        extra={"ctx": session.get("ctx", "no-context")},
    )

    return response


def save_logging_context_before_request():
    app_ctx.start = time.perf_counter()
    session["ctx"] = f"ctx_{uuid.uuid4()}"
