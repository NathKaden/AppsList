import unittest
import os
import json
from PyQt6.QtWidgets import QApplication
from ui.components import SettingsWidget

# A single QApplication instance is required for creating widgets in PyQt
app = QApplication.instance()
if app is None:
    app = QApplication([])

class TestSettingsWidget(unittest.TestCase):
    def setUp(self):
        self.test_settings_path = "tests/test_settings_temp.json"
        self.initial_settings = {
            "path_bdd": "bdd/BDDTest.json",
            "colors": ["#112233", "#445566"]
        }
        os.makedirs(os.path.dirname(self.test_settings_path), exist_ok=True)
        with open(self.test_settings_path, "w", encoding="utf-8") as f:
            json.dump(self.initial_settings, f, indent=4)
        
        self.save_called = False
        self.cancel_called = False
        
        self.widget = SettingsWidget(
            settings_path=self.test_settings_path,
            on_save=self.on_save,
            on_cancel=self.on_cancel
        )

    def tearDown(self):
        self.widget.deleteLater()
        if os.path.exists(self.test_settings_path):
            try:
                os.remove(self.test_settings_path)
            except OSError:
                pass

    def on_save(self):
        self.save_called = True

    def on_cancel(self):
        self.cancel_called = True

    def test_load_settings(self):
        self.assertEqual(self.widget.current_path, "bdd/BDDTest.json")
        self.assertEqual(self.widget.current_colors, ["#112233", "#445566"])
        self.assertEqual(self.widget.path_input.text(), "bdd/BDDTest.json")

    def test_delete_color(self):
        # Initial count is 2
        self.assertEqual(len(self.widget.current_colors), 2)
        # Delete first color
        self.widget.delete_color(0)
        self.assertEqual(len(self.widget.current_colors), 1)
        self.assertEqual(self.widget.current_colors[0], "#445566")

    def test_save_settings(self):
        # Change BDD path
        self.widget.path_input.setText("bdd/NewBDD.json")
        # Add a color
        self.widget.current_colors.append("#778899")
        
        # Save
        self.widget.save_settings()
        self.assertTrue(self.save_called)
        
        # Verify saved contents
        with open(self.test_settings_path, "r", encoding="utf-8") as f:
            saved = json.load(f)
        self.assertEqual(saved["path_bdd"], "bdd/NewBDD.json")
        self.assertEqual(saved["colors"], ["#112233", "#445566", "#778899"])
