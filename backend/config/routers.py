from rest_framework.routers import DefaultRouter


from users.viewsets import UserViewSet

router = DefaultRouter()


router.register("users", UserViewSet, basename="users")
