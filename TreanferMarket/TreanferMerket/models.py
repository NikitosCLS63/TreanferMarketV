from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Пользователи"""
    coins = models.PositiveIntegerField(default=0, verbose_name="Монеты")
    club_name = models.CharField(max_length=50, blank=True, verbose_name="Название клуба")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  
        blank=True,
        help_text='Группы, к которым принадлежит пользователь.',
        verbose_name='группы'
    )

    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', 
        blank=True,
        help_text='Конкретные разрешения для этого пользователя.',
        verbose_name='разрешения пользователя'
    )

    def __str__(self):
        return self.username


class Nation(models.Model):
    """Страны игроков"""
    name = models.CharField(max_length=50, verbose_name="Название страны")
    flag_image_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Флаг страны")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class League(models.Model):
    """Футбольные лиги"""
    name = models.CharField(max_length=50,unique=True, verbose_name="Название лиги")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна лиги")
    logo_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Логотип лиги")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Лига"
        verbose_name_plural = "Лиги"


class Club(models.Model):
    """Футбольные клубы"""
    name = models.CharField(max_length=50,unique=True, verbose_name="Название клуба")
    league = models.ForeignKey(League, on_delete=models.PROTECT, verbose_name="Лига")
    logo_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Логотип клуба")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"


class Position(models.Model):
    """Игровые позиции (GK, CB, ST и т.д.)"""
    code = models.CharField(max_length=3, verbose_name="Код позиции")
    name = models.CharField(max_length=30, verbose_name="Название позиции")

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"


class Player(models.Model):
    """Футбольные игроки"""
    name = models.CharField(max_length=50, verbose_name="Имя игрока")
    position = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name="Позиция", null=True, blank=True)
    overall_rating = models.PositiveSmallIntegerField(verbose_name="Общий рейтинг")
    nation = models.ForeignKey(Nation, on_delete=models.PROTECT, verbose_name="Страна", null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, verbose_name="Клуб", null=True, blank=True)
    base_price = models.PositiveIntegerField(verbose_name="Базовая цена")
    rare = models.BooleanField(default=False, verbose_name="Редкий игрок")
    image_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Фото игрока (URL)")
    image_file = models.ImageField(upload_to='players/', null=True, blank=True, verbose_name="Загруженное фото игрока")
    player_flag_image = models.ImageField(upload_to='player_flags/', null=True, blank=True, verbose_name="Загруженное фото флага")
    player_club_logo_image = models.ImageField(upload_to='player_club_logos/', null=True, blank=True, verbose_name="Загруженное фото логотипа клуба")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    purchase_count = models.PositiveIntegerField(default=0, verbose_name="Количество покупок")
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_players',
        verbose_name="Создано пользователем"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_players',
        verbose_name="Владелец"
    )

    def __str__(self):
        return f"{self.name} ({self.overall_rating})"

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"


class PlayerStat(models.Model):
    """Характеристики игроков"""
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='stats', verbose_name="Игрок")
    pace = models.PositiveSmallIntegerField(verbose_name="Скорость")
    shooting = models.PositiveSmallIntegerField(verbose_name="Удары")
    passing = models.PositiveSmallIntegerField(verbose_name="Передачи")
    dribbling = models.PositiveSmallIntegerField(verbose_name="Дриблинг")
    defending = models.PositiveSmallIntegerField(verbose_name="Защита")
    physicality = models.PositiveSmallIntegerField(verbose_name="Физика")
    weak_foot = models.PositiveSmallIntegerField(verbose_name="Слабая нога")
    skill_moves = models.PositiveSmallIntegerField(verbose_name="Финты")

    def __str__(self):
        return f"Характеристики {self.player.name}"

    class Meta:
        verbose_name = "Характеристика игрока"
        verbose_name_plural = "Характеристики игроков"


class ListingStatus(models.Model):
    """Статусы трансферных предложений"""
    name = models.CharField(max_length=20, verbose_name="Название статуса")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус листинга"
        verbose_name_plural = "Статусы листингов"


class TransferListing(models.Model):
    """Трансферные предложения (аукционы)"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Игрок")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings', verbose_name="Продавец")
    start_price = models.PositiveIntegerField(verbose_name="Стартовая цена")
    buy_now_price = models.PositiveIntegerField(blank=True, null=True, verbose_name="Цена выкупа")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Время начала")
    duration = models.PositiveIntegerField(verbose_name="Длительность (часы)")
    last_price_update = models.DateTimeField(auto_now_add=True, verbose_name="Время последнего обновления цены")
    bid_count = models.PositiveIntegerField(default=0, verbose_name="Количество ставок")
    current_bid = models.PositiveIntegerField(blank=True, null=True, verbose_name="Текущая ставка")
    highest_bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='leading_bids',
        verbose_name="Лидер ставок"
    )
    status = models.ForeignKey(ListingStatus, on_delete=models.PROTECT, verbose_name="Статус")
    is_featured = models.BooleanField(default=False, verbose_name="Горячее предложение")

    def __str__(self):
        return f"{self.player.name} - {self.status.name}"

    class Meta:
        verbose_name = "Трансферное предложение"
        verbose_name_plural = "Трансферные предложения"


