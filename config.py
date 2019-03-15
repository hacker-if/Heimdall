import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    # Básico
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = os.environ.get('DEBUG') or True

    # Banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # E-mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "localhost"
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@example.com']

    # MQTT
    MQTT_BROKER_URL =  os.environ.get('MQTT_BROKER_URL') or 'broker.hivemq.com'  # use the free broker from HIVEMQ
    MQTT_BROKER_PORT = 1883  # default port for non-tls connection
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME') or ''  # set the username here if you need on for the broker
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD') or ''  # set the password here if the broker demands on
    MQTT_KEEPALIVE = 5  # set the time interval for sending a ping to the seconds
    MQTT_TLS_ENABLED = False  # set TLS to disabled for testing purposes
    MQTT_IN_TOPIC = os.environ.get('MQTT_IN_TOPIC') or "testarhs/server"
    MQTT_OUT_TOPIC = os.environ.get('MQTT_OUT_TOPIC') or "testarhs/porta"
    MQTT_KEY = os.environ.get('MQTT_KEY') or "you-will-never-guess-again"
