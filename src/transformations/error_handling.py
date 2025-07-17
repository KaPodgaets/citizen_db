import functools
import traceback
from src.utils.db import get_engine
from src.utils.logging_config import logger
from sqlalchemy import text

def global_error_handler(step_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
                logger.error(f"[{step_name}] Pipeline failed: {error_msg}")
                # Log to meta.etl_audit
                engine = get_engine()
                with engine.begin() as conn:
                    conn.execute(text("""
                        INSERT INTO meta.etl_audit (step, status, message)
                        VALUES (:step, 'FAIL', :message)
                    """), {"step": step_name, "message": error_msg})
                raise
        return wrapper
    return decorator 