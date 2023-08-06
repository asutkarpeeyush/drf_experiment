from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasUpdatedOrNoOwner(BasePermission):
    # Only show details entries that have been updated by the requester
    # or donot have any update_by

    def has_permission(self, request, view):
        # can be used for list views
        print(f"request auth {request.auth}")
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        # can be used for permissions on specific objects.
        print(f"request auth {request.auth}")
        if request.method in SAFE_METHODS:
            return True

        if not obj.updated_by:
            return True
        elif obj.updated_by != request.user:
            return False

        return True