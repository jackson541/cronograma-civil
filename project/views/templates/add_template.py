from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox
)

from project.models import ProjectTemplate

class AddTemplateScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Project Template")
        layout = QVBoxLayout()

        # Template Name
        layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Buttons
        self.save_button = QPushButton("Save Template")
        self.save_button.clicked.connect(self.save_template)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.main_window.show_template_list_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def save_template(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Template name cannot be empty.")
            return

        template = ProjectTemplate(name=name)
        self.session.add(template)
        self.session.commit()

        QMessageBox.information(self, "Success", "Template added successfully!")
        self.name_input.clear()
        self.main_window.show_template_list_screen() 