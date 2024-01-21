from core.domain.entities.application import Application


class ApplicationLoginService:
    def login(self, username: str, password: str) -> Application:
        pass


class ApplicationRegisterService:
    def register(self, application: Application, password: str) -> Application:
        pass
