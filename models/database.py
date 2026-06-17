import json
import os
from models.disk import Disk
from models.app import App

class Database:
    def __init__(self, filepath):
        self.filepath = filepath
        self.disks = {}

    def load(self):
        if not os.path.exists(self.filepath):
            self.disks = {}
            self.save()
            return
        
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        self.disks = {}
        for disk_name, launchers_data in data.items():
            self.disks[disk_name] = Disk.from_dict(disk_name, launchers_data)

    def save(self):
        data = {disk_name: disk.to_dict() for disk_name, disk in self.disks.items()}
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_disques(self):
        return list(self.disks.keys())

    def get_launchers(self):
        launchers = set()
        for disk in self.disks.values():
            launchers.update(disk.launchers.keys())
        return list(launchers)

    def get_apps_count(self):
        count = 0
        for disk in self.disks.values():
            for launcher in disk.launchers.values():
                count += len(launcher.apps)
        return count

    def get_occurrences_count(self, app_name, return_list=False):
        count = 0
        matching_names = []
        for disk in self.disks.values():
            for launcher in disk.launchers.values():
                for app in launcher.apps:
                    if app.name.lower() == app_name.lower():
                        count += 1
                        if return_list:
                            matching_names.append(app.name)
        return matching_names if return_list else count

    def get_apps_list(self):
        apps = []
        for disk in self.disks.values():
            for launcher in disk.launchers.values():
                apps.extend(launcher.apps)
        return apps

    def find_app(self, app_name):
        for disk in self.disks.values():
            for launcher in disk.launchers.values():
                for app in launcher.apps:
                    if app.name.lower() == app_name.lower():
                        return disk, launcher, app
        return None

    def add_app(self, disk_name, launcher_name, app_name, size=0.0, year=0):
        if disk_name not in self.disks:
            return "Erreur : Disque"
        disk = self.disks[disk_name]
        
        if launcher_name not in disk.launchers:
            from models.launcher import Launcher
            disk.launchers[launcher_name] = Launcher(launcher_name)
        launcher = disk.launchers[launcher_name]
        
        # Check if app already exists in this launcher
        for app in launcher.apps:
            if app.name.lower() == app_name.lower():
                return "Erreur : L'application existe deja"
                
        app = App(app_name, size, year)
        launcher.apps.append(app)
        self.save()
        return "Application ajoutée avec succès"

    def delete_app(self, app_name):
        location = self.find_app(app_name)
        if not location:
            return "Erreur : Application non trouvée"
        
        disk, launcher, app = location
        launcher.apps.remove(app)
        self.save()
        return "Application supprimée avec succès"

    def get_app_launchers(self, app_name):
        launchers = []
        for disk in self.disks.values():
            for launcher_name, launcher in disk.launchers.items():
                for app in launcher.apps:
                    if app.name.lower() == app_name.lower():
                        if launcher_name not in launchers:
                            launchers.append(launcher_name)
        return launchers

    def delete_app_from_launcher(self, app_name, launcher_name):
        for disk in self.disks.values():
            for l_name, launcher in disk.launchers.items():
                if l_name.lower() == launcher_name.lower():
                    for app in launcher.apps:
                        if app.name.lower() == app_name.lower():
                            launcher.apps.remove(app)
                            self.save()
                            return "Application supprimée avec succès"
        return "Erreur : Application non trouvée"
