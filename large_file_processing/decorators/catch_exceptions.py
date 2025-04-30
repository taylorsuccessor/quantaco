import functools
import logging

from django.http import JsonResponse

from large_file_processing.exceptions.base import CustomAPIException

logger = logging.getLogger(__name__)


def catch_exceptions(default_code=500):
    """
    Decorator to automatically catch exceptions and return JSON responses.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CustomAPIException as e:
                logger.warning(f"Caught CustomAPIException: {e.message}", exc_info=True)
                return JsonResponse(e.to_dict(), status=e.code)
            except Exception as e:
                logger.critical(f"Caught Unhandled Exception: {str(e)}", exc_info=True)
                return JsonResponse(
                    {
                        "error": "Unexpected server error.",
                        "details": str(e),
                    },
                    status=default_code,
                )

        return wrapper

    return decorator
