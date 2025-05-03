from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox

from project.models import ProjectTemplate, Service, Task


class DeleteTemplateScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.template = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Excluir Modelo")
        layout = QVBoxLayout()

        # Title at the top with larger font
        self.title_label = QLabel("EXCLUIR MODELO")
        self.title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: red;")
        layout.addWidget(self.title_label)

        self.name_label = QLabel()
        self.question_label = QLabel("Tem certeza de que deseja excluir esse modelo de projeto?")
        self.warning_label = QLabel("Isto excluirá todos os serviços e tarefas associados ao modelo.")
        self.warning_label.setStyleSheet("color: red;")

        self.delete_button = QPushButton("Excluir Modelo")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.delete_template)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_templates)

        layout.addWidget(self.name_label)
        layout.addWidget(self.question_label)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_template(self, template_id):
        self.template = self.session.query(ProjectTemplate).get(template_id)
        if not self.template:
            QMessageBox.critical(self, "Erro", "Modelo não encontrado.")
            self.back_to_templates()
            return
        
        self.setWindowTitle(f"Excluir Modelo: {self.template.name}")
        self.name_label.setText(f"Nome: {self.template.name}")

    def delete_template(self):
        if not self.template:
            self.back_to_templates()
            return
            
        # Delete all related services and tasks
        for service in self.template.services:
            # Delete all tasks associated with this service
            for task in service.tasks:
                self.session.delete(task)
            # Delete the service itself
            self.session.delete(service)
            
        # Delete the template
        self.session.delete(self.template)
        self.session.commit()
        
        QMessageBox.information(self, "Concluído", "Modelo de projeto excluído com sucesso.")
        self.back_to_templates()

    def back_to_templates(self):
        self.main_window.show_template_list_screen() 