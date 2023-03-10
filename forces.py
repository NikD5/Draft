import numpy as np

# Вычисляет самодвижущуюся силу от текущего положения к первому узлу на кратчайшем пути агента
def dijkstraforce(pos, targ):
    xs, ys = pos
    xe, ye = targ
    dx, dy = (xe / 6 - xs), (ye / 6 - ys)

# Вычислить угол силы тета
    if np.abs(dx) < 0.00001 or np.abs(dy) < 0.00001:
        if dx > 0.00001:
            theta = 0
        elif dx < -0.00001:
            theta = np.pi
        elif dy > 0.00001:
            theta = np.pi / 2
        elif dy < -0.00001:
            theta = -np.pi / 2
        else:
            return 0, 0
    else:
        if dx > 0 and dy > 0:
            theta = np.arctan(np.abs(dy / dx))
        elif dx < 0 and dy > 0:
            theta = np.pi - np.arctan(np.abs(dy / dx))
        elif dx > 0 and dy < 0:
            theta = -np.arctan(np.abs(dy / dx))
        elif dx < 0 and dy < 0:
            theta = np.pi + np.arctan(np.abs(dy / dx))

    fx, fy = 0.10 * np.cos(theta), 0.10 * np.sin(theta)
    return fx, fy


# Вычисляет взаимодействие между людьми для всех других людей в пределах досягаемости агента.
def bodyforce(pos, humans):
    fx, fy = 0, 0
    xs, ys = pos
    dist = 0

    for human in humans:
        try:
            if human.pos != pos:
                xe, ye = human.pos
                dx, dy = (xe - xs), (ye - ys)
                dist = np.sqrt((dx)**2 + (dy)**2)

                if dist < 1.0:
                    # Calculate force angle theta
                    if np.abs(dx) < 0.00001 or np.abs(dy) < 0.00001:
                        if dx > 0.001:
                            theta = 0
                        elif dx < -0.00001:
                            theta = np.pi
                        elif dy > 0.00001:
                            theta = np.pi / 2
                        elif dy < -0.00001:
                            theta = -np.pi / 2
                    else:
                        if dx > 0 and dy > 0:
                            theta = np.arctan(dy / dx)
                        elif dx < 0 and dy > 0:
                            theta = np.pi - np.arctan(dy / dx)
                        elif dx > 0 and dy < 0:
                            theta = -np.arctan(dy / dx)
                        elif dx < 0 and dy < 0:
                            theta = np.pi + np.arctan(dy / dx)

                    fx -= 0.04 / np.power(dist, 1.8) * np.cos(theta)
                    fy -= 0.04 / np.power(dist, 1.8) * np.sin(theta)
        except Exception as e:
            print(e)

    return (fx, fy)

# Вычисляет и возвращает новое положение агента на основе вычисленных сил и текущего положения.
def totalforce(pos, target, humans):
    dijkstra_x, dijkstra_y = dijkstraforce(pos, target)
    body_x, body_y = bodyforce(pos, humans)
    total_x, total_y = dijkstra_x + body_x, dijkstra_y + body_y

    return pos[0] + total_x, pos[1] + total_y
