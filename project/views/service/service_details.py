from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QLabel, QPushButton, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform, QPainter

from project.models import Service
from project.utils.funcs import generate_graph
from project.utils.widgets import CustomGraphicsView


class ServiceDetailsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.service = None
        self.zoom_factor = 1.0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Detalhes do Serviço")
        layout = QVBoxLayout()

        self.service_name_label = QLabel("Serviço: ")
        layout.addWidget(self.service_name_label)

        self.project_name_label = QLabel("Projeto: ")
        layout.addWidget(self.project_name_label)

        self.edit_service_button = QPushButton("Editar")
        self.edit_service_button.clicked.connect(self.go_to_edit_service)
        layout.addWidget(self.edit_service_button)

        self.dependencies_label = QLabel()
        self.dependencies_label.setOpenExternalLinks(False)
        self.dependencies_label.linkActivated.connect(self.handle_link_click)
        layout.addWidget(QLabel("Depende de:"))
        layout.addWidget(self.dependencies_label)

        self.dependents_label = QLabel()
        self.dependents_label.setOpenExternalLinks(False)
        self.dependents_label.linkActivated.connect(self.handle_link_click)
        layout.addWidget(QLabel("Dependentes:"))
        layout.addWidget(self.dependents_label)

        self.max_days = QLabel()
        layout.addWidget(self.max_days)

        # Graphical representation of tasks
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)
        self.view = CustomGraphicsView(self.scene)
        layout.addWidget(self.view)
        
        # Zoom controls
        zoom_layout = QHBoxLayout()
        
        zoom_out_btn = QPushButton("-")
        zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_layout.addWidget(zoom_out_btn)
        
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.zoom_slider_changed)
        zoom_layout.addWidget(self.zoom_slider)
        
        zoom_in_btn = QPushButton("+")
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(zoom_in_btn)
        
        reset_zoom_btn = QPushButton("Reset")
        reset_zoom_btn.clicked.connect(self.reset_zoom)
        zoom_layout.addWidget(reset_zoom_btn)
        
        layout.addLayout(zoom_layout)

        self.add_task_button = QPushButton("Adicionar tarefa")
        self.add_task_button.clicked.connect(self.go_to_add_task)
        layout.addWidget(self.add_task_button)

        self.delete_button = QPushButton("Apagar serviço")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.go_to_delete_service)
        layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_project_details)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_zoom()
        self.zoom_slider.setValue(int(self.zoom_factor * 100))
        
    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_zoom()
        self.zoom_slider.setValue(int(self.zoom_factor * 100))
        
    def reset_zoom(self):
        self.zoom_factor = 1.0
        self.update_zoom()
        self.zoom_slider.setValue(100)
        
    def zoom_slider_changed(self, value):
        self.zoom_factor = value / 100.0
        self.update_zoom()
        
    def update_zoom(self):
        transform = QTransform()
        transform.scale(self.zoom_factor, self.zoom_factor)
        self.view.setTransform(transform)

    def load_service(self, service_id):
        self.service = self.session.query(Service).get(service_id)
        if not self.service:
            self.service_name_label.setText("Serviço não encontrado.")
            return

        self.service_name_label.setText(f"Serviço: {self.service.name}")
        if self.service.project:
            self.project_name_label.setText(f"Projeto: {self.service.project.name}")
        else:
            self.project_name_label.setText(f"Projeto: {self.service.template.name}")
        self.max_days.setText(f"Caminho crítico dias: {self.service.days_to_complete}")

        # Dependencies
        if self.service.dependencies:
            dep_links = ", ".join(
                f"<a href='service:{dep.id}'>{dep.name}</a>" for dep in self.service.dependencies
            )
            self.dependencies_label.setText(dep_links)
        else:
            self.dependencies_label.setText("Sem dependências")

        # Dependents
        if self.service.dependents:
            dep_on_links = ", ".join(
                f"<a href='service:{d.id}'>{d.name}</a>" for d in self.service.dependents
            )
            self.dependents_label.setText(dep_on_links)
        else:
            self.dependents_label.setText("Sem dependentes")

        self.scene.clear()
        if self.service.tasks:
            generate_graph(
                self.scene, 
                self.service.tasks, 
                self.main_window.show_edit_task_screen, 
                self.service.chart_data
            )
        
        # Reset zoom when loading a new service
        self.reset_zoom()

    def back_to_project_details(self):
        if self.service:
            if self.service.project:
                self.main_window.show_project_details_screen(self.service.project_id)
            else:
                self.main_window.show_template_details_screen(self.service.template_id)

    def handle_link_click(self, link):
        if link.startswith("service:"):
            service_id = int(link.split(":")[1])
            self.main_window.show_service_details_screen(service_id)

    def go_to_add_task(self):
        if self.service:
            self.main_window.show_create_task_screen(self.service.id)

    def go_to_edit_service(self):
        if self.service:
            self.main_window.show_edit_service_screen(self.service.id)

    def go_to_delete_service(self):
        if self.service:
            self.main_window.show_delete_service_screen(self.service.id)
