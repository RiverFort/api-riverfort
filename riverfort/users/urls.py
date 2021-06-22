from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, VerifyEmail

app_name = 'users'

urlpatterns = [
  path('register/', CustomUserCreate.as_view(), name="create_user"),
  path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
  path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),
]