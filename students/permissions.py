from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsDirectorOrSuperuser(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.is_director

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.is_director


class IsTutor(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.tutor == request.user


class IsStudentCreator(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.created_by == request.user
