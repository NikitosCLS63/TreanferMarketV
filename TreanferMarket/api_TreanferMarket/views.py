
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as auth_login 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from TreanferMerket.models import (
    CustomUser, Nation, League, Club, Position, Player, PlayerStat,
    ListingStatus, TransferListing, BidStatus, Bid, TransactionType, Transaction,
    UserSquad, SquadPosition, SBCDifficulty, RewardType, SBC, SBCReward, SBCRequirement
)
from .serializers import (
    CustomUserSerializer, NationSerializer, LeagueSerializer, ClubSerializer, PositionSerializer, PlayerSerializer, PlayerStatSerializer,
    ListingStatusSerializer, TransferListingSerializer, BidStatusSerializer, BidSerializer, TransactionTypeSerializer, TransactionSerializer,
    UserSquadSerializer, SquadPositionSerializer, SBCDifficultySerializer, RewardTypeSerializer, SBCSerializer, SBCRewardSerializer, SBCRequirementSerializer
)
from .permissions import IsOwnerOrReadOnly



class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        auth_login(request, user) # Явно входим в Django-сессию
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'club_name': user.club_name, 
            'coins': user.coins,
            'created_at': user.created_at,
        })

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

class NationViewSet(viewsets.ModelViewSet):
    queryset = Nation.objects.all()
    serializer_class = NationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsOwnerOrReadOnly]

class PlayerStatViewSet(viewsets.ModelViewSet):
    queryset = PlayerStat.objects.all()
    serializer_class = PlayerStatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ListingStatusViewSet(viewsets.ModelViewSet):
    queryset = ListingStatus.objects.all()
    serializer_class = ListingStatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TransferListingViewSet(viewsets.ModelViewSet):
    queryset = TransferListing.objects.all()
    serializer_class = TransferListingSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [IsOwnerOrReadOnly]
        return super().get_permissions()

    def get_queryset(self):
        queryset = TransferListing.objects.all()

        player_name = self.request.query_params.get('player_name', None)
        min_rating = self.request.query_params.get('min_rating', None)
        position_code = self.request.query_params.get('position', None)

        if player_name:
            queryset = queryset.filter(player__name__icontains=player_name)
        if min_rating:
            queryset = queryset.filter(player__overall_rating__gte=min_rating)
        if position_code:
            queryset = queryset.filter(player__position__code=position_code)

        return queryset

    def perform_create(self, serializer):
        
        active_status, created = ListingStatus.objects.get_or_create(name='Active')
        serializer.save(seller=self.request.user, status=active_status)

class BidStatusViewSet(viewsets.ModelViewSet):
    queryset = BidStatus.objects.all()
    serializer_class = BidStatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)

class TransactionTypeViewSet(viewsets.ModelViewSet):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class UserSquadViewSet(viewsets.ModelViewSet):
    queryset = UserSquad.objects.all()
    serializer_class = UserSquadSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SquadPositionViewSet(viewsets.ModelViewSet):
    queryset = SquadPosition.objects.all()
    serializer_class = SquadPositionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SBCDifficultyViewSet(viewsets.ModelViewSet):
    queryset = SBCDifficulty.objects.all()
    serializer_class = SBCDifficultySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RewardTypeViewSet(viewsets.ModelViewSet):
    queryset = RewardType.objects.all()
    serializer_class = RewardTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SBCViewSet(viewsets.ModelViewSet):
    queryset = SBC.objects.all()
    serializer_class = SBCSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SBCRewardViewSet(viewsets.ModelViewSet):
    queryset = SBCReward.objects.all()
    serializer_class = SBCRewardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SBCRequirementViewSet(viewsets.ModelViewSet):
    queryset = SBCRequirement.objects.all()
    serializer_class = SBCRequirementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
