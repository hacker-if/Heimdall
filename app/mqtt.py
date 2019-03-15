from app import app, mqtt, db
from models import User, LogPorta
from time import time

# bibliotecas para altenticação das mensagem
from hashlib import blake2s
from hmac import compare_digest
from base64 import b64encode, b64decode


# Incrição nos tópicos
@mqtt.on_connect()
def mqtt_connect(client, userdata, flags, rc):
    mqtt.subscribe(app.config['MQTT_IN_TOPIC'])


# Callback
# aberto.31135435$...
# id:1,token:Av3DF3d.313535$...
@mqtt.on_message()
def mqtt_message(client, userdata, message):
    if check_payload(message.payload.decode()):
        status = 'MQTT CHECK'
        msg, temp = message.payload.decode().split('.')
        if abs(temp - time()) < 10:
            data = {}
            for x in msg.split(':'):
                cmd = x.split(',')
                if len(cmd) == 1:
                    data[cmd[0]] = None
                else:
                    data[cmd[0]] = cmd[1]

            if 'aberto' in data:
                log = LogPorta(msg='Porta aberta')
                db.session.add(log)
                db.session.commit()

            elif 'id' in data and data['id'] is not None\
                 and 'uid' in data and data['uid'] is not None:
                id = int(data['id'])
                user = User.query.get(id)
                user.token = data['uid']
                db.session.commit()

            elif 'uid' in data and data['uid'] is not None:
                user = User.query.filter_by(token=data['uid']).first()
                if user is not None:
                    payload = form_payload('abrir')
                    mqtt.publish(app.config['MQTT_OUT_TOPIC'], payload)

    else:
        status = 'MQTT FALURE'
    print(status, message.topic, message.payload.decode())

def send(msg):
    payload = form_payload('liberar.{}'.format(round(time())))
    mqtt.publish(app.config['MQTT_OUT_TOPIC'], payload)

def activate_door_request():
    send('liberar')

def add_token_request(id):
    msg = 'id:{}'.format(id)
    send(msg)

def open_door_request():
    send('abrir')

# Gera assinatura
def sign(msg, b64=False):
    s = blake2s(msg.encode(), key=app.config['MQTT_KEY'].encode(), digest_size=16).digest()
    if b64:
        s = b64encode(s)
    return s


# Gera payload, concatenando a mensagem e a assinatura em um string em base64
def form_payload(msg):
    return msg + '$' + sign(msg, b64=True).decode()


# Checa se o payload é válido
def check_payload(payload):
    msg, test = payload.split('$')
    test = b64decode(test)
    valid = sign(app.config['MQTT_KEY'], msg)
    return compare_digest(test, valid)
