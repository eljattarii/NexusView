# =============================================================================
# ui_file_browser.py
# =============================================================================

import os
import shutil
import subprocess

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTreeView,
    QHeaderView,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QFileDialog,
    QMenu,
    QTreeWidget,
    QTreeWidgetItem,
)

from PyQt6.QtGui import (
    QFileSystemModel,
    QAction,
)

from PyQt6.QtCore import (
    QDir,
    Qt,
)

from backend_adb import ADBManager


# =============================================================================
# FILE BROWSER WIDGET
# =============================================================================

class FileBrowserWidget(QWidget):

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------------------------------------------------------------------
        # BACKEND
        # ---------------------------------------------------------------------

        self.adb = ADBManager()

        # ---------------------------------------------------------------------
        # PHONE PATH
        # ---------------------------------------------------------------------

        self.current_phone_path = "/sdcard"

        # ---------------------------------------------------------------------
        # OBJECT NAME
        # ---------------------------------------------------------------------

        self.setObjectName("fileBrowserWidget")

        # ---------------------------------------------------------------------
        # MAIN LAYOUT
        # ---------------------------------------------------------------------

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            16,
            16,
            16,
            16
        )

        self.main_layout.setSpacing(14)

        # ---------------------------------------------------------------------
        # TITLE
        # ---------------------------------------------------------------------

        self.title_label = QLabel(
            "File Browser"
        )

        self.title_label.setObjectName(
            "fileBrowserTitle"
        )

        self.main_layout.addWidget(
            self.title_label
        )

        # ---------------------------------------------------------------------
        # BUILD UI
        # ---------------------------------------------------------------------

        self.build_local_browser()

        self.build_phone_browser()

    # =========================================================================
    # LOCAL FILE BROWSER
    # =========================================================================

    def build_local_browser(self):

        local_title = QLabel(
            "Computer Files"
        )

        local_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #89b4fa;
        """)

        self.main_layout.addWidget(local_title)

        # ---------------------------------------------------------------------
        # BUTTONS
        # ---------------------------------------------------------------------

        button_layout = QHBoxLayout()

        self.button_refresh_local = QPushButton(
            "Refresh"
        )

        self.button_new_folder = QPushButton(
            "New Folder"
        )

        button_layout.addWidget(
            self.button_refresh_local
        )

        button_layout.addWidget(
            self.button_new_folder
        )

        self.main_layout.addLayout(
            button_layout
        )

        # ---------------------------------------------------------------------
        # MODEL
        # ---------------------------------------------------------------------

        self.model = QFileSystemModel()

        self.model.setRootPath(
            QDir.homePath()
        )

        # ---------------------------------------------------------------------
        # TREE
        # ---------------------------------------------------------------------

        self.tree_view = QTreeView()

        self.tree_view.setModel(
            self.model
        )

        self.tree_view.hideColumn(2)

        self.tree_view.hideColumn(3)

        self.tree_view.setRootIndex(
            self.model.index(QDir.homePath())
        )

        self.tree_view.setAnimated(True)

        self.tree_view.setSortingEnabled(True)

        self.tree_view.setAlternatingRowColors(True)

        self.tree_view.setIndentation(18)

        self.tree_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.tree_view.customContextMenuRequested.connect(
            self.show_local_context_menu
        )

        self.tree_view.doubleClicked.connect(
            self.open_local_item
        )

        self.tree_view.header().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.main_layout.addWidget(
            self.tree_view
        )

        # ---------------------------------------------------------------------
        # SIGNALS
        # ---------------------------------------------------------------------

        self.button_refresh_local.clicked.connect(
            self.refresh_local_files
        )

        self.button_new_folder.clicked.connect(
            self.create_local_folder
        )

    # =========================================================================
    # PHONE FILE BROWSER
    # =========================================================================

    def build_phone_browser(self):

        phone_title = QLabel(
            "Phone Files"
        )

        phone_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #89b4fa;
            margin-top: 12px;
        """)

        self.main_layout.addWidget(phone_title)

        # ---------------------------------------------------------------------
        # BUTTONS
        # ---------------------------------------------------------------------

        button_layout = QHBoxLayout()

        self.button_refresh_phone = QPushButton(
            "Refresh"
        )

        self.button_upload_phone = QPushButton(
            "Upload"
        )

        self.button_new_phone_folder = QPushButton(
            "New Folder"
        )

        self.button_back_phone = QPushButton(
            "Back"
        )

        button_layout.addWidget(
            self.button_refresh_phone
        )

        button_layout.addWidget(
            self.button_upload_phone
        )

        button_layout.addWidget(
            self.button_new_phone_folder
        )

        button_layout.addWidget(
            self.button_back_phone
        )

        self.main_layout.addLayout(
            button_layout
        )

        # ---------------------------------------------------------------------
        # CURRENT PATH LABEL
        # ---------------------------------------------------------------------

        self.phone_path_label = QLabel(
            self.current_phone_path
        )

        self.phone_path_label.setStyleSheet("""
            color: #a6adc8;
            padding: 6px;
        """)

        self.main_layout.addWidget(
            self.phone_path_label
        )

        # ---------------------------------------------------------------------
        # PHONE TREE
        # ---------------------------------------------------------------------

        self.phone_tree = QTreeWidget()

        self.phone_tree.setColumnCount(2)

        self.phone_tree.setHeaderLabels([
            "Name",
            "Type"
        ])

        self.phone_tree.setAlternatingRowColors(True)

        self.phone_tree.setMinimumHeight(260)

        self.phone_tree.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.phone_tree.customContextMenuRequested.connect(
            self.show_phone_context_menu
        )

        self.phone_tree.itemDoubleClicked.connect(
            self.open_phone_item
        )

        self.phone_tree.header().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.main_layout.addWidget(
            self.phone_tree
        )

        # ---------------------------------------------------------------------
        # SIGNALS
        # ---------------------------------------------------------------------

        self.button_refresh_phone.clicked.connect(
            self.load_phone_files
        )

        self.button_upload_phone.clicked.connect(
            self.upload_to_phone
        )

        self.button_new_phone_folder.clicked.connect(
            self.create_phone_folder
        )

        self.button_back_phone.clicked.connect(
            self.go_back_phone_folder
        )

    # =========================================================================
    # LOCAL CONTEXT MENU
    # =========================================================================

    def show_local_context_menu(self, position):

        index = self.tree_view.indexAt(position)

        if not index.isValid():
            return

        file_path = self.model.filePath(index)

        menu = QMenu()

        action_open = QAction("Open", self)

        action_rename = QAction("Rename", self)

        action_delete = QAction("Delete", self)

        menu.addAction(action_open)

        menu.addAction(action_rename)

        menu.addAction(action_delete)

        action = menu.exec(
            self.tree_view.viewport().mapToGlobal(position)
        )

        if action == action_open:

            self.open_path(file_path)

        elif action == action_rename:

            self.rename_local_item(file_path)

        elif action == action_delete:

            self.delete_local_item(file_path)

    # =========================================================================
    # PHONE CONTEXT MENU
    # =========================================================================

    def show_phone_context_menu(self, position):

        item = self.phone_tree.itemAt(position)

        if not item:
            return

        file_data = item.data(
            0,
            Qt.ItemDataRole.UserRole
        )

        menu = QMenu()

        action_download = QAction(
            "Download",
            self
        )

        action_rename = QAction(
            "Rename",
            self
        )

        action_delete = QAction(
            "Delete",
            self
        )

        menu.addAction(action_download)

        if file_data["is_dir"]:

            action_download_folder = QAction(
                "Download Folder",
                self
            )

            menu.addAction(
                action_download_folder
            )

        menu.addAction(action_rename)

        menu.addAction(action_delete)

        action = menu.exec(
            self.phone_tree.viewport().mapToGlobal(position)
        )

        if action == action_download:

            self.download_phone_file(item)

        elif (
            file_data["is_dir"] and
            action == action_download_folder
        ):

            self.download_phone_folder(item)

        elif action == action_rename:

            self.rename_phone_item(item)

        elif action == action_delete:

            self.delete_phone_item(item)

    # =========================================================================
    # LOAD PHONE FILES
    # =========================================================================

    def load_phone_files(self):

        self.phone_tree.clear()

        devices = self.adb.get_connected_devices()

        if not devices:

            QMessageBox.warning(
                self,
                "No Device",
                "Please connect a phone first."
            )

            return

        device = devices[0]

        files = self.adb.list_phone_files(
            device,
            self.current_phone_path
        )

        self.phone_path_label.setText(
            self.current_phone_path
        )

        for file_data in files:

            item = QTreeWidgetItem()

            item.setText(
                0,
                file_data["name"]
            )

            item.setText(
                1,
                "Folder" if file_data["is_dir"] else "File"
            )

            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                file_data
            )

            self.phone_tree.addTopLevelItem(item)

    # =========================================================================
    # OPEN PHONE ITEM
    # =========================================================================

    def open_phone_item(self, item):

        file_data = item.data(
            0,
            Qt.ItemDataRole.UserRole
        )

        if file_data["is_dir"]:

            self.current_phone_path = file_data["path"]

            self.load_phone_files()

            return

        self.download_phone_file(item)

    # =========================================================================
    # GO BACK PHONE FOLDER
    # =========================================================================

    def go_back_phone_folder(self):

        if self.current_phone_path == "/sdcard":
            return

        parent = os.path.dirname(
            self.current_phone_path
        )

        if not parent:
            parent = "/sdcard"

        self.current_phone_path = parent

        self.load_phone_files()

    # =========================================================================
    # DOWNLOAD PHONE FILE
    # =========================================================================

    def download_phone_file(self, item):

        file_data = item.data(
            0,
            Qt.ItemDataRole.UserRole
        )

        if file_data["is_dir"]:
            return

        save_path = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder"
        )

        if not save_path:
            return

        devices = self.adb.get_connected_devices()

        if not devices:
            return

        device = devices[0]

        success = self.adb.pull_file(
            device,
            file_data["path"],
            save_path
        )

        if success:

            QMessageBox.information(
                self,
                "Download Complete",
                "File downloaded successfully."
            )

            self.load_phone_files()

    # =========================================================================
    # DOWNLOAD PHONE FOLDER
    # =========================================================================

    def download_phone_folder(self, item):

        file_data = item.data(
            0,
            Qt.ItemDataRole.UserRole
        )

        if not file_data["is_dir"]:
            return

        save_path = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder"
        )

        if not save_path:
            return

        devices = self.adb.get_connected_devices()

        if not devices:
            return

        device = devices[0]

        success = self.adb.pull_file(
            device,
            file_data["path"],
            save_path
        )

        if success:

            QMessageBox.information(
                self,
                "Download Complete",
                "Folder downloaded successfully."
            )

            self.load_phone_files()

    # =========================================================================
    # DELETE PHONE ITEM
    # =========================================================================

    def delete_phone_item(self, item):

        file_data = item.data(
            0,
            Qt.ItemDataRole.UserRole
        )

        confirm = QMessageBox.question(
            self,
            "Delete",
            f"Delete:\n{file_data['name']} ?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        devices = self.adb.get_connected_devices()

        if not devices:
            return

        device = devices[0]

        success = self.adb.delete_phone_file(
            device,
            file_data["path"]
        )

        if success:

            self.load_phone_files()

    # =========================================================================
    # RENAME PHONE ITEM
    # =========================================================================

    def rename_phone_item(self, item):

        file_data = item.data(
            0,
            Qt.ItemDataRole.UserRole
        )

        new_name, ok = QInputDialog.getText(
            self,
            "Rename",
            "New name:"
        )

        if not ok or not new_name:
            return

        old_path = file_data["path"]

        parent = os.path.dirname(old_path)

        new_path = f"{parent}/{new_name}"

        devices = self.adb.get_connected_devices()

        if not devices:
            return

        device = devices[0]

        success = self.adb.rename_phone_file(
            device,
            old_path,
            new_path
        )

        if success:

            self.load_phone_files()

    # =========================================================================
    # CREATE PHONE FOLDER
    # =========================================================================

    def create_phone_folder(self):

        folder_name, ok = QInputDialog.getText(
            self,
            "New Folder",
            "Folder name:"
        )

        if not ok or not folder_name:
            return

        devices = self.adb.get_connected_devices()

        if not devices:
            return

        device = devices[0]

        path = (
            f"{self.current_phone_path}/{folder_name}"
        )

        success = self.adb.create_phone_folder(
            device,
            path
        )

        if success:

            self.load_phone_files()

    # =========================================================================
    # UPLOAD FILE TO PHONE
    # =========================================================================

    def upload_to_phone(self):

        devices = self.adb.get_connected_devices()

        if not devices:

            QMessageBox.warning(
                self,
                "No Device",
                "Please connect a phone first."
            )

            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File"
        )

        if not file_path:
            return

        device = devices[0]

        success = self.adb.push_file(
            device,
            file_path,
            self.current_phone_path
        )

        if success:

            QMessageBox.information(
                self,
                "Upload Complete",
                "File uploaded successfully."
            )

            self.load_phone_files()

    # =========================================================================
    # OPEN LOCAL ITEM
    # =========================================================================

    def open_local_item(self, index):

        file_path = self.model.filePath(index)

        self.open_path(file_path)

    # =========================================================================
    # OPEN PATH
    # =========================================================================

    def open_path(self, path):

        try:

            if os.name == "nt":

                os.startfile(path)

            else:

                subprocess.Popen(["xdg-open", path])

        except Exception as error:

            QMessageBox.critical(
                self,
                "Open Error",
                str(error)
            )

    # =========================================================================
    # DELETE LOCAL ITEM
    # =========================================================================

    def delete_local_item(self, path):

        confirm = QMessageBox.question(
            self,
            "Delete",
            f"Delete:\n{path} ?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:

            if os.path.isfile(path):

                os.remove(path)

            elif os.path.isdir(path):

                shutil.rmtree(path)

            self.refresh_local_files()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Delete Error",
                str(error)
            )

    # =========================================================================
    # RENAME LOCAL ITEM
    # =========================================================================

    def rename_local_item(self, old_path):

        new_name, ok = QInputDialog.getText(
            self,
            "Rename",
            "New name:"
        )

        if not ok or not new_name:
            return

        try:

            folder = os.path.dirname(old_path)

            new_path = os.path.join(
                folder,
                new_name
            )

            os.rename(old_path, new_path)

            self.refresh_local_files()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Rename Error",
                str(error)
            )

    # =========================================================================
    # CREATE LOCAL FOLDER
    # =========================================================================

    def create_local_folder(self):

        folder_name, ok = QInputDialog.getText(
            self,
            "New Folder",
            "Folder name:"
        )

        if not ok or not folder_name:
            return

        try:

            path = os.path.join(
                QDir.homePath(),
                folder_name
            )

            os.makedirs(path, exist_ok=True)

            self.refresh_local_files()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Folder Error",
                str(error)
            )

    # =========================================================================
    # REFRESH LOCAL FILES
    # =========================================================================

    def refresh_local_files(self):

        self.model.setRootPath("")

        self.model.setRootPath(
            QDir.homePath()
        )