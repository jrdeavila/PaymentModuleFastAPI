from firebase_admin import firestore, credentials, initialize_app


# Singleton
class FirebaseApp:
    __instance = None
    __app = None

    @staticmethod
    def getInstance():
        if FirebaseApp.__instance == None:
            FirebaseApp()
        return FirebaseApp.__instance

    def __init__(self):
        if FirebaseApp.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            FirebaseApp.__instance = self
            FirebaseApp.__app = initialize_app(
                credentials.Certificate(
                    "core/infrastructure/firebase/firebase_credentials.json"
                )
            )

    def getApp(self):
        return FirebaseApp.__app


def inject_firestore() -> any:
    app = FirebaseApp.getInstance().getApp()
    db = firestore.client(app=app)
    return db
