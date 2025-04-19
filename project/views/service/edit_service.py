from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox

from project.models import Service


class EditServiceScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit("")

        self.save_button = QPushButton("Salvar alteração")
        self.save_button.clicked.connect(self.save_project)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_service_details)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_service(self, service_id):
        self.service_id = service_id
        self.service = self.session.query(Service).get(service_id)
        if not self.service:
            QMessageBox.critical(self, "Error", "service not found.")
            self.close()
            return
        
        self.name_input.setText(self.service.name)

    def save_project(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "service name cannot be empty.")
            return
        
        self.service.name = name

        self.session.commit()
        QMessageBox.information(self, "Salvo", "Projeto atualizado.")
        self.back_to_service_details()

    def back_to_service_details(self):
        if self.service:
            self.main_window.show_service_details_screen(self.service.id)
