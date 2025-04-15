from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

from project.models import Client


class EditClientScreen(QWidget):
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
        self.save_button.clicked.connect(self.save_client)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_list_client_screen)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_client(self, client_id):
        self.client_id = client_id
        self.client = self.session.query(Client).get(client_id)
        if not self.client:
            QMessageBox.critical(self, "Error", "Client not found.")
            self.close()
            return
        
        self.name_input.setText(self.client.name)
        self.name_input.setFocus()

    def save_client(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Client name cannot be empty.")
            return
        
        self.client.name = name

        self.session.commit()
        QMessageBox.information(self, "Salvo", "Cliente atualizado.")
        self.main_window.show_list_client_screen()
