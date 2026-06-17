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


from ui.components import NewBddInputWidget

class TestNewBddInputWidget(unittest.TestCase):
    def setUp(self):
        self.test_assets_dir = "tests/test_assets_temp/"
        self.test_settings_path = self.test_assets_dir + "settings.json"
        
        os.makedirs(self.test_assets_dir, exist_ok=True)
        self.initial_settings = {
            "path_bdd": "bdd/BDDTest.json",
            "colors": []
        }
        with open(self.test_settings_path, "w", encoding="utf-8") as f:
            json.dump(self.initial_settings, f, indent=4)
            
        self.created_called = False
        self.close_called = False
        self.created_path = None
        
        self.widget = NewBddInputWidget(
            assetsdir=self.test_assets_dir,
            on_created_callback=self.on_created,
            on_close_callback=self.on_close
        )

    def tearDown(self):
        self.widget.deleteLater()
        
        if self.created_path and os.path.exists(self.created_path):
            try:
                os.remove(self.created_path)
            except OSError:
                pass
                
        if os.path.exists(self.test_settings_path):
            try:
                os.remove(self.test_settings_path)
            except OSError:
                pass
                
        test_bdd_dir = "tests/bdd"
        if os.path.exists(test_bdd_dir):
            import shutil
            try:
                shutil.rmtree(test_bdd_dir)
            except OSError:
                pass
                
        if os.path.exists(self.test_assets_dir):
            try:
                os.rmdir(self.test_assets_dir)
            except OSError:
                pass

    def on_created(self, path):
        self.created_called = True
        self.created_path = path

    def on_close(self):
        self.close_called = True

    def test_create_new_bdd(self):
        self.widget.setText("Test SSD")
        self.widget.create_new_bdd()
        
        self.assertTrue(self.created_called)
        self.assertIsNotNone(self.created_path)
        self.assertTrue(os.path.exists(self.created_path))
        
        with open(self.created_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        self.assertEqual(content, {})
        
        with open(self.test_settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.assertEqual(settings["path_bdd"], "bdd/Test_SSD.json")

    def test_create_existing_bdd_does_not_overwrite(self):
        # Pre-create the file with some content
        test_dir = os.path.dirname(self.test_settings_path)
        bdd_dir = os.path.join(os.path.dirname(test_dir), "bdd").replace("\\", "/")
        os.makedirs(bdd_dir, exist_ok=True)
        existing_path = os.path.join(bdd_dir, "Test_SSD.json").replace("\\", "/")
        
        pre_existing_data = {"existing_disk": {"Steam": []}}
        with open(existing_path, "w", encoding="utf-8") as f:
            json.dump(pre_existing_data, f, indent=4)
            
        self.widget.setText("Test SSD")
        self.widget.create_new_bdd()
        
        self.assertTrue(self.created_called)
        self.assertEqual(self.created_path.replace("\\", "/"), existing_path)
        
        # Verify the file was NOT overwritten with empty {}
        with open(existing_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        self.assertEqual(content, pre_existing_data)
        
        # Clean up the pre-created file
        if os.path.exists(existing_path):
            os.remove(existing_path)


from unittest.mock import patch
from main import MainWindow

class TestMainWindowOpenBdd(unittest.TestCase):
    def setUp(self):
        self.settings_path = "assets/settings.json"
        self.backup_settings_path = "assets/settings_backup_test.json"
        if os.path.exists(self.settings_path):
            import shutil
            shutil.copy(self.settings_path, self.backup_settings_path)
            
    def tearDown(self):
        if os.path.exists(self.backup_settings_path):
            import shutil
            shutil.move(self.backup_settings_path, self.settings_path)

    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName')
    def test_open_bdd_file(self, mock_get_open):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_file = os.path.join(current_dir, "bdd", "BDDTest.json").replace("\\", "/")
        mock_get_open.return_value = (target_file, "JSON Files (*.json)")
        
        win = MainWindow()
        win.open_bdd_file()
        
        self.assertEqual(win.db.filepath.replace("\\", "/"), target_file)
        self.assertEqual(win.stacked_widget.currentIndex(), 0)
        
        with open(self.settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.assertEqual(settings["path_bdd"], "bdd/BDDTest.json")
        
        win.deleteLater()

    def test_new_bdd_updates_settings_widget(self):
        win = MainWindow()
        self.assertTrue(hasattr(win, 'settings_widget'))
        
        path_settings = win.assetsdir + "settings.json"
        with open(path_settings, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data["path_bdd"] = "bdd/BDD_new_test.json"
        with open(path_settings, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        win.on_new_bdd_created("bdd/BDD_new_test.json")
        
        self.assertEqual(win.settings_widget.path_input.text(), "bdd/BDD_new_test.json")
        self.assertEqual(win.stacked_widget.currentIndex(), 0)
        
        win.deleteLater()
