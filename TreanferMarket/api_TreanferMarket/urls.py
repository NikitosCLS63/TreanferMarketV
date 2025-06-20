from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet, NationViewSet, LeagueViewSet, ClubViewSet, PositionViewSet, PlayerViewSet,
    PlayerStatViewSet, ListingStatusViewSet, TransferListingViewSet, BidStatusViewSet, BidViewSet,
    TransactionTypeViewSet, TransactionViewSet, UserSquadViewSet, SquadPositionViewSet,
    SBCDifficultyViewSet, RewardTypeViewSet, SBCViewSet, SBCRewardViewSet, SBCRequirementViewSet,
    LoginAPIView
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'nations', NationViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'clubs', ClubViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'player-stats', PlayerStatViewSet)
router.register(r'listing-statuses', ListingStatusViewSet)
router.register(r'transfer-listings', TransferListingViewSet)
router.register(r'bid-statuses', BidStatusViewSet)
router.register(r'bids', BidViewSet)
router.register(r'transaction-types', TransactionTypeViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'user-squads', UserSquadViewSet)
router.register(r'squad-positions', SquadPositionViewSet)
router.register(r'sbc-difficulties', SBCDifficultyViewSet)
router.register(r'reward-types', RewardTypeViewSet)
router.register(r'sbcs', SBCViewSet)
router.register(r'sbc-rewards', SBCRewardViewSet)
router.register(r'sbc-requirements', SBCRequirementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='api_login'),
]

