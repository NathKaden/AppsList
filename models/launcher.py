from models.app import App

class Launcher:
    def __init__(self, name, apps=None):
        self.name = name
        self.apps = apps if apps is not None else []

    @classmethod
    def from_list(cls, name, apps_list):
        launcher = cls(name)
        for app_data in apps_list:
            launcher.apps.append(App.from_dict(app_data))
        return launcher

    def to_list(self):
        return [app.to_dict() for app in self.apps]
