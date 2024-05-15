class Error(dict):
    def __init__(self, msg: str = '', **kwargs) -> None:
        super().__init__(**kwargs)
        self.update({'message': msg})


class Data(dict):
    def __init__(self, **kwargs) -> None:
        self['stage'] = []
        for k, v in kwargs.items():
            self[k] = v

    @property
    def current_stage(self):
        return self.get('stage')

    def set_stage(self, stage):
        self['stage'].append(stage)
        return self['stage']

    def backtrace(self):
        return format(f'[Data id: {self["id"]}] ') + '-->'.join(self['stage'])


class Start(Data):
    def __init__(self, **kwargs) -> None:
        self['name'] = 'Start'
        super().__init__(**kwargs)


class Stop(Data):
    def __init__(self, **kwargs) -> None:
        self['name'] = 'Stop'
        super().__init__(**kwargs)
