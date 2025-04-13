from collections import defaultdict, deque
import random

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton,
    QListWidgetItem
)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt, QPointF

from project.models import Service


class ServiceDetailsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.service = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Service Details")
        layout = QVBoxLayout()

        self.service_name_label = QLabel("Service: ")
        layout.addWidget(self.service_name_label)

        self.project_name_label = QLabel("Project: ")
        layout.addWidget(self.project_name_label)

        self.dependencies_label = QLabel()
        self.dependencies_label.setOpenExternalLinks(False)
        self.dependencies_label.linkActivated.connect(self.handle_link_click)
        layout.addWidget(QLabel("Depends on:"))
        layout.addWidget(self.dependencies_label)

        self.dependents_label = QLabel()
        self.dependents_label.setOpenExternalLinks(False)
        self.dependents_label.linkActivated.connect(self.handle_link_click)
        layout.addWidget(QLabel("Dependents:"))
        layout.addWidget(self.dependents_label)

        self.max_days = QLabel()
        self.max_days.setOpenExternalLinks(False)
        self.max_days.linkActivated.connect(self.handle_link_click)
        layout.addWidget(self.max_days)

        # Graphical representation of tasks
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.add_task_button = QPushButton("Adicionar tarefa")
        self.add_task_button.clicked.connect(self.go_to_add_task)

        layout.addWidget(self.add_task_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_project_details)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_service(self, service_id):
        self.service = self.session.query(Service).get(service_id)
        if not self.service:
            self.service_name_label.setText("Service not found.")
            return

        self.service_name_label.setText(f"Service: {self.service.name}")
        self.project_name_label.setText(f"Project: {self.service.project.name}")

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

        self.generate_graph()

    def generate_graph(self):
        self.scene.clear()
        if not self.service.tasks:
            self.max_days.setText("Sem tarefas")
            return
        
        # --- Build dependency graph ---
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        tasks = {task.id: task for task in self.service.tasks}

        for task in self.service.tasks:
            for dep in task.dependencies:
                graph[dep.id].append(task.id)
                in_degree[task.id] += 1
                out_degree[dep.id] += 1

        # --- Topological sort to get levels ---
        levels = defaultdict(list)
        topological_order = []
        queue = deque()

        # Start with tasks with no dependencies
        for task_id in tasks:
            if in_degree[task_id] == 0:
                queue.append((task_id, 0))
        
        while queue:
            task_id, level = queue.popleft()
            levels[level].append(task_id)
            topological_order.append(task_id)
            for neighbor in graph[task_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append((neighbor, level + 1))

        # --- Calculate max days ---
        # Track max duration and previous task
        distances = {task_id: tasks[task_id].days_to_complete for task_id in tasks}
        previous = {task_id: None for task_id in tasks}

        for task_id in topological_order:
            for neighbor in graph[task_id]:
                new_dist = distances[task_id] + tasks[neighbor].days_to_complete
                if new_dist > distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = task_id

        # Find leaf with longest duration
        leaf_nodes = [task.id for task in self.service.tasks if out_degree[task.id] == 0]
        end_node = max(leaf_nodes, key=lambda tid: distances[tid])
        self.max_days.setText(f"Caminho crítico dias: {distances[end_node]}")

        # Backtrack path
        critical_path = []
        current = end_node
        while current is not None:
            critical_path.insert(0, current)
            current = previous[current]

        critical_edges = set()
        for i in range(len(critical_path) - 1):
            critical_edges.add((critical_path[i], critical_path[i + 1]))


        # --- Place task nodes in screen ---
        task_items = {}
        spacing_x = 200
        spacing_y = 100

        for level in sorted(levels.keys()):
            for i, task_id in enumerate(levels[level]):
                task = tasks[task_id]
                x = level * spacing_x
                y = i * spacing_y

                # Task rectangle
                rect = QGraphicsRectItem(0, 0, 140, 60)
                rect.setBrush(self.random_pastel_color())
                rect.setPos(x, y)
                self.scene.addItem(rect)

                # Task name (inside the box)
                label = QGraphicsTextItem(task.name)
                label.setDefaultTextColor(Qt.black)
                label.setParentItem(rect)
                label.setPos(10, 10)

                # Days to complete (below the box)
                days_label = QGraphicsTextItem(f"{task.days_to_complete} dia(s)")
                days_label.setDefaultTextColor(Qt.darkGray)
                days_label.setPos(x + 10, y + 65)  # just below the rectangle
                self.scene.addItem(days_label)

                task_items[task_id] = rect

        # --- Draw dependency lines ---
        for task in self.service.tasks:
            for dep in task.dependencies:
                start_item = task_items.get(dep.id)
                end_item = task_items.get(task.id)
                if start_item and end_item:
                    start_rect = start_item.sceneBoundingRect()
                    end_rect = end_item.sceneBoundingRect()

                    start_point = QPointF(start_rect.right(), start_rect.center().y())
                    end_point = QPointF(end_rect.left(), end_rect.center().y())

                    line = QGraphicsLineItem(start_point.x(), start_point.y(),
                                            end_point.x(), end_point.y())
                    
                    if (dep.id, task.id) in critical_edges:
                        pen = QPen(Qt.red, 3)
                    else:
                        pen = QPen(Qt.black, 2)

                    line.setPen(pen)
                    self.scene.addItem(line)


    def random_pastel_color(self):
        base = 200  # keep colors light
        r = random.randint(base, 255)
        g = random.randint(base, 255)
        b = random.randint(base, 255)
        return QColor(r, g, b)


    def back_to_project_details(self):
        if self.service:
            self.main_window.show_project_details_screen(self.service.project_id)

    def handle_link_click(self, link):
        if link.startswith("service:"):
            service_id = int(link.split(":")[1])
            self.main_window.show_service_details_screen(service_id)

    def go_to_add_task(self):
        if self.service:
            self.main_window.show_create_task_screen(self.service.id)

    def open_task_detail(self, item):
        task_id = item.data(Qt.UserRole)
        self.main_window.show_task_details_screen(task_id)
