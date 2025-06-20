from django.contrib import admin
from .models import (
    Player, PlayerStat, Nation, Club, Position, League,
    ListingStatus, TransferListing, Bid, BidStatus,
    Transaction, TransactionType, CustomUser,
    UserSquad, SquadPosition,
    SBC, SBCReward, SBCRequirement,
    SBCDifficulty, RewardType 
)

class PlayerStatInline(admin.StackedInline):
         model = PlayerStat
         can_delete = False  

class PlayerAdmin(admin.ModelAdmin):
         inlines = [PlayerStatInline]
         list_display = ('name', 'overall_rating', 'position', 'club', 'nation', 'base_price')
         list_filter = ('position', 'club', 'nation')
         search_fields = ('name',)

class TransferListingAdmin(admin.ModelAdmin):
         list_display = ('player', 'start_price', 'buy_now_price', 'is_featured', 'status')
         list_filter = ('is_featured', 'status')
         search_fields = ('player__name',)

admin.site.register(Player, PlayerAdmin)
admin.site.register(TransferListing, TransferListingAdmin)
admin.site.register(Nation)
admin.site.register(Club)
admin.site.register(Position)
admin.site.register(League)
admin.site.register(ListingStatus)
admin.site.register(BidStatus)
admin.site.register(TransactionType)

admin.site.register(CustomUser)
admin.site.register(UserSquad)
admin.site.register(SquadPosition)
admin.site.register(SBC)
admin.site.register(SBCReward)
admin.site.register(SBCRequirement)
admin.site.register(SBCDifficulty)
admin.site.register(RewardType)