class BidStatus(models.Model):
    """Статусы ставок"""
    name = models.CharField(max_length=20, verbose_name="Название статуса")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус ставки"
        verbose_name_plural = "Статусы ставок"


class Bid(models.Model):
    """Ставки на трансферных предложениях"""
    listing = models.ForeignKey(TransferListing, on_delete=models.CASCADE, related_name='bids', verbose_name="Предложение")
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Ставщик")
    amount = models.PositiveIntegerField(verbose_name="Сумма ставки")
    bid_time = models.DateTimeField(auto_now_add=True, verbose_name="Время ставки")
    status = models.ForeignKey(BidStatus, on_delete=models.PROTECT, verbose_name="Статус")

    def __str__(self):
        return f"{self.bidder.username} - {self.amount} на {self.listing.player.name}"

    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"


class TransactionType(models.Model):
    """Типы транзакций"""
    name = models.CharField(max_length=20, verbose_name="Название типа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип транзакции"
        verbose_name_plural = "Типы транзакций"


class Transaction(models.Model):
    """Финансовые транзакции"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    player = models.ForeignKey(Player, on_delete=models.PROTECT, verbose_name="Игрок")
    price = models.PositiveIntegerField(verbose_name="Сумма")
    type = models.ForeignKey(TransactionType, on_delete=models.PROTECT, verbose_name="Тип")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата транзакции")

    def __str__(self):
        return f"{self.user.username} - {self.type.name} - {self.price}"

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"


class UserSquad(models.Model):
    """Составы пользователей"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='squads', verbose_name="Пользователь")
    name = models.CharField(max_length=50, verbose_name="Название состава")
    formation = models.CharField(max_length=10, default='4-3-3', verbose_name="Схема")
    is_active = models.BooleanField(default=False, verbose_name="Активный состав")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    class Meta:
        verbose_name = "Состав пользователя"
        verbose_name_plural = "Составы пользователей"


class SquadPosition(models.Model):
    """Позиции в составе пользователя"""
    squad = models.ForeignKey(UserSquad, on_delete=models.CASCADE, related_name='positions', verbose_name="Состав")
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Игрок")
    position_type = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name="Тип позиции")
    position_order = models.PositiveSmallIntegerField(verbose_name="Порядок позиции")

    def __str__(self):
        player_name = self.player.name if self.player else "Пусто"
        return f"{self.squad.name} - {self.position_type} - {player_name}"

    class Meta:
        verbose_name = "Позиция в составе"
        verbose_name_plural = "Позиции в составах"


class SBCDifficulty(models.Model):
    """Уровни сложности SBC"""
    name = models.CharField(max_length=20, verbose_name="Название сложности")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сложность SBC"
        verbose_name_plural = "Сложности SBC"


class RewardType(models.Model):
    """Типы наград"""
    name = models.CharField(max_length=20, verbose_name="Тип награды")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип награды"
        verbose_name_plural = "Типы наград"


class SBC(models.Model):
    """SBC (Squad Building Challenges)"""
    name = models.CharField(max_length=100, verbose_name="Название SBC")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    difficulty = models.ForeignKey(SBCDifficulty, on_delete=models.PROTECT, verbose_name="Сложность")
    expiry_date = models.DateTimeField(verbose_name="Дата окончания")
    is_repeatable = models.BooleanField(default=False, verbose_name="Повторяемый")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "SBC"
        verbose_name_plural = "SBC"


class SBCReward(models.Model):
    """Награды за выполнение SBC"""
    sbc = models.ForeignKey(SBC, on_delete=models.CASCADE, related_name='rewards', verbose_name="SBC")
    reward_type = models.ForeignKey(RewardType, on_delete=models.PROTECT, verbose_name="Тип награды")
    value = models.PositiveIntegerField(verbose_name="Значение")
    probability = models.FloatField(default=1.0, verbose_name="Вероятность")

    def __str__(self):
        return f"{self.sbc.name} - {self.reward_type.name}"

    class Meta:
        verbose_name = "Награда SBC"
        verbose_name_plural = "Награды SBC"


class SBCRequirement(models.Model):
    """Требования для SBC"""
    sbc = models.ForeignKey(SBC, on_delete=models.CASCADE, related_name='requirements', verbose_name="SBC")
    min_rating = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Мин. рейтинг")
    max_players = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Макс. игроков")
    nation = models.ForeignKey(Nation, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Нация")
    league = models.ForeignKey(League, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Лига")
    club = models.ForeignKey(Club, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Клуб")

    def __str__(self):
        return f"Требование для {self.sbc.name}"

    class Meta:
        verbose_name = "Требование SBC"
        verbose_name_plural = "Требования SBC"
