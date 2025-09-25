from models import Attack, DeckCard


def combat_logic_service(attack: Attack, card_objetive: DeckCard):
    future_card_hp = card_objetive.current_hp - attack.power
    return future_card_hp