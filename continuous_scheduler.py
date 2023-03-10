import numpy as np
import random as rnd
# Планировщик, который активирует агентов в порядке расстояния от пути до выхода.
# Ближайшие агенты активируются первыми, чтобы максимизировать поток через выход.
class DistanceScheduler:
    def __init__(self, model):
        self.steps = 0
        self.agents = []
        self.model = model

    def add(self, agent):
        self.agents.append(agent)

    def remove(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)

# Сортирует агентов в порядке расстояния до выхода, а затем выполняет шаги
    def step(self):
        try:
            self.agents.sort(key=lambda x: x.dist)
        except Exception as e:
            print(e)

        for agent in self.agents:
            try:
                agent.step()
            except Exception as e:
                print(e)


# Удаляет агентов, если они достигли выхода
            for exit in self.model.exits:
                x, y = exit.pos[0] * 6 + 1, exit.pos[1] * 6 + 1
                if agent.node == (x, y):
                    try:
                        agent.saved()
                    except Exception as e:
                        print(e)

    def get_agent_count(self):
        return len(self.agents)
