from rest_framework import serializers
from TreanferMerket.models import (
    CustomUser, Nation, League, Club, Position, Player,
    PlayerStat, ListingStatus, TransferListing, BidStatus, Bid,
    TransactionType, Transaction, UserSquad, SquadPosition,
    SBCDifficulty, RewardType, SBC, SBCReward, SBCRequirement
)

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'coins', 'club_name', 'created_at', 'password', 'is_staff')
        read_only_fields = ('created_at', 'is_staff')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
            
        )
        user.coins = validated_data.get('coins', 0)
        user.save()
        return user

    def validate_username(self, value):
        if value.lower() == 'admin':
            raise serializers.ValidationError("Имя пользователя «admin» не допускается")
        return value

class NationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = '__all__'

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'

class ClubSerializer(serializers.ModelSerializer):
    nation = serializers.StringRelatedField(read_only=True)
    league = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Club
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class PlayerStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStat
        fields = ('pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality', 'weak_foot', 'skill_moves')

class PlayerSerializer(serializers.ModelSerializer):
    club = serializers.StringRelatedField(read_only=True)
    nation = serializers.StringRelatedField(read_only=True)
    position = serializers.StringRelatedField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    player_image = serializers.ImageField(required=False, allow_empty_file=True)
    player_flag_image = serializers.ImageField(required=False, allow_empty_file=True)
    player_club_logo_image = serializers.ImageField(required=False, allow_empty_file=True)

    # Поля статистики, которые будут извлекаться вручную
    pace = serializers.IntegerField(required=False)
    shooting = serializers.IntegerField(required=False)
    passing = serializers.IntegerField(required=False)
    dribbling = serializers.IntegerField(required=False)
    defending = serializers.IntegerField(required=False)
    physicality = serializers.IntegerField(required=False)
    weak_foot = serializers.IntegerField(required=False)
    skill_moves = serializers.IntegerField(required=False)

    class Meta:
        model = Player
        fields = (
            'id', 'name', 'position', 'overall_rating', 'nation', 'club', 
            'base_price', 'rare', 'image_url', 'image_file', 
            'player_image', 'player_flag_image', 'player_club_logo_image', 
            'created_at', 'purchase_count', 'created_by', 'owner',
            
            'pace', 'shooting', 'passing', 'dribbling', 
            'defending', 'physicality', 'weak_foot', 'skill_moves'
        )

    def create(self, validated_data):
        stat_fields = [
            'pace', 'shooting', 'passing', 'dribbling', 
            'defending', 'physicality', 'weak_foot', 'skill_moves'
        ]
        stats_data = {field: validated_data.pop(field) for field in stat_fields if field in validated_data}

       
        request = self.context.get('request', None)
        print(f"DEBUG: Request user in PlayerSerializer.create: {request.user}")
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['owner'] = request.user
            print(f"DEBUG: Setting created_by and owner to: {request.user.username}")
        else:
            print("DEBUG: Request user is not authenticated or request context not available.")

        player = Player.objects.create(**validated_data)
        PlayerStat.objects.create(player=player, **stats_data)
        print(f"DEBUG: Player created: {player.name}, created_by: {player.created_by}, owner: {player.owner}")
        return player

    def update(self, instance, validated_data):
        stat_fields = [
            'pace', 'shooting', 'passing', 'dribbling', 
            'defending', 'physicality', 'weak_foot', 'skill_moves'
        ]
        stats_data = {field: validated_data.pop(field) for field in stat_fields if field in validated_data}

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if stats_data:
            player_stat, created = PlayerStat.objects.get_or_create(player=instance)
            for attr, value in stats_data.items():
                setattr(player_stat, attr, value)
            player_stat.save()

        return instance

class ListingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingStatus
        fields = '__all__'

class TransferListingSerializer(serializers.ModelSerializer):
    
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())

    class Meta:
        model = TransferListing
        
        fields = (
            'player', 'start_price', 'buy_now_price', 
            'duration',
        )
        
        
        read_only_fields = (
            'id', 'start_time', 'last_price_update', 'bid_count', 
            'current_bid', 'highest_bidder', 'seller', 'status'
        )

   
    def to_representation(self, instance):
        representation = super().to_representation(instance)
       
        representation['player'] = PlayerSerializer(instance.player, context=self.context).data
        representation['seller'] = str(instance.seller)
        representation['status'] = str(instance.status)
        return representation

class BidStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidStatus
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    listing = TransferListingSerializer(read_only=True)
    bidder = serializers.StringRelatedField(read_only=True)
    status = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = '__all__'

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    bid = serializers.StringRelatedField(read_only=True)
    transaction_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

class UserSquadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserSquad
        fields = '__all__'

class SquadPositionSerializer(serializers.ModelSerializer):
    squad = UserSquadSerializer(read_only=True)
    player = PlayerSerializer(read_only=True)
    position = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SquadPosition
        fields = '__all__'

class SBCDifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = SBCDifficulty
        fields = '__all__'

class RewardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardType
        fields = '__all__'

class SBCSerializer(serializers.ModelSerializer):
    difficulty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SBC
        fields = '__all__'

class SBCRewardSerializer(serializers.ModelSerializer):
    sbc = SBCSerializer(read_only=True)
    reward_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SBCReward
        fields = '__all__'

class SBCRequirementSerializer(serializers.ModelSerializer):
    sbc = SBCSerializer(read_only=True)
    nation = serializers.StringRelatedField(read_only=True)
    league = serializers.StringRelatedField(read_only=True)
    club = serializers.StringRelatedField(read_only=True)
    position = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SBCRequirement
        fields = '__all__'
