from PySide6.QtWidgets import QInputDialog, QFileDialog, QMenuBar, QMenu, QMainWindow, QApplication, QTextEdit
from PySide6.QtGui import QIcon, QAction, QTextCursor, QColor
from PySide6.QtCore import Qt
import sys

class TextEditor(QTextEdit):
    """Custom TextEdit widget with added functionality for the highlighting of searched text"""

    def highlight_text(self, search_text):
        """Highlights all occurrences of the selected text"""
        # Check if nothing typed in search text
        if not search_text:
            return 
        # Move cursor of editor to the beginning of text
        self.moveCursor(QTextCursor.MoveOperation.Start)
        highlight_color = QColor(Qt.yellow)
        # list to store the occurrences of text
        selected_text = []

        # Loop through the editor and find the searched text
        while self.find(search_text):
            # create instance of extraselection to set hihlighting and location
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(highlight_color)
            selection.cursor = self.textCursor()
            selected_text.append(selection)

        self.setExtraSelections(selected_text)


class FileHandler:
    """Handles the file read and write operations"""
    @staticmethod
    def read_file(file_path):
        """Reads the contents of the file"""
        try:
            with open(file_path, "r") as file:
                text = file.read()
            return text
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    @staticmethod
    def write_file(file_path, text):
        """Writes the contents to the file"""
        try:
            with open(file_path, "w") as file:
                file.write(text)
        except Exception as e:
            print(f"Error writing to file: {e}")


class MainWindow(QMainWindow):
    """Class to create the main notepad app"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad")
        self.setGeometry(200, 300, 800, 600)
        self.initUI()

    def initUI(self):
        """Add elements of the GUI"""
        self.editor = TextEditor()
        self.setCentralWidget(self.editor)

        self.current_file = None

        menu_bar = QMenuBar(self)
        menu_bar.setNativeMenuBar(False)
        self.setMenuBar(menu_bar)
        
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)

        file_menu.addAction(self.create_action("New", self.new_file))
        file_menu.addAction(self.create_action("Open", self.open_file))
        file_menu.addAction(self.create_action("Save", self.save_file))
        file_menu.addAction(self.create_action("Save as", self.save_file_as))
        file_menu.addAction(self.create_action("Exit", self.close))

        edit_menu.addAction(self.create_action("Undo", self.editor.undo))
        edit_menu.addAction(self.create_action("Redo", self.editor.redo))
        edit_menu.addAction(self.create_action("Cut", self.editor.cut))
        edit_menu.addAction(self.create_action("Copy", self.editor.copy))
        edit_menu.addAction(self.create_action("Paste", self.editor.paste))
        edit_menu.addAction(self.create_action("Find", self.find_text))


    def create_action(self, name, action):
        """Define the action and trigger for the menu"""
        new_action = QAction(name, self)
        new_action.triggered.connect(action)
        return new_action

    def new_file(self):
        """Clears the editor for a new file"""
        self.editor.clear()
        self.current_file = None

    def open_file(self):
        """Open existing file and print contents on the notepad"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", 
                                                   "", "All Files(*);; Python Files(*.py)")

        if file_path:
            content = FileHandler.read_file(file_path)
            self.editor.setText(content)
            self.current_file = file_path

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File",
                                                "", "All Files(*);; Python Files(*.py)")
        if file_path:
            FileHandler.write_file(file_path, self.editor.toPlainText())
        
            self.current_file = file_path

    def save_file(self):
        if self.current_file:
            FileHandler.write_file(self.current_file, self.editor.toPlainText())
        else:
            self.save_file_as()

    def find_text(self):
        search_text, ok = QInputDialog.getText(self, "Find text", "Search for")

        if ok:
            self.editor.highlight_text(search_text)



# Initialize the app and main window, then run the main loop
app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()