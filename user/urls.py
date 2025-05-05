from django.urls import path
from .views import UserList, UserDetail, LoginView

urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
]