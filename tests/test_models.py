import unittest
import os
import json
from models.app import App
from models.launcher import Launcher
from models.disk import Disk
from models.database import Database

class TestAppModel(unittest.TestCase):
    def test_app_creation(self):
        app = App("Portal 2", 12.5, 2011)
        self.assertEqual(app.name, "Portal 2")
        self.assertEqual(app.size, 12.5)
        self.assertEqual(app.year, 2011)

    def test_app_serialization(self):
        app = App("Minecraft", 2.0, 2011)
        app_dict = app.to_dict()
        self.assertEqual(app_dict["nom"], "Minecraft")
        self.assertEqual(app_dict["taille"], 2.0)
        self.assertEqual(app_dict["année"], 2011)

        app_deserialized = App.from_dict(app_dict)
        self.assertEqual(app_deserialized.name, "Minecraft")
        self.assertEqual(app_deserialized.size, 2.0)
        self.assertEqual(app_deserialized.year, 2011)


class TestLauncherModel(unittest.TestCase):
    def test_launcher_creation(self):
        launcher = Launcher("Steam")
        self.assertEqual(launcher.name, "Steam")
        self.assertEqual(len(launcher.apps), 0)

    def test_launcher_from_list(self):
        apps_data = [
            {"nom": "Half-Life 2", "taille": 6.5, "année": 2004},
            {"nom": "Left 4 Dead 2", "taille": 15.0, "année": 2009}
        ]
        launcher = Launcher.from_list("Steam", apps_data)
        self.assertEqual(launcher.name, "Steam")
        self.assertEqual(len(launcher.apps), 2)
        self.assertEqual(launcher.apps[0].name, "Half-Life 2")


class TestDiskModel(unittest.TestCase):
    def test_disk_creation(self):
        disk = Disk("SSD")
        self.assertEqual(disk.name, "SSD")
        self.assertEqual(len(disk.launchers), 0)

    def test_disk_serialization(self):
        disk_data = {
            "Steam": [
                {"nom": "Terraria", "taille": 0.5, "année": 2011}
            ]
        }
        disk = Disk.from_dict("SSD", disk_data)
        self.assertEqual(disk.name, "SSD")
        self.assertIn("Steam", disk.launchers)
        self.assertEqual(disk.launchers["Steam"].apps[0].name, "Terraria")


class TestDatabaseModel(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "tests/test_db_temp.json"
        self.initial_data = {
            "SSD Main": {
                "Steam": [
                    {"nom": "Celeste", "taille": 1.2, "année": 2018}
                ]
            }
        }
        os.makedirs(os.path.dirname(self.test_db_path), exist_ok=True)
        with open(self.test_db_path, "w", encoding="utf-8") as f:
            json.dump(self.initial_data, f, indent=4)
        
        self.db = Database(self.test_db_path)
        self.db.load()

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except OSError:
                pass

    def test_database_load(self):
        self.assertIn("SSD Main", self.db.disks)
        self.assertIn("Steam", self.db.disks["SSD Main"].launchers)
        apps = self.db.get_apps_list()
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0].name, "Celeste")

    def test_find_app(self):
        res = self.db.find_app("Celeste")
        self.assertIsNotNone(res)
        disk, launcher, app = res
        self.assertEqual(disk.name, "SSD Main")
        self.assertEqual(launcher.name, "Steam")
        self.assertEqual(app.name, "Celeste")

        self.assertIsNone(self.db.find_app("Nonexistent"))

    def test_add_app(self):
        msg = self.db.add_app("SSD Main", "Steam", "Hades", 15.0, 2020)
        self.assertEqual(msg, "Application ajoutée avec succès")
        
        self.db.load()
        res = self.db.find_app("Hades")
        self.assertIsNotNone(res)
        self.assertEqual(res[2].size, 15.0)

        msg_duplicate = self.db.add_app("SSD Main", "Steam", "Hades", 15.0, 2020)
        self.assertTrue(msg_duplicate.startswith("Erreur"))

    def test_delete_app(self):
        msg = self.db.delete_app("Celeste")
        self.assertEqual(msg, "Application supprimée avec succès")
        
        self.db.load()
        self.assertIsNone(self.db.find_app("Celeste"))

        msg_nonexistent = self.db.delete_app("Nonexistent")
        self.assertTrue(msg_nonexistent.startswith("Erreur"))
