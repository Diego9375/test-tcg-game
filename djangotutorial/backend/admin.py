from django.contrib import admin
from .models import Card, Attack, CardAttack, Booster, Collection


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(Attack)
class AttackAdmin(admin.ModelAdmin):
    pass


@admin.register(CardAttack)
class CardAttackAdmin(admin.ModelAdmin):
    pass

@admin.register(Booster)
class BoosterAdmin(admin.ModelAdmin):
    pass

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass