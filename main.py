import firebase_admin
from firebase_admin import credentials
import time


def main_loop():
    import data
    import controllers
    listeners.listen()
    test.send_ping('R6U6M8yjm4VYJ9O9aMuoDpPFYVC2')
    while 1:
        print("still alive")
        time.sleep(300)


if __name__ == '__main__':
    cred = credentials.Certificate("tradinggame-3e673-firebase-adminsdk-1mfhz-b836064b24.json")
    firebase_admin.initialize_app(cred)
    import listeners
    import test
    try:
        main_loop()
        print("Service started")
    except KeyboardInterrupt:
        print("Service stopped")
        exit(0)
