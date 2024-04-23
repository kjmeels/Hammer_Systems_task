from rest_framework.routers import DefaultRouter


from users.viewsets import AuthenticationViewSet

router = DefaultRouter()


router.register("users", AuthenticationViewSet, basename="users")
