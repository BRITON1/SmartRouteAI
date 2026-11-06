
# comparison.py
# Compare Greedy Best-First Search and A* Search

import time
import statistics

from greedy_search import greedy_best_first_search
from astar_search import a_star_search


GOAL = "Bucharest"

# Different starting cities for our experiments
TEST_CITIES = [
    "Arad",
    "Timisoara",
    "Lugoj",
    "Oradea",
    "Craiova",
    "Sibiu"
]

# Number of repetitions for execution-time measurements
REPETITIONS = 100


def measure_execution_time(search_function, start, goal):
    """Measure average execution time in milliseconds."""

    measurements = []

    for _ in range(REPETITIONS):
        beginning = time.perf_counter()

        search_function(start, goal)

        ending = time.perf_counter()

        measurements.append((ending - beginning) * 1000)

    return statistics.mean(measurements)


def compare_algorithms(start, goal):
    """Run and compare both search algorithms."""

    greedy_result = greedy_best_first_search(start, goal)
    astar_result = a_star_search(start, goal)

    greedy_time = measure_execution_time(
        greedy_best_first_search, start, goal
    )

    astar_time = measure_execution_time(
        a_star_search, start, goal
    )

    return {
        "start": start,
        "goal": goal,

        "greedy_path": greedy_result["path"],
        "greedy_cost": greedy_result["cost"],
        "greedy_nodes": greedy_result["expanded_nodes"],
        "greedy_time": greedy_time,

        "astar_path": astar_result["path"],
        "astar_cost": astar_result["cost"],
        "astar_nodes": astar_result["expanded_nodes"],
        "astar_time": astar_time,

        "distance_difference": (
            greedy_result["cost"] - astar_result["cost"]
        )
    }


def main():

    print("\nSMARTROUTE AI")
    print("ALGORITHM PERFORMANCE COMPARISON")
    print("=" * 75)

    print(f"Destination: {GOAL}")
    print(f"Number of test cities: {len(TEST_CITIES)}")
    print(f"Timing repetitions per algorithm: {REPETITIONS}")

    results = []

    for start in TEST_CITIES:

        result = compare_algorithms(start, GOAL)
        results.append(result)

        print("\n" + "-" * 75)

        print(f"ROUTE: {start} -> {GOAL}")

        print("\nGREEDY BEST-FIRST SEARCH")
        print("Path:", " -> ".join(result["greedy_path"]))
        print("Distance:", result["greedy_cost"], "km")
        print("Expanded nodes:", result["greedy_nodes"])
        print(f"Average time: {result['greedy_time']:.6f} ms")

        print("\nA* SEARCH")
        print("Path:", " -> ".join(result["astar_path"]))
        print("Distance:", result["astar_cost"], "km")
        print("Expanded nodes:", result["astar_nodes"])
        print(f"Average time: {result['astar_time']:.6f} ms")

        print("\nDISTANCE DIFFERENCE:",
              result["distance_difference"], "km")

    # Overall performance summary
    print("\n" + "=" * 75)
    print("OVERALL PERFORMANCE SUMMARY")
    print("=" * 75)

    greedy_distances = [r["greedy_cost"] for r in results]
    astar_distances = [r["astar_cost"] for r in results]

    greedy_nodes = [r["greedy_nodes"] for r in results]
    astar_nodes = [r["astar_nodes"] for r in results]

    greedy_times = [r["greedy_time"] for r in results]
    astar_times = [r["astar_time"] for r in results]

    print("\nAverage route distance:")
    print(f"Greedy: {statistics.mean(greedy_distances):.2f} km")
    print(f"A*:     {statistics.mean(astar_distances):.2f} km")

    print("\nAverage expanded nodes:")
    print(f"Greedy: {statistics.mean(greedy_nodes):.2f}")
    print(f"A*:     {statistics.mean(astar_nodes):.2f}")

    print("\nAverage execution time:")
    print(f"Greedy: {statistics.mean(greedy_times):.6f} ms")
    print(f"A*:     {statistics.mean(astar_times):.6f} ms")

    print("\nINTELLIGENT SYSTEM RECOMMENDATION")
    print("-" * 45)

    if sum(astar_distances) < sum(greedy_distances):
        print("A* produced the lower total route distance")
        print("Recommendation: Use A* when shortest distance")
        print("is the primary objective.")

    elif sum(greedy_distances) < sum(astar_distances):
        print("Greedy produced the lower total route distance")
        print("for these test cases.")

    else:
        print("Both algorithms produced equal total distances.")

    print("\nNote: Execution time and expanded nodes are")
    print("separate performance measures from route quality.")


if __name__ == "__main__":
    main()
