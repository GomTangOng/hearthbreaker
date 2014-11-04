import hearthbreaker
from hearthbreaker.constants import MINION_TYPE
from hearthbreaker.effects.base import Condition


class HasSecret(Condition):
    def evaluate(self, target, *args):
        return len(target.player.secrets) > 0

    def __to_json__(self):
        return {
            'name': 'has_secret'
        }


class CardMatches(Condition):
    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def evaluate(self, target, card, *args):
        return self.selector.match(target, card)

    def __to_json__(self):
        return {
            'name': 'card_matches',
            'selector': self.selector,
        }

    def __from_json__(self, selector):
        selector = hearthbreaker.effects.selector.Selector.from_json(**selector)
        self.__init__(selector)
        return self


class MinionIsTarget(Condition):
    def evaluate(self, target, minion, *args):
        return minion is target

    def __to_json__(self):
        return {
            'name': 'minion_is_target'
        }


class MinionIsNotTarget(Condition):
    def evaluate(self, target, minion, *args):
        return minion is not target

    def __to_json__(self):
        return {
            'name': 'minion_is_not_target'
        }


class MinionIsType(Condition):
    def __init__(self, minion_type, include_self=False):
        super().__init__()
        self.minion_type = minion_type
        self.include_self = include_self

    def evaluate(self, target, minion, *args):
        if self.include_self or target is not minion:
            return minion.card.minion_type == self.minion_type
        return False

    def __to_json__(self):
        return {
            'name': 'minion_is_type',
            'include_self': self.include_self,
            'minion_type': MINION_TYPE.to_str(self.minion_type)
        }

    def __from_json__(self, minion_type, include_self=False):
        self.minion_type = MINION_TYPE.from_str(minion_type)
        self.include_self = include_self
        return self


class MinionHasDeathrattle(Condition):
    def __to_json__(self):
        return {
            'name': 'minion_has_deathrattle'
        }

    def __init__(self):
        super().__init__()

    def evaluate(self, target, minion, *args):
        return minion.deathrattle is not None


class Adjacent(Condition):
    def __to_json__(self):
        return {
            'name': 'adjacent'
        }

    def __init__(self):
        super().__init__()

    def evaluate(self, target, minion, *args):
        return minion.player is target.player and \
            (minion.index == target.index - 1) or (minion.index == target.index + 1)


class AttackLessThanOrEqualTo(Condition):
    def __init__(self, attack_max, include_self=False):
        super().__init__()
        self.attack_max = attack_max
        self.include_self = include_self

    def evaluate(self, target, minion, *args):
        return (self.include_self or target is not minion) and minion.calculate_attack() <= self.attack_max

    def __to_json__(self):
        return {
            'name': 'attack_less_than_or_equal_to',
            'include_self': self.include_self,
            'attack_max': self.attack_max
        }
