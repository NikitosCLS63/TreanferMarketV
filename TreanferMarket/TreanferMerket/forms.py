from django import forms
from .models import (
    Nation, League, Club, Position, Player, PlayerStat,
    ListingStatus, TransferListing, BidStatus, Bid,
    TransactionType, Transaction, UserSquad, SquadPosition,
    SBCDifficulty, SBC, SBCReward, SBCRequirement, RewardType
)
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'coins', 'club_name']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'coins', 'club_name']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class NationForm(forms.ModelForm):
    class Meta:
        model = Nation
        fields = ['name', 'flag_image_url']

class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'country', 'logo_url']

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'league', 'logo_url']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['code', 'name']

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'position', 'overall_rating', 'nation', 'club', 'base_price', 'rare', 'image_url']

class PlayerStatForm(forms.ModelForm):
    class Meta:
        model = PlayerStat
        fields = ['player', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality', 'weak_foot', 'skill_moves']

class ListingStatusForm(forms.ModelForm):
    class Meta:
        model = ListingStatus
        fields = ['name']

class TransferListingForm(forms.ModelForm):
    class Meta:
        model = TransferListing
        fields = ['player', 'seller', 'start_price', 'buy_now_price', 'duration', 'status']

class BidStatusForm(forms.ModelForm):
    class Meta:
        model = BidStatus
        fields = ['name']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['listing', 'bidder', 'amount', 'status']

class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = ['name']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user', 'player', 'price', 'type']

class UserSquadForm(forms.ModelForm):
    class Meta:
        model = UserSquad
        fields = ['user', 'name', 'formation', 'is_active']

class SquadPositionForm(forms.ModelForm):
    class Meta:
        model = SquadPosition
        fields = ['squad', 'player', 'position_type', 'position_order']

class SBCDifficultyForm(forms.ModelForm):
    class Meta:
        model = SBCDifficulty
        fields = ['name']

class SBCForm(forms.ModelForm):
    class Meta:
        model = SBC
        fields = ['name', 'description', 'difficulty', 'expiry_date', 'is_repeatable']

class SBCRewardForm(forms.ModelForm):
    class Meta:
        model = SBCReward
        fields = ['sbc', 'reward_type', 'value', 'probability']

class SBCRequirementForm(forms.ModelForm):
    class Meta:
        model = SBCRequirement
        fields = ['sbc', 'min_rating', 'max_players', 'nation', 'league', 'club']

class RewardTypeForm(forms.ModelForm):
    class Meta:
        model = RewardType
        fields = ['name']



class PlayerCreationForm(forms.ModelForm):
    pace = forms.IntegerField(min_value=1, max_value=99, required=True, label="Скорость")
    shooting = forms.IntegerField(min_value=1, max_value=99, required=True, label="Удары")
    passing = forms.IntegerField(min_value=1, max_value=99, required=True, label="Передачи")
    dribbling = forms.IntegerField(min_value=1, max_value=99, required=True, label="Дриблинг")
    defending = forms.IntegerField(min_value=1, max_value=99, required=True, label="Защита")
    physicality = forms.IntegerField(min_value=1, max_value=99, required=True, label="Физика")
    weak_foot = forms.IntegerField(min_value=1, max_value=5, required=True, label="Слабая нога")
    skill_moves = forms.IntegerField(min_value=1, max_value=5, required=True, label="Финты")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

        position_order = [
            'ST', 'CF', 'LW', 'RW', 'CAM', 'CM', 'CDM', 'LM', 'RM',
            'LWB', 'RWB', 'LB', 'RB', 'CB', 'GK'
        ]
        positions = sorted(Position.objects.all(), key=lambda p: position_order.index(p.code) if p.code in position_order else len(position_order))
        self.fields['position'].queryset = Position.objects.filter(pk__in=[p.pk for p in positions])


    class Meta:
        model = Player
        fields = [
            'name', 'position', 'overall_rating',
            'base_price', 'rare', 'image_file', 'player_flag_image', 'player_club_logo_image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'overall_rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'rare': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'image_file': forms.FileInput(attrs={'class': 'form-control'}),
            'player_flag_image': forms.FileInput(attrs={'class': 'form-control'}),
            'player_club_logo_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        player = super().save(commit=False)
        if self.user:
            player.owner = self.user
            player.created_by = self.user
        if commit:
            player.save()
            # Create or update PlayerStat
            PlayerStat.objects.update_or_create(
                player=player,
                defaults={
                    'pace': self.cleaned_data['pace'],
                    'shooting': self.cleaned_data['shooting'],
                    'passing': self.cleaned_data['passing'],
                    'dribbling': self.cleaned_data['dribbling'],
                    'defending': self.cleaned_data['defending'],
                    'physicality': self.cleaned_data['physicality'],
                    'weak_foot': self.cleaned_data['weak_foot'],
                    'skill_moves': self.cleaned_data['skill_moves'],
                }
            )
        return player

class SellPlayerForm(forms.ModelForm):
    class Meta:
        model = TransferListing
        fields = ['start_price', 'duration']
        widgets = {
            'start_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Стартовая цена'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Длительность в часах'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_price'].label = "Стартовая цена"
        self.fields['duration'].label = "Длительность (часы)"