
# heuristics.py
# Destination-independent heuristic for SmartRouteAI

import math

from graph import romania_map


# --------------------------------------------------
# CITY POSITIONS
# --------------------------------------------------
# These are schematic map coordinates.
# They are NOT actual geographical coordinates.
#
# They allow us to calculate a consistent heuristic
# for every possible destination in our graph.

city_coordinates = {
    "Arad": (1, 5),
    "Zerind": (2, 6),
    "Oradea": (3, 7),
    "Sibiu": (4, 5),
    "Timisoara": (0, 3),
    "Lugoj": (1, 2),
    "Mehadia": (2, 1),
    "Drobeta": (3, 0),
    "Craiova": (5, 1),
    "Rimnicu Vilcea": (5, 4),
    "Fagaras": (7, 5),
    "Pitesti": (7, 3),
    "Bucharest": (9, 2),
    "Giurgiu": (10, 0),
    "Urziceni": (11, 3),
    "Hirsova": (13, 3),
    "Eforie": (14, 1),
    "Vaslui": (13, 5),
    "Iasi": (14, 7),
    "Neamt": (12, 8)
}


# --------------------------------------------------
# HEURISTIC SCALE
# --------------------------------------------------
# The scale must ensure that estimated straight-line
# distances never exceed the corresponding road costs.

HEURISTIC_SCALE_KM = 30


# --------------------------------------------------
# HEURISTIC FUNCTION
# --------------------------------------------------

def get_heuristic(city, goal="Bucharest"):
    """
    Estimate the distance from a city to a destination.

    Uses scaled Euclidean distance.

    h(n) = scale * sqrt((x2-x1)^2 + (y2-y1)^2)

    The scale of 30 km per map unit keeps the heuristic
    admissible and consistent for the current road graph.
    """

    if city not in romania_map:
        raise ValueError(f"Unknown city: {city}")

    if goal not in romania_map:
        raise ValueError(f"Unknown destination: {goal}")

    x1, y1 = city_coordinates[city]
    x2, y2 = city_coordinates[goal]

    distance = math.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2
    )

    return distance * HEURISTIC_SCALE_KM


# --------------------------------------------------
# TEST THE HEURISTIC
# --------------------------------------------------

if __name__ == "__main__":

    print("SMARTROUTEAI DYNAMIC HEURISTIC")
    print("=" * 50)

    test_routes = [
        ("Arad", "Bucharest"),
        ("Bucharest", "Arad"),
        ("Timisoara", "Iasi"),
        ("Oradea", "Craiova"),
        ("Sibiu", "Pitesti")
    ]

    for start, goal in test_routes:

        estimate = get_heuristic(start, goal)

        print(
            f"{start:18} -> {goal:18} "
            f"{estimate:.2f} km"
        )

    # Verify heuristic consistency across every road
    print("\nCHECKING HEURISTIC CONSISTENCY")
    print("=" * 50)

    consistent = True

    for goal in romania_map:

        for city, neighbours in romania_map.items():

            for neighbour, road_distance in neighbours.items():

                h_city = get_heuristic(city, goal)
                h_neighbour = get_heuristic(neighbour, goal)

                if h_city > road_distance + h_neighbour + 1e-9:

                    print(
                        f"Violation: {city} -> {neighbour} "
                        f"for goal {goal}"
                    )

                    consistent = False

    if consistent:
        print("SUCCESS: Heuristic is consistent for every destination.")

    else:
        print("WARNING: Heuristic consistency check failed.")
