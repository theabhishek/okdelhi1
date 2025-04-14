from functools import wraps
from django.utils.deprecation import RemovedInDjango60Warning
import warnings

def django_deprecated_view(reason=None):
    """
    Decorator to mark a Django view as deprecated.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            warnings.warn(
                reason or f"{view_func.__name__} is deprecated.",
                RemovedInDjango60Warning,
                stacklevel=2
            )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator 