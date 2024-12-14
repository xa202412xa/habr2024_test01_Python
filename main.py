import queue
import threading
import time

# Класс, представляющий задачу
class Task:
    def __init__(self, id, duration):
        self.id = id  # Идентификатор задачи
        self.duration = duration  # Продолжительность задачи

# Класс, представляющий сервер, который выполняет задачи
class Server(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id  # Идентификатор сервера
        self.task = None  # Текущая задача, выполняемая сервером
        self.remaining_time = 0  # Оставшееся время выполнения текущей задачи
        self.lock = threading.Lock()  # Блокировка для синхронизации доступа к задачам

    # Метод для назначения задачи серверу
    def assign_task(self, task):
        with self.lock:
            self.task = task  # Назначение задачи
            self.remaining_time = task.duration  # Установка времени выполнения задачи

    # Метод, выполняющийся в отдельном потоке
    def run(self):
        while True:
            if self.task:
                print(f"Server {self.id} is processing task {self.task.id}")
                while self.remaining_time > 0:
                    time.sleep(1)  # Имитация выполнения задачи
                    self.remaining_time -= 1  # Уменьшение оставшегося времени
                print(f"Server {self.id} finished task {self.task.id}")
                self.task = None  # Освобождение сервера после завершения задачи

# Класс, представляющий распределенную систему с несколькими серверами
class DistributedSystem:
    def __init__(self, num_servers):
        self.servers = [Server(i) for i in range(num_servers)]  # Создание списка серверов
        self.task_queue = queue.Queue()  # Очередь задач
        for server in self.servers:
            server.start()  # Запуск каждого сервера в отдельном потоке

    # Метод для добавления задачи в очередь
    def add_task(self, task):
        self.task_queue.put(task)  # Добавление задачи в очередь
        self.assign_tasks()  # Попытка назначения задач серверам

    # Метод для назначения задач серверам
    def assign_tasks(self):
        for server in self.servers:
            if not server.task and not self.task_queue.empty():
                task = self.task_queue.get()  # Получение задачи из очереди
                server.assign_task(task)  # Назначение задачи серверу

    # Метод для получения статуса всех серверов
    def get_status(self):
        status = []
        for server in self.servers:
            status.append((server.id, server.task.id if server.task else None, server.remaining_time))
        return status

    # Метод для отображения статуса всех серверов
    def display_status(self):
        print("Состояние серверов:")
        for server in self.servers:
            task_status = f"выполняет задание (осталось {server.remaining_time} сек.)" if server.task else "пусто"
            print(f"Сервер {server.id}: {task_status}")
        print("Очередь заданий:", [task.id for task in list(self.task_queue.queue)])

def main():
    num_servers = int(input("Введите количество серверов: "))
    system = DistributedSystem(num_servers)

    # Функция для периодического назначения задач серверам
    def assign_tasks_periodically():
        while True:
            system.assign_tasks()
            time.sleep(1)

    threading.Thread(target=assign_tasks_periodically, daemon=True).start()

    while True:
        command = input("Команда: ")
        if command.startswith("добавить"):
            duration = int(command.split()[1])
            task_id = len(list(system.task_queue.queue)) + 1
            system.add_task(Task(task_id, duration))
        elif command == "статус":
            system.display_status()
        elif command == "выход":
            break

if __name__ == "__main__":
    main()
