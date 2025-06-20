"""
URL configuration for TreanferMarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from django.contrib import admin
from django.urls import path
from TreanferMerket.views import (
    info_view, my_club, create_player_card, buy_player, transfer_market_view,
    UserRegisterView, UserLoginView, UserLogoutView, sell_player
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', info_view, name='info_view'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('my-club/', my_club, name='my_club'),
    path('api/create-player/', create_player_card, name='create_player'),
    path('buy/<int:listing_id>/', buy_player, name='buy_player'),
    path('market/', transfer_market_view, name='market_view'),
    path('sell-player/<int:player_id>/', sell_player, name='sell_player'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Для медиа-файлов
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)