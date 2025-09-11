import toml


class Utils:
    def __init__(self):
        pass

    def get_pyproject(self):
        with open('pyproject.toml', 'r') as f:
            return toml.load(f)
