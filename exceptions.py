class StatusCodeException(Exception):
    def __init__(self, answer_status_code, answer_text):
        self.answer_status_code = answer_status_code
        self.answer_text = answer_text
        super().__init__(self.answer_status_code)


class StatusCode403(StatusCodeException):
    # Вы забанены на https://goldapple.ru/parfjumerija
    pass


class StatusCodeNot200(StatusCodeException):
    # Код ответа не 200
    pass


