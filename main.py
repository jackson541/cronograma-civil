import sys

from PyQt5.QtWidgets import QApplication, QLabel

from project.views.dashboard import MainWindow
from project.models import session

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow(session)
    window.show()
    sys.exit(app.exec_())

    # Create and add new objects
    # task1 = Task(name="Design UI")
    # session.add(task1)
    # session.commit()

    # all_tasks = session.query(Task).all()
    # print("All tasks in the database:")
    # for task in all_tasks:
    #     print(f"Task ID: {task.id}, Task Name: {task.name}")

# app = QApplication([])
# label = QLabel('Hello World!')
# label.show()
# app.exec()
