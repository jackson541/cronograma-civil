from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene,
    QPushButton, QListWidgetItem, QMessageBox, QHBoxLayout, QSlider
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform, QPainter

from project.models import Project
from project.utils.funcs import generate_graph
from project.utils.widgets import CustomGraphicsView


class ProjectDetailsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.project = None  # Set this before showing
        self.zoom_factor = 1.0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.project_name_label = QLabel("Nome do Projeto: ")
        layout.addWidget(self.project_name_label)

        self.client_name_label = QLabel("Cliente: ")
        layout.addWidget(self.client_name_label)

        self.project_status_label = QLabel("Status: ")
        layout.addWidget(self.project_status_label)

        self.max_days = QLabel()
        layout.addWidget(self.max_days)

        self.edit_project_button = QPushButton("Editar")
        self.edit_project_button.clicked.connect(self.go_to_edit_project)
        layout.addWidget(self.edit_project_button)
        
        self.delete_project_button = QPushButton("Excluir Projeto")
        self.delete_project_button.setStyleSheet("background-color: red; color: white;")
        self.delete_project_button.clicked.connect(self.delete_project)
        layout.addWidget(self.delete_project_button)

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

        self.add_service_button = QPushButton("Adicionar serviço")
        self.add_service_button.clicked.connect(self.go_to_add_service)
        layout.addWidget(self.add_service_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_project_screen)
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

    def load_project(self, project_id):
        self.project = self.session.query(Project).get(project_id)
        if not self.project:
            self.project_name_label.setText("Projeto não encontrado.")
            return
        
        self.setWindowTitle(self.project.name)

        self.project_name_label.setText(f"Nome do Projeto: {self.project.name}")
        self.client_name_label.setText(f"Cliente: {self.project.client.name}")
        status = "Concluído" if self.project.concluded else "Em Andamento"
        self.project_status_label.setText(f"Status: {status}")

        self.max_days.setText(f"Caminho crítico dias: {self.project.days_to_complete}")

        self.scene.clear()
        if self.project.services:
            generate_graph(
                self.scene, 
                self.project.services, 
                self.main_window.show_service_details_screen, 
                self.project.chart_data
            )
            
        # Reset zoom when loading a new project
        self.reset_zoom()

    def go_to_add_service(self):
        if self.project:
            self.main_window.show_create_service_screen(self.project.id)

    def go_to_edit_project(self):
        if self.project:
            self.main_window.show_edit_project_screen(self.project.id)
            
    def delete_project(self):
        if not self.project:
            return
            
        # Go directly to delete screen without confirmation
        self.main_window.show_delete_project_screen(self.project.id)

