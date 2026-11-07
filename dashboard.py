
import time

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from graph import romania_map
from greedy_search import greedy_best_first_search
from astar_search import a_star_search


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SmartRouteAI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #0b1120;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background: #111a2e;
        border-right: 1px solid #26344d;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #172c4c, #102039, #17233b);
        border: 1px solid #2c4569;
        margin-bottom: 24px;
    }

    .hero h1 {
        font-size: 34px;
        color: #ffffff;
        margin-bottom: 5px;
        font-weight: 800;
    }

    .hero p {
        color: #a9bdd8;
        font-size: 15px;
        margin-bottom: 0;
    }

    .metric-card {
        background: #141f33;
        border: 1px solid #263750;
        padding: 19px;
        border-radius: 15px;
        min-height: 115px;
    }

    .metric-label {
        color: #91a4c0;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-value {
        color: #ffffff;
        font-size: 27px;
        font-weight: 800;
        margin-top: 8px;
    }

    .metric-sub {
        color: #8295b1;
        font-size: 12px;
        margin-top: 4px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .algorithm-card {
        background: #141f33;
        border: 1px solid #263750;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 10px;
    }

    .algorithm-card h3 {
        color: #ffffff;
        font-size: 19px;
    }

    .algorithm-card p {
        color: #a9bdd8;
        font-size: 14px;
    }

    .route-text {
        color: #dce8f8;
        font-size: 14px;
        line-height: 1.9;
    }

    .recommendation {
        background: #132b2b;
        border: 1px solid #23665b;
        border-radius: 15px;
        padding: 20px;
        color: #d8f5eb;
        margin-top: 15px;
    }

    div.stButton > button {
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
    }

    div.stButton > button:hover {
        background: #3b82f6;
        color: white;
        border: none;
    }

    h2, h3 {
        color: #ffffff;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# ROMANIA MAP POSITIONS
# Schematic positions, not geographic coordinates
# --------------------------------------------------

positions = {
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
# ROUTE VISUALIZATION
# --------------------------------------------------

def create_route_map(greedy_result, astar_result, start, goal):

    fig = go.Figure()

    # Draw all road connections
    for city, neighbours in romania_map.items():

        for neighbour, distance in neighbours.items():

            # Avoid drawing each two-way road twice
            if city < neighbour:

                x1, y1 = positions[city]
                x2, y2 = positions[neighbour]

                fig.add_trace(go.Scatter(
                    x=[x1, x2],
                    y=[y1, y2],
                    mode="lines",
                    line=dict(color="#34445e", width=2),
                    hoverinfo="text",
                    text=f"{city} — {neighbour}: {distance} km",
                    showlegend=False
                ))

    # Highlight Greedy route
    if greedy_result["found"]:
        path = greedy_result["path"]

        for i in range(len(path) - 1):
            x1, y1 = positions[path[i]]
            x2, y2 = positions[path[i + 1]]

            fig.add_trace(go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line=dict(color="#f59e0b", width=5),
                name="Greedy route",
                showlegend=(i == 0),
                hoverinfo="text",
                text=f"Greedy: {path[i]} → {path[i + 1]}"
            ))

    # Highlight A* route
    if astar_result["found"]:
        path = astar_result["path"]

        for i in range(len(path) - 1):
            x1, y1 = positions[path[i]]
            x2, y2 = positions[path[i + 1]]

            fig.add_trace(go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line=dict(color="#22d3ee", width=5),
                name="A* route",
                showlegend=(i == 0),
                hoverinfo="text",
                text=f"A*: {path[i]} → {path[i + 1]}"
            ))

    # Draw cities
    cities = list(romania_map.keys())

    city_x = [positions[city][0] for city in cities]
    city_y = [positions[city][1] for city in cities]

    fig.add_trace(go.Scatter(
        x=city_x,
        y=city_y,
        mode="markers+text",
        text=cities,
        textposition="top center",
        textfont=dict(color="#dce8f8", size=10),
        marker=dict(
            size=12,
            color=[
                "#f59e0b" if city == start == goal
                else "#22c55e" if city == start
                else "#ef4444" if city == goal
                else "#64748b"
                for city in cities
            ],
            line=dict(color="#ffffff", width=1)
        ),
        name="Cities",
        hovertemplate="%{text}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="ROMANIA ROAD NETWORK",
            font=dict(color="white", size=18)
        ),
        paper_bgcolor="#111a2e",
        plot_bgcolor="#111a2e",
        font=dict(color="white"),
        height=570,
        margin=dict(l=15, r=15, t=60, b=15),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


# --------------------------------------------------
# RUN AND MEASURE ALGORITHMS
# --------------------------------------------------

def run_algorithm(search_function, start, goal):

    start_time = time.perf_counter()

    result = search_function(start, goal)

    execution_time = (time.perf_counter() - start_time) * 1000

    result["execution_time"] = execution_time

    return result


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🧭 SmartRouteAI")

    st.caption("Intelligent Route Optimization System")

    st.divider()

    st.markdown("### Route Planner")

    cities = sorted(romania_map.keys())

    start_city = st.selectbox(
        "Starting city",
        cities,
        index=cities.index("Arad")
    )

    destination = st.selectbox(
        "Destination city",
        cities,
        index=cities.index("Bucharest")
    )

    st.caption("Choose any destination in the Romania road network.")

    st.divider()

    st.markdown("### Search Algorithms")

    st.markdown("🟠 Greedy Best-First Search")
    st.markdown("🔵 A* Search")

    st.divider()

    run_button = st.button(
        "🚀 Find Best Route",
        width="stretch"
    )

    st.caption("SmartRouteAI • Academic AI Project")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>🧭 SmartRouteAI</h1>
    <p>
        Intelligent route planning powered by Artificial Intelligence.
        Compare Greedy Best-First Search and A* Search.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = None

if run_button:

    greedy_result = run_algorithm(
        greedy_best_first_search,
        start_city,
        destination
    )

    astar_result = run_algorithm(
        a_star_search,
        start_city,
        destination
    )

    st.session_state.results = {
        "start": start_city,
        "goal": destination,
        "greedy": greedy_result,
        "astar": astar_result
    }


# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

results = st.session_state.results

if results is None:

    st.info(
        "Select starting and destination cities from the sidebar and click "
        "'Find Best Route' to begin."
    )

    st.markdown("### What SmartRouteAI does")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🟠 Greedy Search**

        Selects the next city using the heuristic estimate.
        """)

    with col2:
        st.markdown("""
        **🔵 A* Search**

        Combines the actual distance travelled and estimated remaining distance.
        """)

    with col3:
        st.markdown("""
        **📊 Performance Analysis**

        Compares route distance, search effort and execution time.
        """)

else:

    greedy = results["greedy"]
    astar = results["astar"]

    st.markdown(
        f"### Route analysis: {results['start']} → {results['goal']}"
    )

    # TOP METRICS

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">A* Route Distance</div>
            <div class="metric-value">{astar['cost']} km</div>
            <div class="metric-sub">Shortest route found</div>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Greedy Distance</div>
            <div class="metric-value">{greedy['cost']} km</div>
            <div class="metric-sub">Heuristic-based route</div>
        </div>
        """, unsafe_allow_html=True)

    with metric3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">A* Expanded Nodes</div>
            <div class="metric-value">{astar['expanded_nodes']}</div>
            <div class="metric-sub">Cities expanded</div>
        </div>
        """, unsafe_allow_html=True)

    with metric4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Greedy Expanded Nodes</div>
            <div class="metric-value">{greedy['expanded_nodes']}</div>
            <div class="metric-sub">Cities expanded</div>
        </div>
        """, unsafe_allow_html=True)

    # ALGORITHM RESULTS

    st.markdown('<div class="section-title">Algorithm Results</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="algorithm-card">
            <h3>🟠 Greedy Best-First Search</h3>
            <p>Evaluation function: f(n) = h(n)</p>
        </div>
        """, unsafe_allow_html=True)

        if greedy["found"]:
            st.success(f"Route found • {greedy['cost']} km")

            st.markdown(
                "**Selected route**:  \n"
                + " → ".join(greedy["path"])
            )

            st.write("Expanded nodes:", greedy["expanded_nodes"])

            st.write(
                "Execution time:",
                f"{greedy['execution_time']:.4f} ms"
            )

            st.write(
                "Exploration order:",
                " → ".join(greedy["explored_order"])
            )

        else:
            st.error("No route found.")

    with col2:

        st.markdown("""
        <div class="algorithm-card">
            <h3>🔵 A* Search</h3>
            <p>Evaluation function: f(n) = g(n) + h(n)</p>
        </div>
        """, unsafe_allow_html=True)

        if astar["found"]:
            st.success(f"Route found • {astar['cost']} km")

            st.markdown(
                "**Selected route**:  \n"
                + " → ".join(astar["path"])
            )

            st.write("Expanded nodes:", astar["expanded_nodes"])

            st.write(
                "Execution time:",
                f"{astar['execution_time']:.4f} ms"
            )

            st.write(
                "Exploration order:",
                " → ".join(astar["explored_order"])
            )

        else:
            st.error("No route found.")

    # INTERACTIVE MAP

    st.markdown('<div class="section-title">Interactive Road Network</div>',
                unsafe_allow_html=True)

    st.caption(
        "Orange represents the Greedy route. Cyan represents the A* route. "
        "Some roads may overlap."
    )

    fig = create_route_map(
        greedy,
        astar,
        results["start"],
        results["goal"]
    )

    st.plotly_chart(fig, width="stretch")

    # PERFORMANCE CHARTS

    st.markdown('<div class="section-title">Performance Analytics</div>',
                unsafe_allow_html=True)

    comparison = pd.DataFrame({
        "Algorithm": ["Greedy", "A*"],
        "Distance (km)": [greedy["cost"], astar["cost"]],
        "Expanded Nodes": [
            greedy["expanded_nodes"],
            astar["expanded_nodes"]
        ],
        "Execution Time (ms)": [
            greedy["execution_time"],
            astar["execution_time"]
        ]
    })

    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown("#### Route distance")

        st.bar_chart(
            comparison,
            x="Algorithm",
            y="Distance (km)"
        )

        st.markdown("#### Expanded nodes")

        st.bar_chart(
            comparison,
            x="Algorithm",
            y="Expanded Nodes"
        )

    with chart2:
        st.markdown("#### Execution time")

        st.bar_chart(
            comparison,
            x="Algorithm",
            y="Execution Time (ms)"
        )

        st.markdown("#### Comparison table")

        st.dataframe(
            comparison,
            hide_index=True,
            width="stretch"
        )

    # INTELLIGENT RECOMMENDATION

    st.markdown('<div class="section-title">AI Recommendation</div>',
                unsafe_allow_html=True)

    if astar["found"] and greedy["found"]:

        if astar["cost"] < greedy["cost"]:

            recommendation = (
                "A* Search found a shorter route than Greedy Best-First Search. "
                "For this journey, A* is the better choice when minimizing "
                "travel distance is the priority."
            )

        elif astar["cost"] == greedy["cost"]:

            recommendation = (
                "Both algorithms found routes with the same total distance. "
                "A* guarantees an optimal route under the conditions of this "
                "problem, while Greedy uses the heuristic to guide its search."
            )

        else:

            recommendation = (
                "The results differ from the expected optimality of A*. "
                "Check the heuristic values and algorithm implementation."
            )

        st.markdown(
            f'<div class="recommendation">💡 <b>System insight</b><br><br>'
            f'{recommendation}</div>',
            unsafe_allow_html=True
        )

    else:
        st.warning("One or both algorithms did not find a valid route.")

    st.caption(
        "Note: Execution time is measured for a single run and can vary "
        "between runs depending on the computer and system load."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<center style='color:#71839e'>"
    "SmartRouteAI | Artificial Intelligence | "
    "Greedy Best-First Search & A* Search"
    "</center>",
    unsafe_allow_html=True
)
