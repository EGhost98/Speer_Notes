from django.urls import path
from .views import RegisterView, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegisterView.as_view(), name="sign_up"),
    path('logout/', LogoutView.as_view(), name="logout"),
]