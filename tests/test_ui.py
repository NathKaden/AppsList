import unittest
import os
import json
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog
from ui.components import SettingsWidget

REAL_OPEN = open

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


class TestMainWindowAppDetails(unittest.TestCase):
    def setUp(self):
        self.settings_path = "assets/settings.json"
        self.backup_settings_path = "assets/settings_backup_test.json"
        if os.path.exists(self.settings_path):
            import shutil
            shutil.copy(self.settings_path, self.backup_settings_path)
            
        self.db_path = "tests/test_bdd_temp.json"
        self.initial_data = {
            "SSD Main": {
                "Steam": [
                    {"nom": "Celeste", "taille": 1.2, "année": 2018}
                ]
            }
        }
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.initial_data, f, indent=4)
            
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
            settings["path_bdd"] = self.db_path
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)

        self.win = MainWindow()

    def tearDown(self):
        self.win.deleteLater()
        if os.path.exists(self.backup_settings_path):
            import shutil
            shutil.move(self.backup_settings_path, self.settings_path)
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_show_app_details(self):
        app = self.win.db.disks["SSD Main"].launchers["Steam"].apps[0]
        launcher = self.win.db.disks["SSD Main"].launchers["Steam"]
        
        self.win.show_app_details(app, launcher)
        
        self.assertFalse(self.win.side_panel.isHidden())
        self.assertEqual(self.win.side_name_input.text(), "Celeste")
        self.assertEqual(self.win.side_year_input.value(), 2018)
        self.assertEqual(self.win.side_size_input.value(), 1.2)

    def test_save_app_details(self):
        app = self.win.db.disks["SSD Main"].launchers["Steam"].apps[0]
        launcher = self.win.db.disks["SSD Main"].launchers["Steam"]
        
        self.win.show_app_details(app, launcher)
        self.win.side_name_input.setText("Celeste Remastered")
        self.win.side_year_input.setValue(2020)
        self.win.side_size_input.setValue(2.5)
        
        self.win.save_app_details()
        
        self.assertTrue(self.win.side_panel.isHidden())
        self.assertEqual(app.name, "Celeste Remastered")
        self.assertEqual(app.year, 2020)
        self.assertEqual(app.size, 2.5)
        
        with open(self.db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["SSD Main"]["Steam"][0]["nom"], "Celeste Remastered")

    @patch('PyQt6.QtWidgets.QMessageBox.question')
    def test_delete_selected_app(self, mock_question):
        mock_question.return_value = QMessageBox.StandardButton.Yes
        app = self.win.db.disks["SSD Main"].launchers["Steam"].apps[0]
        launcher = self.win.db.disks["SSD Main"].launchers["Steam"]
        
        self.win.show_app_details(app, launcher)
        self.win.delete_selected_app()
        
        self.assertTrue(self.win.side_panel.isHidden())
        self.assertEqual(len(launcher.apps), 0)



    @patch('PyQt6.QtWidgets.QMenu.exec')
    def test_app_label_context_menu_modify(self, mock_exec):
        from ui.components import AppLabel
        from PyQt6.QtGui import QContextMenuEvent
        from PyQt6.QtCore import QPoint
        import PyQt6.QtWidgets
        
        app_label = self.win.canvas_container.findChildren(AppLabel)[0]
        
        actions = []
        original_add_action = PyQt6.QtWidgets.QMenu.addAction
        
        def mock_add_action(menu_self, text):
            act = original_add_action(menu_self, text)
            actions.append(act)
            return act
            
        with patch('PyQt6.QtWidgets.QMenu.addAction', mock_add_action):
            def exec_side_effect(*args, **kwargs):
                return actions[0]  # Modifier action
            mock_exec.side_effect = exec_side_effect
            
            from PyQt6.QtCore import QPointF
            local_pos = app_label.mapTo(self.win.canvas_container, QPoint(app_label.width() // 2, app_label.height() // 2))
            scene_pos = self.win.proxy.mapToScene(QPointF(local_pos))
            viewport_pos = self.win.canvas_view.mapFromScene(scene_pos)
            
            self.win.canvas_view.afficher_menu_contextuel(viewport_pos)
            
            self.assertFalse(self.win.side_panel.isHidden())
            self.assertEqual(self.win.selected_app, app_label.app)

    @patch('PyQt6.QtWidgets.QMenu.exec')
    @patch('PyQt6.QtWidgets.QMessageBox.question')
    def test_app_label_context_menu_delete(self, mock_question, mock_exec):
        from ui.components import AppLabel
        from PyQt6.QtGui import QContextMenuEvent
        from PyQt6.QtCore import QPoint
        import PyQt6.QtWidgets
        
        mock_question.return_value = QMessageBox.StandardButton.Yes
        app_label = self.win.canvas_container.findChildren(AppLabel)[0]
        
        actions = []
        original_add_action = PyQt6.QtWidgets.QMenu.addAction
        
        def mock_add_action(menu_self, text):
            act = original_add_action(menu_self, text)
            actions.append(act)
            return act
            
        with patch('PyQt6.QtWidgets.QMenu.addAction', mock_add_action):
            def exec_side_effect(*args, **kwargs):
                return actions[1]  # Supprimer action
            mock_exec.side_effect = exec_side_effect
            
            initial_count = len(app_label.launcher.apps)
            
            from PyQt6.QtCore import QPointF
            local_pos = app_label.mapTo(self.win.canvas_container, QPoint(app_label.width() // 2, app_label.height() // 2))
            scene_pos = self.win.proxy.mapToScene(QPointF(local_pos))
            viewport_pos = self.win.canvas_view.mapFromScene(scene_pos)
            
            self.win.canvas_view.afficher_menu_contextuel(viewport_pos)
            
            self.assertEqual(len(app_label.launcher.apps), initial_count - 1)

    @patch('PyQt6.QtWidgets.QInputDialog.getText')
    def test_rechercher_jeu_success(self, mock_get_text):
        mock_get_text.return_value = ("Celeste", True)
        self.assertTrue(self.win.side_panel.isHidden())
        self.win.rechercher_jeu()
        self.assertFalse(self.win.side_panel.isHidden())
        self.assertEqual(self.win.selected_app.name, "Celeste")

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    @patch('PyQt6.QtWidgets.QInputDialog.getText')
    def test_rechercher_jeu_not_found(self, mock_get_text, mock_info):
        mock_get_text.return_value = ("NonExistentGame", True)
        self.win.rechercher_jeu()
        mock_info.assert_called_once()
        self.assertTrue(self.win.side_panel.isHidden())

    @patch('PyQt6.QtWidgets.QInputDialog.getText')
    def test_rechercher_jeu_on_settings_page(self, mock_get_text):
        self.win.stacked_widget.setCurrentIndex(1)
        self.win.rechercher_jeu()
        mock_get_text.assert_not_called()

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    @patch('ctypes.windll.kernel32.GetVolumeInformationW')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('builtins.open')
    def test_remplir_automatiquement_success(self, mock_open, mock_listdir, mock_isdir, mock_get_volume, mock_info):
        def side_effect_volume(drive, buf, *args):
            buf.value = "SSD Main"
            return True
        mock_get_volume.side_effect = side_effect_volume
        
        mock_isdir.side_effect = lambda path: "steamapps" in path.lower() or "manifests" in path.lower() or path.endswith("Steam")
        
        def side_effect_listdir(path):
            if "steamapps" in path.lower():
                return ["appmanifest_123.acf"]
            if "manifests" in path.lower():
                return ["gta.item"]
            return []
        mock_listdir.side_effect = side_effect_listdir
        
        from unittest.mock import mock_open as m_open
        acf_content = '"name" "Mock Steam Game"\n"SizeOnDisk" "10737418240"'
        epic_content = '{"DisplayName": "Mock Epic Game", "InstallLocation": "C:\\\\Games\\\\Epic", "InstallSize": 21474836480}'
        
        original_open = REAL_OPEN
        def side_effect_open(path, *args, **kwargs):
            if "temp" in path or "settings" in path or "BDD" in path:
                return original_open(path, *args, **kwargs)
            content = ""
            if "libraryfolders.vdf" in path:
                content = '"libraryfolders" { "0" { "path" "C:\\\\Program Files (x86)\\\\Steam" } }'
            elif "appmanifest_" in path:
                content = acf_content
            elif "gta.item" in path:
                content = epic_content
            else:
                content = "{}"
            return m_open(read_data=content).return_value
            
        mock_open.side_effect = side_effect_open
        
        self.win.db.disks["SSD Main"].launchers = {}
        self.win.db.save()
        
        self.win.remplir_automatiquement()
        
        mock_info.assert_called_once()
        
        steam_launcher = self.win.db.disks["SSD Main"].launchers.get("Steam")
        self.assertIsNotNone(steam_launcher)
        self.assertEqual(steam_launcher.apps[0].name, "Mock Steam Game")
        self.assertEqual(steam_launcher.apps[0].size, 10.0)
        
        epic_launcher = self.win.db.disks["SSD Main"].launchers.get("Epic Games")
        self.assertIsNotNone(epic_launcher)
        self.assertEqual(epic_launcher.apps[0].name, "Mock Epic Game")
        self.assertEqual(epic_launcher.apps[0].size, 20.0)

    def test_game_with_small_size_hidden(self):
        from ui.components import AppLabel
        from models.app import App
        launcher = self.win.db.disks["SSD Main"].launchers["Steam"]
        launcher.apps = [
            App("Big Game", size=0.1, year=2020),
            App("Small Game", size=0.05, year=2020)
        ]
        self.win.db.save()
        self.win.refresh()
        
        app_labels = self.win.canvas_container.findChildren(AppLabel)
        names = [label.app.name for label in app_labels]
        self.assertIn("Big Game", names)
        self.assertNotIn("Small Game", names)

    def test_game_with_no_year_empty_spinbox(self):
        from models.app import App
        launcher = self.win.db.disks["SSD Main"].launchers["Steam"]
        app_zero = App("No Year Game", size=1.0, year=0)
        app_year = App("With Year Game", size=1.0, year=2022)
        launcher.apps = [app_zero, app_year]
        self.win.db.save()
        self.win.refresh()
        
        self.win.show_app_details(app_zero, launcher)
        self.assertEqual(self.win.side_year_input.value(), 0)
        self.assertEqual(self.win.side_year_input.text(), "")
        
        self.win.show_app_details(app_year, launcher)
        self.assertEqual(self.win.side_year_input.value(), 2022)
        self.assertEqual(self.win.side_year_input.text(), "2022")

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_disk_details_renaming_and_image(self, mock_info):
        disk = self.win.db.disks["SSD Main"]
        self.win.show_disk_details(disk)
        self.assertFalse(self.win.disk_panel.isHidden())
        self.assertEqual(self.win.disk_name_input.text(), "SSD Main")
        
        # Change disk name and image
        self.win.disk_name_input.setText("New Disk Name")
        if self.win.disk_image_combo.count() > 0:
            self.win.disk_image_combo.setCurrentIndex(0)
            
        self.win.save_disk_details()
        self.assertTrue(self.win.disk_panel.isHidden())
        
        self.assertIn("New Disk Name", self.win.db.disks)
        self.assertNotIn("SSD Main", self.win.db.disks)
        
        # Verify it was saved to settings
        with open(self.win.assetsdir + "settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.assertIn("New Disk Name", settings.get("disk_images", {}))
        mock_info.assert_called_once()

    @patch('PyQt6.QtWidgets.QMenu.exec')
    def test_disk_widget_context_menu_modify(self, mock_exec):
        from ui.components import DiskWidget
        from PyQt6.QtCore import QPoint
        import PyQt6.QtWidgets
        
        disk_widget = self.win.canvas_container.findChild(DiskWidget)
        self.assertIsNotNone(disk_widget)
        
        actions = []
        original_add_action = PyQt6.QtWidgets.QMenu.addAction
        
        def mock_add_action(menu_self, text):
            act = original_add_action(menu_self, text)
            actions.append(act)
            return act
            
        with patch('PyQt6.QtWidgets.QMenu.addAction', mock_add_action):
            def exec_side_effect(*args, **kwargs):
                return actions[0]  # Modifier action
            mock_exec.side_effect = exec_side_effect
            
            from PyQt6.QtCore import QPointF
            local_pos = disk_widget.disk_name_label.mapTo(self.win.canvas_container, QPoint(disk_widget.disk_name_label.width() // 2, disk_widget.disk_name_label.height() // 2))
            scene_pos = self.win.proxy.mapToScene(QPointF(local_pos))
            viewport_pos = self.win.canvas_view.mapFromScene(scene_pos)
            
            self.win.canvas_view.afficher_menu_contextuel(viewport_pos)
            
            self.assertFalse(self.win.disk_panel.isHidden())
            self.assertEqual(self.win.selected_disk.name, disk_widget.disk.name)

    @patch('PyQt6.QtWidgets.QMenu.exec')
    def test_disk_widget_context_menu_modify_outside_name(self, mock_exec):
        from ui.components import DiskWidget
        from PyQt6.QtCore import QPoint
        import PyQt6.QtWidgets
        
        disk_widget = self.win.canvas_container.findChild(DiskWidget)
        self.assertIsNotNone(disk_widget)
        
        self.win.disk_panel.hide()
        
        # Click on bottom right of the disk widget, far from header
        from PyQt6.QtCore import QPointF
        local_pos = disk_widget.mapTo(self.win.canvas_container, QPoint(disk_widget.width() - 5, disk_widget.height() - 5))
        scene_pos = self.win.proxy.mapToScene(QPointF(local_pos))
        viewport_pos = self.win.canvas_view.mapFromScene(scene_pos)
        
        self.win.canvas_view.afficher_menu_contextuel(viewport_pos)
        
        # Verify it did not trigger disk panel showing
        self.assertTrue(self.win.disk_panel.isHidden())
        mock_exec.assert_not_called()

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    @patch('ctypes.windll.kernel32.GetVolumeInformationW')
    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('winreg.OpenKey')
    @patch('winreg.QueryInfoKey')
    @patch('winreg.EnumKey')
    @patch('winreg.QueryValueEx')
    def test_remplir_automatiquement_platforms(self, mock_query_value_ex, mock_enum_key, mock_query_info_key, mock_open_key,
                                               mock_getsize, mock_walk, mock_listdir, mock_exists, mock_isdir, mock_volume, mock_info):
        from unittest.mock import MagicMock, mock_open
        
        # 1. Setup Volume mock
        def side_effect_volume(drive, buf, *args):
            buf.value = "SSD Main"
            return True
        mock_volume.side_effect = side_effect_volume
        
        # 2. Setup path checks
        def side_effect_isdir(path):
            p_lower = path.lower()
            if "steam" in p_lower or "manifests" in p_lower:
                return False
            return True
        mock_isdir.side_effect = side_effect_isdir
        
        def side_effect_exists(path):
            p_lower = path.lower()
            if "steam" in p_lower or "manifests" in p_lower:
                return False
            return True
        mock_exists.side_effect = side_effect_exists
        
        # 3. Setup os.listdir
        def side_effect_listdir(path):
            if "XboxGames" in path:
                return ["Minecraft for Windows"]
            return []
        mock_listdir.side_effect = side_effect_listdir
        
        # 4. Setup os.walk & os.path.getsize
        mock_walk.side_effect = lambda path: [ (path, [], ["file.bin"]) ]
        mock_getsize.side_effect = lambda path: 5 * 1024**3 # 5 GB
        
        # 5. Setup winreg mocks
        def mock_open_key_side_effect(key_or_hive, subkey_name=None, *args):
            m = MagicMock()
            m.__enter__.return_value = m
            if subkey_name == "Call of Duty Black Ops Cold War":
                m.name = "CODBnet"
            elif subkey_name == "{5EFC6C07-6B87-43FC-9524-F9E967241741}":
                m.name = "GTARockstar"
            else:
                m.name = "UninstallRoot"
            return m
        mock_open_key.side_effect = mock_open_key_side_effect
        
        def mock_query_info_key_side_effect(key):
            if key.name == "UninstallRoot":
                return (2, 0, 0)
            return (0, 0, 0)
        mock_query_info_key.side_effect = mock_query_info_key_side_effect
        
        def mock_enum_key_side_effect(key, index):
            if key.name == "UninstallRoot":
                if index == 0:
                    return "Call of Duty Black Ops Cold War"
                elif index == 1:
                    return "{5EFC6C07-6B87-43FC-9524-F9E967241741}"
            return ""
        mock_enum_key.side_effect = mock_enum_key_side_effect
        
        def mock_query_value_ex_side_effect(key, name):
            if key.name == "CODBnet":
                if name == "DisplayName":
                    return ("Call of Duty Black Ops Cold War", 1)
                elif name == "InstallLocation":
                    return ("D:\\Games\\Call of Duty", 1)
                elif name == "UninstallString":
                    return ("Blizzard Uninstaller.exe", 1)
                elif name == "Publisher":
                    return ("Blizzard Entertainment", 1)
            elif key.name == "GTARockstar":
                if name == "DisplayName":
                    return ("Grand Theft Auto V Enhanced", 1)
                elif name == "InstallLocation":
                    return ("D:\\Games\\GTA V", 1)
                elif name == "UninstallString":
                    return ("uninstall.exe -enableFullMode -uninstall=gta5_gen9", 1)
                elif name == "Publisher":
                    return ("Rockstar Games", 1)
            raise FileNotFoundError()
        mock_query_value_ex.side_effect = mock_query_value_ex_side_effect
        
        # Clear SSD Main launchers first
        self.win.db.disks["SSD Main"].launchers = {}
        self.win.db.save()
        
        # Call remplir_automatiquement
        self.win.remplir_automatiquement()
            
        mock_info.assert_called_once()
        
        # Verify Battle.net was added
        bnet_launcher = self.win.db.disks["SSD Main"].launchers.get("Battle.net")
        self.assertIsNotNone(bnet_launcher)
        self.assertEqual(bnet_launcher.apps[0].name, "Call of Duty Black Ops Cold War")
        self.assertEqual(bnet_launcher.apps[0].size, 5.0)
        
        # Verify Rockstar was added
        rockstar_launcher = self.win.db.disks["SSD Main"].launchers.get("Rockstar")
        self.assertIsNotNone(rockstar_launcher)
        self.assertEqual(rockstar_launcher.apps[0].name, "Grand Theft Auto V Enhanced")
        self.assertEqual(rockstar_launcher.apps[0].size, 5.0)
        
        # Verify Microsoft Store was added
        ms_launcher = self.win.db.disks["SSD Main"].launchers.get("Microsoft Store")
        self.assertIsNotNone(ms_launcher)
        self.assertEqual(ms_launcher.apps[0].name, "Minecraft for Windows")
        self.assertEqual(ms_launcher.apps[0].size, 5.0)


