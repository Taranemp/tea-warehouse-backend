from rest_framework import permissions

class DynamicGroupBasedPermission(permissions.BasePermission):
    """
    Fully dynamic permission class.
    - Checks if user is authenticated.
    - Checks if user belongs to at least one group.
    - Maps HTTP methods to Django model permissions (view, add, change, delete).
    - If admin removes a permission from a group, access is instantly revoked.
    """

    def has_permission(self, request, view):
        user = request.user

        # 1. Strict Authentication Check
        if not user or not user.is_authenticated:
            return False

        # 2. Group Membership Check (Requirement: No group = No access)
        if not user.groups.exists():
            return False

        # 3. Get the model from the viewset
        # This makes the permission reusable for any model
        try:
            model_cls = view.get_queryset().model
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name
        except AttributeError:
            return False

        # 4. Map HTTP Methods to Django's default permission codenames
        # These are the permissions admin sees in the Admin Panel
        method_map = {
            'GET': 'view',
            'HEAD': 'view',
            'OPTIONS': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
        }

        permission_verb = method_map.get(request.method)
        if not permission_verb:
            return False

        # Construct the permission string (e.g., 'myapp.view_room')
        required_perm = f"{app_label}.{permission_verb}_{model_name}"

        # 5. Check Permissions
        # user.has_perm() automatically checks permissions granted through groups.
        # This is dynamic: if admin changes group perms, this returns False immediately.
        return user.has_perm(required_perm)