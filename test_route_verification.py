
# test_route_verification.py
# Compare Greedy, A* and Dijkstra on the same road graph

from osm_data import get_osm_road_graph

from osm_search import (
    greedy_best_first_search_osm,
    a_star_search_osm
)

from dijkstra_search import dijkstra_search


def main():

    start = "Westlands, Nairobi, Kenya"
    destination = (
        "Jomo Kenyatta International Airport, Nairobi, Kenya"
    )

    network = get_osm_road_graph(start, destination)

    graph = network["graph"]
    start_node = network["start_node"]
    goal_node = network["goal_node"]
    coordinates = network["coordinates"]

    print("\nSMARTROUTEAI ROUTE VERIFICATION")
    print("=" * 55)

    greedy = greedy_best_first_search_osm(
        graph, start_node, goal_node, coordinates
    )

    astar = a_star_search_osm(
        graph, start_node, goal_node, coordinates
    )

    dijkstra = dijkstra_search(
        graph, start_node, goal_node
    )

    results = {
        "Greedy": greedy,
        "A*": astar,
        "Dijkstra": dijkstra
    }

    for name, result in results.items():

        print(f"\n{name}")

        if result["found"]:
            print(
                "Distance:",
                round(result["distance_km"], 3),
                "km"
            )

            print("Road nodes:", len(result["path"]))

        else:
            print("No route found.")

    print("\nINDEPENDENT VERIFICATION")
    print("-" * 40)

    if not dijkstra["found"] or not astar["found"]:
        print("VERIFICATION FAILED: A route was not found.")

    elif abs(astar["cost"] - dijkstra["cost"]) <= 1e-6:

        print("SUCCESS: A* matches Dijkstra's shortest distance.")
        print("A* route distance is independently verified.")

    elif astar["cost"] > dijkstra["cost"]:

        print("WARNING: A* returned a longer route than Dijkstra.")
        print("We need to investigate the heuristic or implementation.")

    else:

        print("WARNING: A* is shorter than the Dijkstra baseline.")
        print("Investigate the graph or implementation.")

    if greedy["found"] and dijkstra["found"]:

        difference = greedy["cost"] - dijkstra["cost"]

        print(
            "\nGreedy distance above optimal:",
            round(difference / 1000, 3),
            "km"
        )


if __name__ == "__main__":
    main()
