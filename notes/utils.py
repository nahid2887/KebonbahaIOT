from rest_framework.permissions import BasePermission
from accounts.models import SharedAccess

class HasSharedAccessOrOwner(BasePermission):
    """
    Allows access if the authenticated user is the owner or
    has been granted shared access by the owner (target_user_id).
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Assumes the view is retrieving an object tied to a user.
        You can adapt this as needed (e.g. if `obj.user.id` or `obj.owner.id`)
        """
        target_user_id = getattr(obj, 'user_id', None) or getattr(obj, 'owner_id', None)

        if not target_user_id:
            return False

        # Allow if the authenticated user is the owner or has shared access
        return request.user.id == target_user_id or SharedAccess.objects.filter(
            owner_id=target_user_id,
            viewer=request.user,
            status='accepted'  # only accepted shares
        ).exists()