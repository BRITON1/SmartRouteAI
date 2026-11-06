
# greedy_search.py
# Greedy Best-First Search implementation

import heapq
from itertools import count

from graph import romania_map
from heuristics import get_heuristic


def greedy_best_first_search(start, goal):
    """
    Find a route using Greedy Best-First Search.

    Evaluation function:
        f(n) = h(n)

    Returns:
        Route, total distance, expanded nodes and search order.
    """

    if start not in romania_map:
        raise ValueError(f"Unknown starting city: {start}")

    if goal not in romania_map:
        raise ValueError(f"Unknown destination city: {goal}")

    # Handle the case where start and goal are identical
    if start == goal:
        return {
            "path": [start],
            "cost": 0,
            "expanded_nodes": 0,
            "explored_order": [],
            "found": True
        }

    # Priority queue: (heuristic, insertion order, city)
    frontier = []
    sequence = count()

    heapq.heappush(
        frontier,
        (get_heuristic(start, goal), next(sequence), start)
    )

    # Store each city's predecessor
    parent = {start: None}

    # Prevent adding the same city repeatedly
    discovered = {start}

    # Cities whose neighbours have been examined
    explored = set()

    # Record the order of expanded cities
    explored_order = []

    while frontier:

        # Get the city with the smallest heuristic
        _, _, current_city = heapq.heappop(frontier)

        # Check whether we have reached the destination
        if current_city == goal:

            # Reconstruct the route
            path = []
            city = goal

            while city is not None:
                path.append(city)
                city = parent[city]

            path.reverse()

            # Calculate actual road distance
            total_cost = 0

            for i in range(len(path) - 1):
                total_cost += romania_map[path[i]][path[i + 1]]

            return {
                "path": path,
                "cost": total_cost,
                "expanded_nodes": len(explored_order),
                "explored_order": explored_order,
                "found": True
            }

        # Mark the current city as expanded
        explored.add(current_city)
        explored_order.append(current_city)

        # Examine all neighbouring cities
        for neighbour in romania_map[current_city]:

            if neighbour not in discovered and neighbour not in explored:

                discovered.add(neighbour)

                # Remember how we reached this neighbour
                parent[neighbour] = current_city

                # Add neighbour using heuristic as priority
                priority = get_heuristic(neighbour, goal)

                heapq.heappush(
                    frontier,
                    (priority, next(sequence), neighbour)
                )

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

    result = greedy_best_first_search(start, goal)

    print("\nGREEDY BEST-FIRST SEARCH")
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
