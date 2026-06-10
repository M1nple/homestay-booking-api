from rest_framework.permissions import BasePermission

# kiểm tra user có phải là admin hay không
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'ADMIN'
        ) 
    
# kiểm tra user có phải là host hay không 
class IsHost(BasePermission):
    def has_permission(self, request, view):
        # print("USER:", request.user)
        # print("ROLE:", request.user.role)
        return(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'HOST'
        )
