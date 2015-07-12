import requests


def turn_lights_on():
    requests.post(
        "https://api.particle.io/v1/devices/cowhow0/blink",
        data={
            'access_token': '8ace38caf13cdb4520b3a3149bb2f0537b6a5e2c',
        }
    )
