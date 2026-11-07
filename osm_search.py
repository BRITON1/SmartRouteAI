
# osm_search.py
# Greedy Best-First Search and A* for OpenStreetMap road networks

import heapq
from itertools import count

from osm_data import haversine_distance


def calculate_heuristic(city, goal, coordinates):
    """
    Estimate remaining distance using Haversine distance.

    Returns metres.
    """

    return haversine_distance(
        coordinates[city],
        coordinates[goal]
    )


def reconstruct_path(parent, goal):
    """Reconstruct the route from the parent dictionary."""

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path


def calculate_path_distance(graph, path):
    """Calculate total road distance in metres."""

    total_distance = 0

    for i in range(len(path) - 1):
        total_distance += graph[path[i]][path[i + 1]]

    return total_distance


def greedy_best_first_search_osm(graph, start, goal, coordinates):
    """
    Greedy Best-First Search.

    Evaluation function:
        f(n) = h(n)
    """

    if start not in graph or goal not in graph:
        raise ValueError("Start or destination node is missing.")

    if start == goal:
        return {
            "path": [start],
            "cost": 0,
            "distance_km": 0,
            "expanded_nodes": 0,
            "explored_order": [],
            "found": True
        }

    frontier = []
    sequence = count()

    heapq.heappush(
        frontier,
        (calculate_heuristic(start, goal, coordinates),
         next(sequence),
         start)
    )

    parent = {start: None}
    discovered = {start}
    explored = set()
    explored_order = []

    while frontier:

        _, _, current = heapq.heappop(frontier)

        if current == goal:

            path = reconstruct_path(parent, goal)
            distance = calculate_path_distance(graph, path)

            return {
                "path": path,
                "cost": distance,
                "distance_km": distance / 1000,
                "expanded_nodes": len(explored_order),
                "explored_order": explored_order,
                "found": True
            }

        explored.add(current)
        explored_order.append(current)

        for neighbour in graph[current]:

            if neighbour not in discovered and neighbour not in explored:

                discovered.add(neighbour)
                parent[neighbour] = current

                priority = calculate_heuristic(
                    neighbour,
                    goal,
                    coordinates
                )

                heapq.heappush(
                    frontier,
                    (priority, next(sequence), neighbour)
                )

    return {
        "path": [],
        "cost": float("inf"),
        "distance_km": float("inf"),
        "expanded_nodes": len(explored_order),
        "explored_order": explored_order,
        "found": False
    }


def a_star_search_osm(graph, start, goal, coordinates):
    """
    A* Search.

    Evaluation function:
        f(n) = g(n) + h(n)
    """

    if start not in graph or goal not in graph:
        raise ValueError("Start or destination node is missing.")

    if start == goal:
        return {
            "path": [start],
            "cost": 0,
            "distance_km": 0,
            "expanded_nodes": 0,
            "explored_order": [],
            "found": True
        }

    sequence = count()
    frontier = []

    g_score = {start: 0}
    parent = {start: None}

    explored = set()
    explored_order = []

    initial_h = calculate_heuristic(start, goal, coordinates)

    heapq.heappush(
        frontier,
        (initial_h, next(sequence), start, 0)
    )

    while frontier:

        current_f, _, current, current_g = heapq.heappop(frontier)

        # Ignore outdated queue entries
        if current_g != g_score.get(current):
            continue

        if current == goal:

            path = reconstruct_path(parent, goal)
            distance = g_score[goal]

            return {
                "path": path,
                "cost": distance,
                "distance_km": distance / 1000,
                "expanded_nodes": len(explored_order),
                "explored_order": explored_order,
                "found": True
            }

        explored.add(current)
        explored_order.append(current)

        for neighbour, road_distance in graph[current].items():

            tentative_g = current_g + road_distance

            if tentative_g < g_score.get(neighbour, float("inf")):

                g_score[neighbour] = tentative_g
                parent[neighbour] = current

                h = calculate_heuristic(
                    neighbour,
                    goal,
                    coordinates
                )

                new_f = tentative_g + h

                heapq.heappush(
                    frontier,
                    (new_f, next(sequence), neighbour, tentative_g)
                )

                # Reopen a node if a better route is discovered
                explored.discard(neighbour)

    return {
        "path": [],
        "cost": float("inf"),
        "distance_km": float("inf"),
        "expanded_nodes": len(explored_order),
        "explored_order": explored_order,
        "found": False
    }
