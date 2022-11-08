from django.core.exceptions import PermissionDenied


def is_student(function):
    
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'student':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def is_teacher(function):
    
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'teacher':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap