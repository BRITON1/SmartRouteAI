
# graph.py
# Romania road network for SmartRouteAI

# Create an empty graph
romania_map = {}


def add_road(city1, city2, distance):
    """Add a two-way road between two cities."""

    if city1 not in romania_map:
        romania_map[city1] = {}

    if city2 not in romania_map:
        romania_map[city2] = {}

    # Roads work in both directions
    romania_map[city1][city2] = distance
    romania_map[city2][city1] = distance


# Define the roads and their distances in kilometres

roads = [
    ("Arad", "Zerind", 75),
    ("Arad", "Sibiu", 140),
    ("Arad", "Timisoara", 118),
    ("Zerind", "Oradea", 71),
    ("Oradea", "Sibiu", 151),
    ("Sibiu", "Fagaras", 99),
    ("Sibiu", "Rimnicu Vilcea", 80),
    ("Timisoara", "Lugoj", 111),
    ("Lugoj", "Mehadia", 70),
    ("Mehadia", "Drobeta", 75),
    ("Drobeta", "Craiova", 120),
    ("Craiova", "Rimnicu Vilcea", 146),
    ("Craiova", "Pitesti", 138),
    ("Rimnicu Vilcea", "Pitesti", 97),
    ("Fagaras", "Bucharest", 211),
    ("Pitesti", "Bucharest", 101),
    ("Bucharest", "Giurgiu", 90),
    ("Bucharest", "Urziceni", 85),
    ("Urziceni", "Hirsova", 98),
    ("Hirsova", "Eforie", 86),
    ("Urziceni", "Vaslui", 142),
    ("Vaslui", "Iasi", 92),
    ("Iasi", "Neamt", 87)
]


# Build the graph
for city1, city2, distance in roads:
    add_road(city1, city2, distance)


# Display the graph
if __name__ == "__main__":
    print("ROMANIA ROAD NETWORK")
    print("=" * 40)

    for city, neighbours in romania_map.items():
        print(f"\n{city}:")
        for neighbour, distance in neighbours.items():
            print(f"  -> {neighbour}: {distance} km")
