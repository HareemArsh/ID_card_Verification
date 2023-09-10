from django.urls import path, include
from rest_framework import routers
from idcardapp import views

router = routers.DefaultRouter()
router.register(r'scanned-id-cards', views.ScannedIDCardViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/extract-id-card-info/', views.extract_id_card_info, name='extract_id_card_info'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # URL for the login page
    path('logout/', views.logout_view, name='logout'),  # URL for the logout page
    path('accounts/register/', views.register, name='register'),  # URL for the registration page
    path('', views.home, name='home'),  # Map the root URL to the home view
    # Add your other views/URL patterns here as needed
]
