
# astar_search.py
# A* Search implementation for SmartRouteAI

import heapq
from itertools import count

from graph import romania_map
from heuristics import get_heuristic


def a_star_search(start, goal):
    """
    Find the shortest route using A* Search.

    Evaluation function:
        f(n) = g(n) + h(n)

    Returns:
        Route, total distance, expanded nodes and search order.
    """

    if start not in romania_map:
        raise ValueError(f"Unknown starting city: {start}")

    if goal not in romania_map:
        raise ValueError(f"Unknown destination city: {goal}")

    if start == goal:
        return {
            "path": [start],
            "cost": 0,
            "expanded_nodes": 0,
            "explored_order": [],
            "found": True
        }

    # Unique sequence number breaks priority ties
    sequence = count()

    # Priority queue entries: (f_score, sequence, city, g_score)
    frontier = []

    # Actual cheapest known distance from start to each city
    g_score = {start: 0}

    # Estimated total cost
    f_score = {start: get_heuristic(start, goal)}

    # Parent dictionary for reconstructing the route
    parent = {start: None}

    # Cities whose neighbours have been examined
    explored = set()

    # Record expansion order
    explored_order = []

    heapq.heappush(
        frontier,
        (f_score[start], next(sequence), start, 0)
    )

    while frontier:

        # Select the city with the lowest estimated total cost
        current_f, _, current_city, current_g = heapq.heappop(frontier)

        # Ignore outdated queue entries
        if current_g != g_score.get(current_city):
            continue

        # Goal test
        if current_city == goal:

            # Reconstruct the optimal path
            path = []
            city = goal

            while city is not None:
                path.append(city)
                city = parent[city]

            path.reverse()

            return {
                "path": path,
                "cost": g_score[goal],
                "expanded_nodes": len(explored_order),
                "explored_order": explored_order,
                "found": True
            }

        # Mark city as expanded
        explored.add(current_city)
        explored_order.append(current_city)

        # Examine neighbouring cities
        for neighbour, distance in romania_map[current_city].items():

            # Calculate the new actual distance
            tentative_g = current_g + distance

            # Check whether this route is better
            if tentative_g < g_score.get(neighbour, float("inf")):

                # Update the best known route
                parent[neighbour] = current_city
                g_score[neighbour] = tentative_g

                # Calculate estimated total cost
                h = get_heuristic(neighbour, goal)
                new_f = tentative_g + h

                f_score[neighbour] = new_f

                # Add the improved route to the priority queue
                heapq.heappush(
                    frontier,
                    (new_f, next(sequence), neighbour, tentative_g)
                )

                # Allow a previously expanded city to be revisited
                explored.discard(neighbour)

    # No route found
    return {
        "path": [],
        "cost": float("inf"),
        "expanded_nodes": len(explored_order),
        "explored_order": explored_order,
        "found": False
    }


# Test the algorithm
if __name__ == "__main__":

    start = "Arad"
    goal = "Bucharest"

    result = a_star_search(start, goal)

    print("\nA* SEARCH")
    print("=" * 45)

    if result["found"]:

        print("Starting city:", start)
        print("Destination:", goal)

        print("\nSelected route:")
        print(" -> ".join(result["path"]))

        print("\nTotal distance:", result["cost"], "km")

        print("Expanded nodes:", result["expanded_nodes"])

        print("Exploration order:")
        print(" -> ".join(result["explored_order"]))

    else:
        print("No route found.")
