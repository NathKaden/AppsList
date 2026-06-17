from models.launcher import Launcher

class Disk:
    def __init__(self, name, launchers=None):
        self.name = name
        self.launchers = launchers if launchers is not None else {}

    @classmethod
    def from_dict(cls, name, launchers_data):
        disk = cls(name)
        for launcher_name, apps_list in launchers_data.items():
            disk.launchers[launcher_name] = Launcher.from_list(launcher_name, apps_list)
        return disk

    def to_dict(self):
        return {launcher_name: launcher.to_list() for launcher_name, launcher in self.launchers.items()}
