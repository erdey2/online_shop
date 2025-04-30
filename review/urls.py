from django.urls import include, path
from .views import ProductReviewList, ProductReviewDetail
urlpatterns = [
    path('review/', ProductReviewList.as_view(), name='products-review-list'),
    path('review/<uuid:pk>/', ProductReviewDetail.as_view(), name='products-review-detail')
]