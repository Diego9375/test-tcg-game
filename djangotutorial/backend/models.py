from django.db import models
from service.combat_service import combat_logic_service
import random


class Card(models.Model):
    name = models.CharField(max_length=30)
    hp = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to='cards')
    type = models.CharField(max_length=30)
    set = models.CharField(max_length=30, default="base_set")
    rarity = models.CharField(max_length=30, default="common")

    def __str__(self):
        return '{id}, {name}'.format(id=self.id, name=self.name)


class Attack(models.Model):
    name = models.CharField(max_length=30)
    power = models.IntegerField()
    cost = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return '{id}, {name}'.format(id=self.id, name=self.name)


class CardAttack(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    attack = models.ForeignKey(Attack, on_delete=models.CASCADE)

    def __str__(self):
        return '{card}, {attack}'.format(card=self.card, attack=self.attack)


class Collection(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    attack1 = models.ForeignKey(Attack, on_delete=models.CASCADE, related_name="attack1", default=2)
    attack2 = models.ForeignKey(Attack, on_delete=models.CASCADE, related_name="attack2", null=True, blank=True,
                                default=None)

    def __str__(self):
        return '{id}, {name}'.format(id=self.id, name=self.card)


class Player(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    telephone = models.IntegerField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

class Deck(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    def __str__(self):
        return '{id}, {name}'.format(id=self.player, name=self.name)

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    current_hp = models.IntegerField()

class Battle(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class Hand(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card)

    def num_cards(self):
        return len(self.cards)

class PlayerTurn(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_active_cards = models.ManyToManyField(Card, related_name="player_active_cards")
    bench_cards = models.ManyToManyField(Card, related_name="player_benched_cards")

    def action(self, decision, atk, card_objetive):
        if decision == 'pass':
            pass
        elif decision == 'attack':
            combat_logic_service(atk, card_objetive)
        elif decision == 'play_object':
            pass
        else:
            pass

class BattleStatus(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    turn = models.ForeignKey(PlayerTurn, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    active_cards = models.ManyToManyField(Card, related_name="active_cards") # limit 2
    bench_cards = models.ManyToManyField(Card, related_name="benched_cards") # limit 3
    num_cards = models.IntegerField()


class Booster(models.Model):
    name = models.CharField(max_length=30, default='Booster')

    def __str__(self):
        return '{id}, {name}'.format(id=self.id, name=self.name)

    def open_booster(self):
        card_list_common = Card.objects.filter(cardattack__isnull=False, rarity="common").distinct()
        card_list_rare = Card.objects.filter(cardattack__isnull=False, rarity="rare").distinct()
        for x in range(3):
            if x == 2:
                card_selected = random.choice(card_list_rare)

                attacks = CardAttack.objects.filter(card=card_selected)
                selected_attack1 = random.choice(attacks)
                selected_attack2 = random.choice(attacks)

                while selected_attack1 == selected_attack2:
                    selected_attack2 = random.choice(attacks)

                new_collection = Collection()
                new_collection.card = card_selected
                new_collection.attack1 = Attack.objects.filter(id=selected_attack1.attack.id).first()
                new_collection.attack2 = Attack.objects.filter(id=selected_attack2.attack.id).first()
                new_collection.save()
            else:
                card_selected = random.choice(card_list_common)

                attacks = CardAttack.objects.filter(card=card_selected)
                selected_attack1 = random.choice(attacks)
                selected_attack2 = random.choice(attacks)

                while selected_attack1 == selected_attack2:
                    selected_attack2 = random.choice(attacks)

                new_collection = Collection()
                new_collection.card = card_selected
                new_collection.attack1 = Attack.objects.filter(id=selected_attack1.attack.id).first()
                new_collection.attack2 = Attack.objects.filter(id=selected_attack2.attack.id).first()
                new_collection.save()

