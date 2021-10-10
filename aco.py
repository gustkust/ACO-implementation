import random
import sys
import math


def euclidean_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def points_to_matrix(filename):
    with open(filename, "r") as f:
        point_number = int(f.readline())
        points = [[float(number) for number in line.split()[1:]] for line in f.read().splitlines()]
    matrix = [[] for i in range(point_number)]
    for number, point in enumerate(points):
        for n in range(number):
            matrix[number].append(matrix[n][number])
        matrix[number].append(-1)
        for n in range(number + 1, point_number):
            matrix[number].append(euclidean_dist(point[0], point[1], points[n][0], points[n][1]))
    return matrix


def create_instance(filename, n, dist):
    with open(filename, "w") as f:
        f.write(str(n) + "\n")
        for i in range(n):
            f.write(str(i + 1) + " " + str(random.randint(0, dist)) + " " + str(random.randint(0, dist)) + "\n")


def greedy_method(matrix, start):
    path = [start]
    curr_sum = 0
    curr_point = start
    visited = [False] * len(matrix)
    visited[start] = True
    visited_points = 1
    matrix_size = len(matrix)
    while visited_points != matrix_size:
        curr_minimum = sys.maxsize
        for candidate in range(matrix_size):
            if not (visited[candidate]):
                if matrix[curr_point][candidate] < curr_minimum:
                    curr_minimum = matrix[curr_point][candidate]
                    next_point = candidate
        visited[next_point] = True
        curr_point = next_point
        path.append(next_point)
        curr_sum += curr_minimum
        visited_points += 1
    curr_sum += matrix[curr_point][start]
    path.append(start)
    print(curr_sum)
    print(path)
    return path, curr_sum


class Ant:
    def __init__(self):
        self.path = []  # droga mrowki
        self.total_dist = 0.0  # przebyty dystans przez mrowke
        self.unvisited = [i for i in range(len(distances))]  # z tego trzeba usuwac odwiedzone przez 1 mrowke punkty


# def next_edge(dists, pher, at, a, b):
#     current = at.path[-1]
#     ps = {}
#     p_sum = 0
#     for i in range(len(dists)):
#         if i in at.unvisited:
#             p_cur = math.pow((dists[current][i]), a) * math.pow(pher[current][i], b)
#             ps[i] = p_cur
#             p_sum += p_cur
#     for i in ps:
#         ps[i] = ps[i] / p_sum
#     ps = dict(sorted(ps.items(), key=lambda item: item[1]))
#     r = random.random()
#     tmp = 0
#     for i in ps:
#         ps[i] += tmp
#         if r < ps[i]:
#             at.unvisited.remove(i)
#             at.path.append(i)
#             at.total_dist += dists[current][i]
#             return i
#         tmp = ps[i]


def next_edge(dists, pher, at, a, b):
    current = at.path[-1]
    ps_sum = 0
    for i in at.unvisited:
        ps_sum += math.pow((dists[current][i]), a) * math.pow(pher[current][i], b)
    ps = [0 for i in range(len(dists))]
    for i in range(len(dists)):
        if i in at.unvisited:
            ps[i] = math.pow((dists[current][i]), a) * math.pow(pher[current][i], b) / ps_sum
    r = random.random()
    for i, p in enumerate(ps):
        r -= p
        if r <= 0:
            at.unvisited.remove(i)
            at.path.append(i)
            at.total_dist += dists[current][i]
            return i


def aco_algorithm(distances, iterations, ant_count, alpha=1.0, beta=1.0):
    min_dist = 999999999
    path_len = len(distances)
    pheromones = [[1 / (path_len * path_len)] * path_len for i in range(path_len)]  # macierz z iloscia pheromones na krawedziach
    for iteration in range(iterations):
        tmp_pheromones = [[0.0] * path_len for i in range(path_len)]
        ants = [Ant() for ant in range(ant_count)]
        for ant in ants:
            start = random.randint(0, path_len - 1)
            ant.path.append(start)
            ant.unvisited.remove(start)
            for edge in range(path_len - 1):
                next_edge(distances, pheromones, ant, alpha, beta)
            ant.path.append(start)
            ant.total_dist += (distances[ant.path[-1]][ant.path[-2]])
            if ant.total_dist < min_dist:
                min_dist = ant.total_dist
            last_location = start
            for location in ant.path:
                if location != start:
                    tmp_pheromones[last_location][location] += 1 / ant.total_dist
                    last_location = location
        for i in range(path_len):
            for j in range(path_len):
                pheromones[i][j] *= 0.5
                pheromones[i][j] += tmp_pheromones[i][j]
    print(min_dist)


        # policzyc o ile sie zwiekszyl pheromone na kazdej krawedzi po trasie kazdej mrowki i sumowac wyniki dla kazdej krawedzi w jakiejs pomocniczej macierzy
        # zupdateowac globalna macierz pheromones o wartosci z pomocniczej macierzy ale uwzglednic vaporization
        # (chyba po przejsciu wszystkich mrowek trzeba tak ale nie jestem pewny, w kazdym razie tak jest w tym projekcie z githuba)


create_instance("instance.txt", 20, 1000)
# distances = points_to_matrix("berlin52.txt")
# distances = points_to_matrix("bier127.txt")
# distances = points_to_matrix("tsp1000.txt")
# distances = points_to_matrix("tsp500.txt")
# distances = points_to_matrix("tsp250.txt")
distances = points_to_matrix("instance.txt")
# for index, row in enumerate(distances):
#     print(index + 1, row)

print("greedy")
greedy_method(distances, 0)
print("mrowki")
aco_algorithm(distances, 100, 100, 1, 10)

# path, path_len = greedy_method(distances, 0)
# for i in range(len(path)):
#     path[i] += 1
# print("Path:", path)
# print("Distance:", path_len)
