from robot.robot import Robot


class Page:
    URL: str | None = None

    def __init__(self, robot: Robot, skip_init_load: bool = True):
        self.robot = robot
        self.skip_init_load = skip_init_load
        if not skip_init_load:
            self.load()

    def load(self):
        if self.URL is None:
            raise ValueError('Page url is not set')
        self.robot.load_url(self.URL)
