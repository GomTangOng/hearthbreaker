import hearthbreaker.cards
from hearthbreaker.constants import CHARACTER_CLASS, CARD_RARITY
from hearthbreaker.effects.action import ChangeAttack, Freeze, ChangeHealth, ManaChange
from hearthbreaker.effects.aura import ManaAura
from hearthbreaker.effects.base import NewEffect, Aura
from hearthbreaker.effects.condition import HasSecret
from hearthbreaker.effects.event import SpellCast, DidDamage, TurnEnded
from hearthbreaker.effects.minion import AddCard
from hearthbreaker.effects.selector import SecretSelector, SpellSelector, PlayerSelector, SelfSelector, TargetSelector
from hearthbreaker.game_objects import MinionCard, Minion


class ManaWyrm(MinionCard):
    def __init__(self):
        super().__init__("Mana Wyrm", 1, CHARACTER_CLASS.MAGE, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 3, effects=[NewEffect(SpellCast(), ChangeAttack(1), SelfSelector())])


class SorcerersApprentice(MinionCard):
    def __init__(self):
        super().__init__("Sorcerer's Apprentice", 2, CHARACTER_CLASS.MAGE, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(3, 2, auras=[Aura(ManaChange(1, 0, SpellSelector()), PlayerSelector())])


class KirinTorMage(MinionCard):
    def __init__(self):
        super().__init__("Kirin Tor Mage", 3, CHARACTER_CLASS.MAGE, CARD_RARITY.RARE)

    def create_minion(self, player):
        def first_secret_cost_zero(m):
            m.player.add_aura(ManaAura(100, 0, SecretSelector(), True))

        return Minion(4, 3, battlecry=first_secret_cost_zero)


class EtherealArcanist(MinionCard):
    def __init__(self):
        super().__init__("Ethereal Arcanist", 4, CHARACTER_CLASS.MAGE, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(3, 3, effects=[NewEffect(TurnEnded(HasSecret()), ChangeAttack(2), SelfSelector()),
                                     NewEffect(TurnEnded(HasSecret()), ChangeHealth(2), SelfSelector())])


class WaterElemental(MinionCard):
    def __init__(self):
        super().__init__("Water Elemental", 4, CHARACTER_CLASS.MAGE, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(3, 6, effects=[NewEffect(DidDamage(), Freeze(), TargetSelector())])


class ArchmageAntonidas(MinionCard):
    def __init__(self):
        super().__init__("Archmage Antonidas", 7, CHARACTER_CLASS.MAGE, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(5, 7, effects=[AddCard("played", hearthbreaker.cards.Fireball, "spell", "owner")])
