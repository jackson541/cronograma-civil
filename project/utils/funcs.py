from collections import defaultdict, deque
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QColor
import random

from project.utils.widgets import CustomRectItem


def compute_critical_path(tasks_list):
    tasks = {t.id: t for t in tasks_list}
    graph = defaultdict(list)
    in_deg = defaultdict(int)
    out_deg = defaultdict(int)

    # Build graph
    for t in tasks_list:
        for d in t.dependencies:
            graph[d.id].append(t.id)
            in_deg[t.id] += 1
            out_deg[d.id] += 1

    # Topological sort with level tracking
    queue = deque((tid, 0) for tid in tasks if in_deg[tid] == 0)
    top_order, levels = [], defaultdict(list)

    while queue:
        tid, lvl = queue.popleft()
        top_order.append(tid)
        levels[lvl].append(tid)
        for neighbor in graph[tid]:
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0:
                queue.append((neighbor, lvl + 1))

    # Longest path calculation
    dist = {tid: tasks[tid].days_to_complete for tid in tasks}
    prev = {tid: None for tid in tasks}

    for tid in top_order:
        for neighbor in graph[tid]:
            new_dist = dist[tid] + tasks[neighbor].days_to_complete
            if new_dist > dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = tid

    # Get critical path
    leaves = [tid for tid in tasks if out_deg[tid] == 0]
    print('leaves', leaves)
    end = max(leaves, key=lambda tid: dist[tid])

    path = []
    while end:
        path.insert(0, end)
        end = prev[end]

    return path, levels, dist[path[-1]]


def generate_graph(scene, items, callback_function, chart_data):
    # --- Place item nodes in screen ---
    items_dict = {}
    spacing_x = 200
    spacing_y = 100

    items = {item.id: item for item in items}
    levels = chart_data['levels']
    levels = {int(level): items for level, items in levels.items()}

    for level in sorted(levels.keys()):
        for i, item_id in enumerate(levels[level]):
            item = items[item_id]
            x = level * spacing_x
            y = i * spacing_y

            # item rectangle
            rect = CustomRectItem(
                item, 
                (0, 0, 140, 60),
                random_pastel_color(),
                (x, y),
                callback_function
            )
            scene.addItem(rect)

            # item name (inside the box)
            label = QGraphicsTextItem(item.name)
            label.setDefaultTextColor(Qt.black)
            label.setParentItem(rect)
            label.setPos(10, 10)

            # Days to complete (below the box)
            days_label = QGraphicsTextItem(f"{item.days_to_complete} dia(s)")
            days_label.setDefaultTextColor(Qt.darkGray)
            days_label.setPos(x + 10, y + 65)  # just below the rectangle
            scene.addItem(days_label)

            items_dict[item_id] = rect

    # --- Draw dependency lines ---
    path = chart_data['path']
    edges = {(path[i], path[i+1]) for i in range(len(path) - 1)}
    for item in items.values():
        for dep in item.dependencies:
            start_item = items_dict.get(dep.id)
            end_item = items_dict.get(item.id)
            if start_item and end_item:
                start_rect = start_item.sceneBoundingRect()
                end_rect = end_item.sceneBoundingRect()

                start_point = QPointF(start_rect.right(), start_rect.center().y())
                end_point = QPointF(end_rect.left(), end_rect.center().y())

                line = QGraphicsLineItem(start_point.x(), start_point.y(),
                                        end_point.x(), end_point.y())
                
                if (dep.id, item.id) in edges:
                    pen = QPen(Qt.red, 3)
                else:
                    pen = QPen(Qt.black, 2)

                line.setPen(pen)
                scene.addItem(line)


def random_pastel_color():
    base = 200  # keep colors light
    r = random.randint(base, 255)
    g = random.randint(base, 255)
    b = random.randint(base, 255)
    return QColor(r, g, b)
