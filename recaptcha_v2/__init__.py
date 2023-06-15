from otree.api import *

# RECAPTCHA
import requests
from otree.settings import RECAPTCHA_SECRET_KEY, RECAPTCHA_SITE_KEY


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'recaptcha_v2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    is_human = models.BooleanField(initial=False)


# PAGES
class MyPage(Page):
    def vars_for_template(player: Player):
        return {
            "RECAPTCHA_SITE_KEY": RECAPTCHA_SITE_KEY
        }

    def live_method(player: Player, data):
        if recaptcha_valid(data["response_token"]):
            player.is_human = True

    @staticmethod
    def error_message(player, values):
        if not player.is_human:
            return 'You did not solve the captcha.'


class Results(Page):
    pass


def recaptcha_valid(response_token):
    res = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret': RECAPTCHA_SECRET_KEY,
        'response': response_token
    })
    return res.json()["success"]


page_sequence = [MyPage, Results]
