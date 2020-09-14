from django.urls import include, path
from rest_framework import routers
from bucket import viewsets as restapis

router = routers.DefaultRouter()
router.register(r'todo', restapis.TodoViewset)
router.register(r'bucket', restapis.BucketViewset)
router.register(r'login', restapis.LoginViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]