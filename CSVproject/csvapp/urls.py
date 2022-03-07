from django.urls import path, include
from .views import product_download, ProductViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register("product", ProductViewSet)
urlpatterns = [
    path('', include(router.urls))
]
# urlpatterns = [
#
#     path("csv-download", product_download, name='csv-download'),
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]
