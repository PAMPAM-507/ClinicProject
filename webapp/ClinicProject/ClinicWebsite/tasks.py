import requests
import uuid
import json
import redis

# webauth - ClinicProject

from celery import shared_task
from ClinicProject.celery import app

from .utils.Redis.actionWithRedis import getFromRedis, setToRedis
from .utils.Redis.Redis import RedisClass
from ClinicProject.settings import URL_FUZZY_MODEL, CELERY_BROKER_URL, REDIS_PORT, REDIS_HOST
from .utils.Redis.actionWithRedis import getFromRedis, setToRedis

urlForAuth = URL_FUZZY_MODEL + 'api/token/'
urlForRedis = CELERY_BROKER_URL


@app.task
def register_to_model():
    r = requests.post(urlForAuth,
                      json={"username": "root", "password": "root"})
    data = r.text
    try:
        data_json = json.loads(data)
        with RedisClass(host=REDIS_HOST, port=REDIS_PORT) as redis_obj:
            setToRedis.SetKeyValue().set(redis_obj,
                                         'refresh', data_json.get('refresh'))
            setToRedis.SetKeyValue().set(redis_obj,
                                         'access', data_json.get('access'))
        print('We sign-in in model: ', json.loads(r.text))
    except json.JSONDecodeError:
        print("Empty response")
    except Exception as error:
        print("Error is ", error)


@app.task
def refresh_access_token():
    try:
        with RedisClass(host=REDIS_HOST, port=REDIS_PORT) as redis_obj:
            data = getFromRedis.GetByKey().get(redis_obj, 'refresh')

        data = data.decode("utf-8")

        if data and isinstance(data, str):
            r = requests.post(urlForAuth + 'refresh/', json={"refresh": str(data)})

            data_json = json.loads(r.text)

            with RedisClass(host=REDIS_HOST, port=REDIS_PORT) as redis_obj:
                setToRedis.SetKeyValue().set(redis_obj,
                                             'access',
                                             data_json.get('access'))

            print('We get new access token for model: ', data_json)

    except json.JSONDecodeError:
        print("Empty response")
    except Exception as error:
        if error == "'NoneType' object has no attribute 'decode'":
            print("Token is not exist now, probably it will made in future")
        print("Error is ", error)
