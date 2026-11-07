
# test_osm_search.py
# Test SmartRouteAI algorithms on real Nairobi roads

from time import perf_counter

from osm_data import get_osm_road_graph

from osm_search import (
    greedy_best_first_search_osm,
    a_star_search_osm
)


def run_test():

    start = "Westlands, Nairobi, Kenya"

    destination = (
        "Jomo Kenyatta International Airport, Nairobi, Kenya"
    )

    # Retrieve the road network
    network_data = get_osm_road_graph(
        start,
        destination
    )

    graph = network_data["graph"]
    start_node = network_data["start_node"]
    goal_node = network_data["goal_node"]
    coordinates = network_data["coordinates"]

    print("\nSMARTROUTEAI REAL-WORLD ROUTING")
    print("=" * 55)

    # Run Greedy
    print("\nRunning Greedy Best-First Search...")

    start_time = perf_counter()

    greedy_result = greedy_best_first_search_osm(
        graph,
        start_node,
        goal_node,
        coordinates
    )

    greedy_time = (perf_counter() - start_time) * 1000

    # Run A*
    print("\nRunning A* Search...")

    start_time = perf_counter()

    astar_result = a_star_search_osm(
        graph,
        start_node,
        goal_node,
        coordinates
    )

    astar_time = (perf_counter() - start_time) * 1000

    # Display results
    print("\nGREEDY BEST-FIRST SEARCH")
    print("-" * 40)

    if greedy_result["found"]:

        print("Distance:", round(greedy_result["distance_km"], 2), "km")
        print("Road nodes in route:", len(greedy_result["path"]))
        print("Expanded nodes:", greedy_result["expanded_nodes"])
        print("Execution time:", round(greedy_time, 3), "ms")

    else:
        print("No route found.")

    print("\nA* SEARCH")
    print("-" * 40)

    if astar_result["found"]:

        print("Distance:", round(astar_result["distance_km"], 2), "km")
        print("Road nodes in route:", len(astar_result["path"]))
        print("Expanded nodes:", astar_result["expanded_nodes"])
        print("Execution time:", round(astar_time, 3), "ms")

    else:
        print("No route found.")

    print("\nALGORITHM COMPARISON")
    print("=" * 55)

    if greedy_result["found"] and astar_result["found"]:

        difference = (
            greedy_result["distance_km"]
            - astar_result["distance_km"]
        )

        print(
            "Distance difference:",
            round(difference, 3),
            "km"
        )

        if astar_result["cost"] <= greedy_result["cost"] + 1e-6:
            print("A* found a route no longer than Greedy's route.")

        else:
            print("Unexpected result: investigate the algorithms.")

        print("\nA* optimality will be independently verified later")
        print("using a Dijkstra shortest-path baseline.")

    else:
        print("At least one algorithm failed to find a route.")


if __name__ == "__main__":
    run_test()
