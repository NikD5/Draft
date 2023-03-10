import numpy as np
from mesa import Agent

from dijkstra_algorithm import dijkstra
from forces import totalforce

# Узел для поиска пути по алгоритму
#  self.pos : позиция в сетке
#  self.done : проверка узла
#  self.exit : проверка на выход
#  self.path : кротчайший путь к узлу
class Node:
def __init__(self, position):
    self.pos = position
    self.done = False
    self.exit = False
    self.path = []

def __str__(self):
    x, y = self.pos
    return f"{x / 6, y / 6}"


# Родительский класс для всех агентов

class Objects (Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.model = model

    def get_position(self):
        return self.pos

class Obstacles(Objects):
    def __init__(self, model, pos):
        super().__init__(model, pos)

class Wall(Objects):
    def __init__(self, model, pos):
        super().__init__(model, pos)

class Exit(Objects):
    def __init__(self, model, pos):
        super().__init__(model, pos)


# Люди в модели

# self.new_pos : цель для перемещения
# self.node : ближайший узел
# self.path : кротчайший путь
# self.dist : длина кротчайшего пути

class Human(Objects):
    def __init__(self, model, pos):
        super().__init__(model, pos)
        getattr(model, f'scheduler').add(self)
        self.new_pos = 0
        self.node = 6 * self.pos[0], 6 * self.pos[1]
        self.path = dijkstra(self.model.grid, self.node)
        self.dist = len(self.path)

# Алгоритм поиска пути
    def dijkstra(self):
        self.path = dijkstra(self.model.grid, self.node)
        self.dist = len(self.path)


# Как я понял, тут вычисление силы взаимодействия между людьми
    def force(self):
        self.new_pos = totalforce(self.pos, self.path[0], self.model.humans)

# Поиск ближайшего узла в сетке
    def get_node(self):
        xs, ys = self.pos
        self.node = int(np.round(xs * 6)), int(np.round(ys * 6))

# Движение агентов в пространстве
    def move(self):
        self.model.space.move_agent(self, self.new_pos)

# Выполнение всех методов для первого шага
    def step(self):
        try:
            self.dijkstra()
            self.get_node()
            self.force()
            self.move()
        except Exception as e:
            print(e)

# Удаление агента
    def saved(self):
        self.model.remove_agent(self)