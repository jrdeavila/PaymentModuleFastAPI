import hashlib
import uuid
from core.application.exceptions.message_exception import MessageException
from core.domain.entities.application import Application
from core.domain.services.application_auth_service import (
    ApplicationLoginService,
    ApplicationRegisterService,
)
from pymongo import MongoClient


class MongoApplicationInDb(Application):
    hashed_password: str


class MongoApplicationLoginService(ApplicationLoginService):
    mongo_client: MongoClient

    def __init__(self, mongo_client: MongoClient) -> None:
        self.mongo_client = mongo_client

    def login(self, username: str, password: str) -> Application:
        payment_db = self.mongo_client.payment
        collection = payment_db.applications
        doc = collection.find_one({"username": username})
        if doc is None:
            raise MessageException(
                code=404,
                name="Application Not Found",
                message="The application with the given username was not found.",
            )
        application_in_db = MongoApplicationInDb(**doc)
        if not verify_password(password, application_in_db.hashed_password):
            raise MessageException(
                code=401,
                name="Invalid Credentials",
                message="Incorrect username or password.",
            )
        application = Application(**(vars(application_in_db)))
        return application


class MongoRegisterApplicationService(ApplicationRegisterService):
    mongo_client: MongoClient

    def __init__(self, mongo_client: MongoClient) -> None:
        self.mongo_client = mongo_client

    def register(self, application: Application, password: str) -> Application:
        payment_db = self.mongo_client.payment
        collection = payment_db.applications
        hashed_password = hash_password(password)
        id = generate_application_id()
        application.id = id
        application_in_db = MongoApplicationInDb(
            **(vars(application)), hashed_password=hashed_password
        )
        collection.insert_one({"_id": id, **(vars(application_in_db))})
        return application


def generate_application_id() -> str:
    return str(uuid.uuid4())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def hash_password(password: str) -> str:
    return hashlib.scrypt(password.encode(), salt=b"salt", n=16384, r=8, p=1).hex()
