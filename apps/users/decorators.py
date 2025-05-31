from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def role_required(*roles):
    def decorator(view):
        @login_required
        def _wrapped(request, *a, **kw):
            if request.user.is_superuser or request.user.role in roles:
                return view(request, *a, **kw)
            return render(request, "403_forbidden.html", status=403)

        return _wrapped

    return decorator
