# reCAPTCHA v2 for oTree 5

This is an example integration of reCAPTCHA v2 into oTree 5.10.3.
The implementation includes server-side validation of the user's response and presents a form error if the user did not solve the captcha (correctly).

## Setup
- sign up for [reCAPTCHA](https://www.google.com/recaptcha/)
    - select V2 with otherwise default options 
    - make sure to add ```herokuapp.com``` as the domain if you intend to use it with Heroku as your hosting provider.
    - for development, also add ```localhost```

- add ```requests``` to the requirements.txt
- install: ```pip install -r requirements.txt```"


## Usage
Add the credentials to your ``settings.py``. You get them as part of the sign up process to reCAPTCHA.
```python
# settings.py
RECAPTCHA_SITE_KEY = "MyRecaptchaSiteKey123"
RECAPTCHA_SECRET_KEY = "MyRecaptchaSecretKey456"
```

Better yet, use environmental variables (on heroku):
```python
# settings.py
RECAPTCHA_SITE_KEY = environ.get('RECAPTCHA_SITE_KEY', '')
RECAPTCHA_SECRET_KEY = environ.get('RECAPTCHA_SECRET_KEY', '')
```

Add the necessary import statements at the top of your ``__init__.py``:
```python
# __init__.py
import requests
from otree.settings import RECAPTCHA_SECRET_KEY, RECAPTCHA_SITE_KEY
```

Add a field to your player model:
```python
# __init__.py
class Player(BasePlayer):
    is_human = models.BooleanField(initial=False)
```

On the page that you want to use reCAPTCHA, add the following code to send the ``RECAPTCHA_SITE_KEY`` to the template, handle captcha validation, and show an error message if needed:
```python
# __init__.py
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
```

Add the referenced ``recaptcha_valid()`` function.
```python
# __init__.py
def recaptcha_valid(response_token):
    res = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret': RECAPTCHA_SECRET_KEY,
        'response': response_token
    })
    return res.json()["success"]
```

On the template for the page, add the following code to the ``content block`` to render the captcha:
```html
<!-- place in content block, where all formfields live -->
<div class="g-recaptcha" data-sitekey="{{ RECAPTCHA_SITE_KEY }}" data-callback="verify_token"></div>
``` 

And finally add the following scripts to the same template:
```javascript
{{ block scripts }}
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
    <script>
         function verify_token(response_token) {
             liveSend({'response_token': response_token});
         }
    </script>
{{ endblock }}
```
