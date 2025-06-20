import random
from django.db.models import F
from TreanferMerket.models import TransferListing, ListingStatus

def update_listing_prices():
    """Обновляет цены активных трансферных предложений случайным образом.
    Цены будут варьироваться от 50,000 до 100,000,000.
    """
    active_status = ListingStatus.objects.get(name='Active')
    listings = TransferListing.objects.filter(status=active_status)

    for listing in listings:
        # Генерируем новую случайную цену от 50,000 до 100,000,000
        new_price = random.randint(50000, 100000000)
        listing.buy_now_price = new_price
        listing.save()
        print(f"Цена для {listing.player.name} обновлена до {new_price} монет.") 