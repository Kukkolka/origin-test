from rest_framework.permissions import BasePermission

class UserIsOwnerBond(BasePermission):

    def has_object_permission(self, request, view, bond):
        return request.user.id == bond.user.id
