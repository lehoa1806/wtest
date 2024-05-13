class Error(dict):
    def __init__(self, msg: str = '', **kwargs) -> None:
        super().__init__(**kwargs)
        self.update({'message': msg})


class Start(dict):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Stop(dict):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
