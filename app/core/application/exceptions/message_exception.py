class MessageException(Exception):
    name: str
    message: any
    code: int

    def __init__(self, name: str, message: any, code: int = 400) -> None:
        self.name = name
        self.message = message
        self.code = code
