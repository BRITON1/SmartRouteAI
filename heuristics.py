
# heuristics.py
# Straight-line distance estimates to Bucharest

heuristics = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}


def get_heuristic(city, goal="Bucharest"):
    """
    Return the estimated distance from a city
    to the destination.
    """

    if city not in heuristics:
        raise ValueError(f"Unknown city: {city}")

    if goal == "Bucharest":
        return heuristics[city]

    raise ValueError(
        "Heuristic values are currently available only for Bucharest."
    )


# Test the heuristic function
if __name__ == "__main__":

    print("HEURISTIC DISTANCES TO BUCHAREST")
    print("=" * 40)

    for city, distance in heuristics.items():
        print(f"{city:<20} {distance} km")

    print("\nTesting heuristic function:")

    print("Arad:", get_heuristic("Arad"))
    print("Sibiu:", get_heuristic("Sibiu"))
    print("Pitesti:", get_heuristic("Pitesti"))
    print("Bucharest:", get_heuristic("Bucharest"))
