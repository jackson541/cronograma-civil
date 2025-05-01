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
        self.setWindowTitle("Adicionar Modelo de Projeto")
        layout = QVBoxLayout()

        # Template Name
        layout.addWidget(QLabel("Nome:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Buttons
        self.save_button = QPushButton("Salvar Modelo")
        self.save_button.clicked.connect(self.save_template)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_template_list_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def save_template(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Erro de Validação", "O nome do modelo não pode estar vazio.")
            return

        template = ProjectTemplate(name=name)
        self.session.add(template)
        self.session.commit()

        QMessageBox.information(self, "Sucesso", "Modelo adicionado com sucesso!")
        self.name_input.clear()
        self.main_window.show_template_list_screen() 