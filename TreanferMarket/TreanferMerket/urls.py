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





