
# dijkstra_search.py
# Independent shortest-path verification for SmartRouteAI

import heapq
from itertools import count


def dijkstra_search(graph, start, goal):
    """
    Dijkstra's shortest-path algorithm.

    Uses actual road distances only.

    Returns the shortest known route and its distance.
    """

    if start not in graph or goal not in graph:
        raise ValueError("Start or destination node is missing.")

    if start == goal:
        return {
            "path": [start],
            "cost": 0,
            "distance_km": 0,
            "expanded_nodes": 0,
            "found": True
        }

    sequence = count()
    frontier = []

    distances = {start: 0}
    parent = {start: None}

    explored = set()

    heapq.heappush(
        frontier,
        (0, next(sequence), start)
    )

    while frontier:

        current_distance, _, current = heapq.heappop(frontier)

        # Ignore outdated queue entries
        if current_distance != distances.get(current):
            continue

        if current == goal:

            path = []
            node = goal

            while node is not None:
                path.append(node)
                node = parent[node]

            path.reverse()

            return {
                "path": path,
                "cost": current_distance,
                "distance_km": current_distance / 1000,
                "expanded_nodes": len(explored),
                "found": True
            }

        explored.add(current)

        for neighbour, road_distance in graph[current].items():

            new_distance = current_distance + road_distance

            if new_distance < distances.get(
                neighbour,
                float("inf")
            ):

                distances[neighbour] = new_distance
                parent[neighbour] = current

                heapq.heappush(
                    frontier,
                    (
                        new_distance,
                        next(sequence),
                        neighbour
                    )
                )

    return {
        "path": [],
        "cost": float("inf"),
        "distance_km": float("inf"),
        "expanded_nodes": len(explored),
        "found": False
    }
