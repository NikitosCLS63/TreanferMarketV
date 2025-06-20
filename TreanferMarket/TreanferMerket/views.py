from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView, View
from .models import (
    Nation, League, Club, Position, Player, PlayerStat,
    ListingStatus, TransferListing, BidStatus, Bid,
    TransactionType, Transaction, UserSquad, SquadPosition,
    SBCDifficulty, SBC, SBCReward, SBCRequirement
)
from .forms import (
    NationForm, LeagueForm, ClubForm, PositionForm, PlayerForm, PlayerStatForm,
    ListingStatusForm, TransferListingForm, BidStatusForm, BidForm,
    TransactionTypeForm, TransactionForm, UserSquadForm, SquadPositionForm,
    SBCDifficultyForm, SBCForm, SBCRewardForm, SBCRequirementForm, PlayerCreationForm,
    CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, SellPlayerForm
)

from .models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView

import random
from django.utils import timezone


def info_view(request):
    return render(request, 'info.html')

# Регистрация
class UserRegisterView(TemplateView):
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomUserCreationForm()
        return context

# Вход
class UserLoginView(TemplateView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomAuthenticationForm()
        return context

# Выход
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# CRUD для пользователей
class UserListView(ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user_obj'

class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


class NationListView(ListView):
    model = Nation
    template_name = 'nation/nation_list.html'
    context_object_name = 'nations'

class NationDetailView(DetailView):
    model = Nation
    template_name = 'nation/nation_detail.html'
    context_object_name = 'nation'

class NationCreateView(CreateView):
    model = Nation
    form_class = NationForm
    template_name = 'nation/nation_form.html'
    success_url = reverse_lazy('nation_list_view')

class NationUpdateView(UpdateView):
    model = Nation
    form_class = NationForm
    template_name = 'nation/nation_form.html'
    success_url = reverse_lazy('nation_list_view')

class NationDeleteView(DeleteView):
    model = Nation
    template_name = 'nation/nation_confirm_delete.html'
    success_url = reverse_lazy('nation_list_view')


class LeagueListView(ListView):
    model = League
    template_name = 'league/league_list.html'
    context_object_name = 'leagues'

class LeagueDetailView(DetailView):
    model = League
    template_name = 'league/league_detail.html'
    context_object_name = 'league'

class LeagueCreateView(CreateView):
    model = League
    form_class = LeagueForm
    template_name = 'league/league_form.html'
    success_url = reverse_lazy('league_list_view')

class LeagueUpdateView(UpdateView):
    model = League
    form_class = LeagueForm
    template_name = 'league/league_form.html'
    success_url = reverse_lazy('league_list_view')

class LeagueDeleteView(DeleteView):
    model = League
    template_name = 'league/league_confirm_delete.html'
    success_url = reverse_lazy('league_list_view')


class ClubListView(ListView):
    model = Club
    template_name = 'club/club_list.html'
    context_object_name = 'clubs'

class ClubDetailView(DetailView):
    model = Club
    template_name = 'club/club_detail.html'
    context_object_name = 'club'

class ClubCreateView(CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'club/club_form.html'
    success_url = reverse_lazy('club_list_view')

class ClubUpdateView(UpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'club/club_form.html'
    success_url = reverse_lazy('club_list_view')

class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'club/club_confirm_delete.html'
    success_url = reverse_lazy('club_list_view')

class PositionListView(ListView):
    model = Position
    template_name = 'position/position_list.html'
    context_object_name = 'positions'

class PositionDetailView(DetailView):
    model = Position
    template_name = 'position/position_detail.html'
    context_object_name = 'position'

class PositionCreateView(CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'position/position_form.html'
    success_url = reverse_lazy('position_list_view')

class PositionUpdateView(UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'position/position_form.html'
    success_url = reverse_lazy('position_list_view')

class PositionDeleteView(DeleteView):
    model = Position
    template_name = 'position/position_confirm_delete.html'
    success_url = reverse_lazy('position_list_view')

class ListingStatusListView(ListView):
    model = ListingStatus
    template_name = 'listingstatus/listingstatus_list.html'
    context_object_name = 'statuses'

class ListingStatusCreateView(CreateView):
    model = ListingStatus
    form_class = ListingStatusForm
    template_name = 'listingstatus/listingstatus_form.html'
    success_url = reverse_lazy('listingstatus_list_view')

class ListingStatusUpdateView(UpdateView):
    model = ListingStatus
    form_class = ListingStatusForm
    template_name = 'listingstatus/listingstatus_form.html'
    success_url = reverse_lazy('listingstatus_list_view')

class ListingStatusDeleteView(DeleteView):
    model = ListingStatus
    template_name = 'listingstatus/listingstatus_confirm_delete.html'
    success_url = reverse_lazy('listingstatus_list_view')

# BidStatus CRUD
class BidStatusListView(ListView):
    model = BidStatus
    template_name = 'bidstatus/bidstatus_list.html'
    context_object_name = 'bidstatuses'

class BidStatusCreateView(CreateView):
    model = BidStatus
    form_class = BidStatusForm
    template_name = 'bidstatus/bidstatus_form.html'
    success_url = reverse_lazy('bidstatus_list_view')

class BidStatusUpdateView(UpdateView):
    model = BidStatus
    form_class = BidStatusForm
    template_name = 'bidstatus/bidstatus_form.html'
    success_url = reverse_lazy('bidstatus_list_view')

class BidStatusDeleteView(DeleteView):
    model = BidStatus
    template_name = 'bidstatus/bidstatus_confirm_delete.html'
    success_url = reverse_lazy('bidstatus_list_view')

# Player CRUD
class PlayerListView(ListView):
    model = Player
    template_name = 'player/player_list.html'
    context_object_name = 'players'

class PlayerDetailView(DetailView):
    model = Player
    template_name = 'player/player_detail.html'
    context_object_name = 'player'

class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'player/player_form.html'
    success_url = reverse_lazy('player_list_view')

class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'player/player_form.html'
    success_url = reverse_lazy('player_list_view')

class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'player/player_confirm_delete.html'
    success_url = reverse_lazy('player_list_view')

class PlayerStatUpdateView(UpdateView):
    model = PlayerStat
    form_class = PlayerStatForm
    template_name = 'playerstat/playerstat_form.html'
    success_url = reverse_lazy('player_list_view')


class TransferListingListView(ListView):
    model = TransferListing
    template_name = 'transferlisting/transferlisting_list.html'
    context_object_name = 'listings'

class TransferListingDetailView(DetailView):
    model = TransferListing
    template_name = 'transferlisting/transferlisting_detail.html'
    context_object_name = 'listing'

class TransferListingCreateView(CreateView):
    model = TransferListing
    form_class = TransferListingForm
    template_name = 'transferlisting/transferlisting_form.html'
    success_url = reverse_lazy('listing_list_view')

class TransferListingUpdateView(UpdateView):
    model = TransferListing
    form_class = TransferListingForm
    template_name = 'transferlisting/transferlisting_form.html'
    success_url = reverse_lazy('listing_list_view')

class TransferListingDeleteView(DeleteView):
    model = TransferListing
    template_name = 'transferlisting/transferlisting_confirm_delete.html'
    success_url = reverse_lazy('listing_list_view')


class BidListView(ListView):
    model = Bid
    template_name = 'bid/bid_list.html'
    context_object_name = 'bids'

class BidCreateView(CreateView):
    model = Bid
    form_class = BidForm
    template_name = 'bid/bid_form.html'
    success_url = reverse_lazy('bid_list_view')

# TransactionType CRUD
class TransactionTypeListView(ListView):
    model = TransactionType
    template_name = 'transactiontype/transactiontype_list.html'
    context_object_name = 'transactiontypes'

class TransactionTypeCreateView(CreateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'transactiontype/transactiontype_form.html'
    success_url = reverse_lazy('transactiontype_list_view')

class TransactionTypeUpdateView(UpdateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'transactiontype/transactiontype_form.html'
    success_url = reverse_lazy('transactiontype_list_view')

class TransactionTypeDeleteView(DeleteView):
    model = TransactionType
    template_name = 'transactiontype/transactiontype_confirm_delete.html'
    success_url = reverse_lazy('transactiontype_list_view')

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction/transaction_list.html'
    context_object_name = 'transactions'

class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction/transaction_form.html'
    success_url = reverse_lazy('transaction_list_view')

# UserSquad CRUD
class UserSquadListView(ListView):
    model = UserSquad
    template_name = 'usersquad/usersquad_list.html'
    context_object_name = 'squads'

class UserSquadCreateView(CreateView):
    model = UserSquad
    form_class = UserSquadForm
    template_name = 'usersquad/usersquad_form.html'
    success_url = reverse_lazy('usersquad_list_view')



@login_required
def create_player_card(request):
    # Обработка формы и отправка данных будет происходить через JavaScript на фронтенде.
    form = PlayerCreationForm(user=request.user) # Форма для отображения пустых полей
    return render(request, 'create_player.html', {'form': form})

@login_required
def my_club(request):
    created_players = Player.objects.filter(created_by=request.user).select_related('stats', 'position', 'nation', 'club')
    owned_players = Player.objects.filter(owner=request.user).select_related('stats', 'position', 'nation', 'club')

    # Отладка: Проверка наличия статистики
    print("Created Players:")
    for player in created_players:
        print(f"  Игрок: {player.name}, ID: {player.id}")
        if hasattr(player, 'stats'):
            print(f"    Статистика: Скорость={player.stats.pace}, Удары={player.stats.shooting}, Передачи={player.stats.passing}, Дриблинг={player.stats.dribbling}, Защита={player.stats.defending}, Физика={player.stats.physicality}, СлабаяНога={player.stats.weak_foot}, Финты={player.stats.skill_moves}")
        else:
            print("    Объект статистики не найден.")

    print("Owned Players:")
    for player in owned_players:
        print(f"  Игрок: {player.name}, ID: {player.id}")
        if hasattr(player, 'stats'):
            print(f"    Статистика: Скорость={player.stats.pace}, Удары={player.stats.shooting}, Передачи={player.stats.passing}, Дриблинг={player.stats.dribbling}, Защита={player.stats.defending}, Физика={player.stats.physicality}, СлабаяНога={player.stats.weak_foot}, Финты={player.stats.skill_moves}")
        else:
            print("    Объект статистики не найден.")

    return render(request, 'my_club.html', {'created_players': created_players, 'owned_players': owned_players, 'user_club_name': request.user.club_name})


@login_required
def buy_player(request, listing_id):
    listing = get_object_or_404(TransferListing, id=listing_id)
    if request.method == 'POST':
        if listing.buy_now_price and listing.status.name == 'Active':
            if request.user.coins >= listing.buy_now_price:
                
                listing.player.owner = request.user
                listing.player.save()
                
                request.user.coins -= listing.buy_now_price
                request.user.save()

                # Увеличение монет продавца
                seller_user = listing.seller
                seller_user.coins += listing.buy_now_price
                seller_user.save()

                listing.status = ListingStatus.objects.get(name='Sold')
                listing.save()
                
                Transaction.objects.create(
                    user=request.user,
                    player=listing.player,
                    price=listing.buy_now_price,
                    type=TransactionType.objects.get(name='Purchase')
                )
                return redirect('my_club')
            else:
                return render(request, 'error.html', {'message': 'Недостаточно монет для покупки'})
        else:
            return render(request, 'error.html', {'message': 'Листинг не активен или недоступен для покупки'})
    return render(request, 'confirm_purchase.html', {'listing': listing})


@login_required
def transfer_market_view(request):
    active_status = ListingStatus.objects.get(name='Active')
    active_listings = TransferListing.objects.filter(status=active_status).select_related('player__stats', 'player__position', 'player__nation', 'player__club')

    for listing in active_listings:
        time_since_last_update = timezone.now() - listing.last_price_update
        if time_since_last_update.total_seconds() > 60:  
            new_price = random.randint(50000, 100000000)
            listing.buy_now_price = new_price
            listing.last_price_update = timezone.now()
            listing.save()

    return render(request, 'transfer.html', {'listings': active_listings})

@login_required
def sell_player(request, player_id):
    player = get_object_or_404(Player, id=player_id, owner=request.user)
    form = SellPlayerForm() 
    return render(request, 'sell_player.html', {'form': form, 'player': player})