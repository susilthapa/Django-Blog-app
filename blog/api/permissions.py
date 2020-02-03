from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this object"
    my_safe_method = ['GET', 'POST']

    # def has_permission(self, request, view):  # for views function i.e non-generic
    #     if request.method in self.my_safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):  # for generic views : for more see django-rest-framework docs
        if request.method in self.my_safe_method:  # we can also use if request.method in SAFE_METHODS: #(like in docs)
            return True
        return obj.author == request.user
