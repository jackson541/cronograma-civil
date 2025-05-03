from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene,
    QPushButton, QListWidgetItem, QMessageBox, QHBoxLayout, QSlider
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform, QPainter

from project.models import ProjectTemplate
from project.utils.funcs import generate_graph
from project.utils.widgets import CustomGraphicsView

class TemplateDetailsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.template = None
        self.zoom_factor = 1.0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.template_name_label = QLabel("Nome do Modelo: ")
        layout.addWidget(self.template_name_label)

        self.max_days = QLabel()
        layout.addWidget(self.max_days)

        # Graphical representation of services
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

        self.add_service_button = QPushButton("Adicionar Serviço")
        self.add_service_button.clicked.connect(self.go_to_add_service)
        layout.addWidget(self.add_service_button)

        self.create_project_button = QPushButton("Criar Projeto a partir do Modelo")
        self.create_project_button.clicked.connect(self.create_project_from_template)
        layout.addWidget(self.create_project_button)

        self.delete_button = QPushButton("Excluir Modelo")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.delete_template)
        layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_template_list_screen)
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

    def load_template(self, template_id):
        self.template = self.session.query(ProjectTemplate).get(template_id)
        if not self.template:
            self.template_name_label.setText("Modelo não encontrado.")
            return
        
        self.setWindowTitle(self.template.name)

        self.template_name_label.setText(f"Nome do Modelo: {self.template.name}")
        self.max_days.setText(f"Dias do caminho crítico: {self.template.days_to_complete}")

        self.scene.clear()
        if self.template.services:
            generate_graph(
                self.scene, 
                self.template.services, 
                self.main_window.show_service_details_screen, 
                self.template.chart_data
            )
            
        # Reset zoom when loading a new template
        self.reset_zoom()

    def go_to_add_service(self):
        if self.template:
            self.main_window.show_add_template_service_screen(self.template.id)

    def create_project_from_template(self):
        if not self.template:
            return
            
        self.main_window.show_create_project_from_template_screen(self.template.id)
        
    def delete_template(self):
        if not self.template:
            return
        self.main_window.show_delete_template_screen(self.template.id) 