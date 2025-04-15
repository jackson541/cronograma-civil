from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox

from project.models import Project


class EditProjectScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit("")

        self.concluded_label = QLabel("Concluido:")
        self.concluded_checkbox = QCheckBox("Concluded")

        self.save_button = QPushButton("Salvar alteração")
        self.save_button.clicked.connect(self.save_project)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_project_details)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.concluded_label)
        layout.addWidget(self.concluded_checkbox)
        layout.addWidget(self.save_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_project(self, project_id):
        self.project_id = project_id
        self.project = self.session.query(Project).get(project_id)
        if not self.project:
            QMessageBox.critical(self, "Error", "project not found.")
            self.close()
            return
        
        self.name_input.setText(self.project.name)
        self.concluded_checkbox.setChecked(self.project.concluded)

    def save_project(self):
        name = self.name_input.text().strip()
        concluded = self.concluded_checkbox.isChecked()

        if not name:
            QMessageBox.warning(self, "Validation Error", "project name cannot be empty.")
            return
        
        self.project.name = name
        self.project.concluded = concluded

        self.session.commit()
        QMessageBox.information(self, "Salvo", "Projeto atualizado.")
        self.back_to_project_details()

    def back_to_project_details(self):
        if self.project:
            self.main_window.show_project_details_screen(self.project.id)
