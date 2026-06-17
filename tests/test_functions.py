import unittest
import os
import json
from functions.functions import getDisques, getLaunchers, getApps, getOccurApps, getNbApps, terminal
from models.database import Database

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "tests/test_db_temp.json"
        self.initial_data = {
            "SSD Main": {
                "Steam": [
                    {"nom": "Celeste", "taille": 1.2, "année": 2018}
                ]
            },
            "HDD Storage": {
                "Epic Games": [
                    {"nom": "Subnautica", "taille": 20.0, "année": 2018}
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

    def test_get_disques(self):
        disks = getDisques(self.db)
        self.assertEqual(len(disks), 2)
        self.assertIn("SSD Main", disks)
        self.assertIn("HDD Storage", disks)

    def test_get_launchers(self):
        launchers = getLaunchers(self.db)
        self.assertEqual(len(launchers), 2)
        self.assertIn("Steam", launchers)
        self.assertIn("Epic Games", launchers)

    def test_get_apps(self):
        apps = getApps(self.db)
        self.assertEqual(len(apps), 2)
        names = [app["nom"] for app in apps]
        self.assertIn("Celeste", names)
        self.assertIn("Subnautica", names)

    def test_get_occur_apps(self):
        self.assertEqual(getOccurApps(self.db, "Celeste"), 1)
        self.assertEqual(getOccurApps(self.db, "nonexistent"), 0)

    def test_get_nb_apps(self):
        self.assertEqual(getNbApps(self.db), 2)

    def test_terminal_parser(self):
        help_msg = terminal("help", self.db, self.test_db_path)
        self.assertIn("Commandes possibles", help_msg)

        print_msg = terminal("print", self.db, self.test_db_path)
        self.assertIn("Disques", print_msg)

        add_msg = terminal('add app "SSD Main" "Tomb Raider" "Steam" 25 2013', self.db, self.test_db_path)
        self.assertIn("Application ajoutée avec succès", add_msg)

        del_msg = terminal('delete app "Subnautica"', self.db, self.test_db_path)
        self.assertIn("Application supprimée avec succès", del_msg)

        # Test deleting non-existent app
        del_nonexistent = terminal('delete app "NonExistentGame"', self.db, self.test_db_path)
        self.assertIn("n'a pas été trouvée dans la base de données", del_nonexistent)

        # Add duplicate app to test multiple occurrences delete
        terminal('add app "SSD Main" "DuplicateGame" "Steam" 20 2020', self.db, self.test_db_path)
        terminal('add app "HDD Storage" "DuplicateGame" "Epic Games" 20 2020', self.db, self.test_db_path)
        
        # Test delete duplicate app without launcher
        del_dup_no_launcher = terminal('delete app "DuplicateGame"', self.db, self.test_db_path)
        self.assertIn("car plusieurs occurrences ont été trouvées", del_dup_no_launcher)

        # Test delete duplicate app with wrong launcher
        del_dup_wrong_launcher = terminal('delete app "DuplicateGame" "Nintendo"', self.db, self.test_db_path)
        self.assertIn("n'existe pas sous le launcher 'Nintendo'", del_dup_wrong_launcher)

        # Test delete duplicate app with correct launcher
        del_dup_ok = terminal('delete app "DuplicateGame" "Steam"', self.db, self.test_db_path)
        self.assertIn("Application supprimée avec succès", del_dup_ok)
