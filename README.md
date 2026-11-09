# SmartRouteAI
### Experiment No. 3 – Greedy Best-First Search and A* Search

**Group:** 9  
**Institution:** University of Nairobi  
**Course:** Artificial Intelligence Programming

## 1. Project Overview

SmartRouteAI is an intelligent route-planning application that demonstrates and compares informed search algorithms through an interactive dashboard.

The project implements:
- Greedy Best-First Search.
- A* Search.
- Dijkstra's Algorithm (additional shortest-path verification).

It includes an academic Romania road-map demonstration and an additional real-world routing module using OpenStreetMap.

## 2. Main Features

- Interactive Streamlit dashboard.
- Route selection between starting and destination cities.
- Greedy and A* route comparison.
- Search performance measurements:
  - Route distance.
  - Expanded nodes.
  - Execution time.
- Real-world road-network retrieval using OpenStreetMap.
- Interactive Folium route maps.
- Dijkstra shortest-path verification.

## 3. Technologies Used

- Python 3.13
- Streamlit
- OSMnx
- OpenStreetMap
- Folium
- Streamlit-Folium
- Scikit-learn

## 4. Project Requirements

Before running the application, ensure you have:

- Windows 10 or later.
- Python 3.13.x installed.
- Visual Studio Code (recommended).
- Git (optional).
- An active internet connection for real-world map retrieval.

## 5. Installation Guide – Windows PowerShell

**Step 1: Extract the project**

Download or copy the SmartRouteAI project folder to your computer.

**Step 2: Open the project directory**

Open PowerShell or the VS Code terminal and navigate to the project folder.

Example:

```powershell
cd "C:\Users\YourUsername\Desktop\SmartRouteAI"
```

**Step 3: Create a virtual environment**

```powershell
python -m venv .venv
```

**Step 4: Activate the virtual environment**

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

**Step 5: Upgrade pip**

```powershell
python -m pip install --upgrade pip
```

**Step 6: Install project dependencies**

```powershell
pip install -r requirements.txt
```

Wait until the installation completes.

## 6. Running the Application

From the main SmartRouteAI project directory, execute:

```powershell
streamlit run dashboard.py
```

The application opens in a web browser.

### Available Modules

**A. Romania Road Map**
- Demonstrates Greedy Best-First Search and A*.
- Allows selection of starting and destination cities.
- Displays routes and algorithm performance comparisons.

**B. Real-World Routing**
- Open the Real-World Routing page from the Streamlit sidebar.
- Enter the starting and destination locations.
- Prepare the road network.
- Select the algorithms to execute and calculate routes.
- View the calculated routes on an interactive map.

## 7. Current Limitations

- The real-world routing module has been reliably tested within Nairobi, Kenya.
- Intercity routes, such as Vihiga to Nairobi, are not yet reliably supported.
- Road-network retrieval depends on external OpenStreetMap services.
- Temporary external service errors may prevent a route from loading.

The Romania road-map implementation remains available independently of the real-world routing module.

## 8. Troubleshooting

**Problem: Python is not recognised**

- Confirm Python is installed.
- Ensure Python is added to the system PATH.
- Restart the terminal after installation.

**Problem: Virtual environment activation is blocked**

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Problem: Missing Python packages**

Ensure the virtual environment is activated, then run:

```powershell
pip install -r requirements.txt
```

**Problem: Real-world road network fails to load**

- Check your internet connection.
- Retry after some time.
- OpenStreetMap-related services may temporarily be unavailable.

## 9. Important Notes

- Run commands from the main SmartRouteAI project directory.
- Do not distribute the `.venv` folder.
- Do not include temporary cache files in the submission.
- Install dependencies using `requirements.txt`.

## 10. References

- Greedy Best-First Search: https://www.geeksforgeeks.org/best-first-search-informed-search/
- A* Search: https://www.geeksforgeeks.org/a-search-algorithm/
- OpenStreetMap: https://www.openstreetmap.org/
- OSMnx Documentation: https://osmnx.readthedocs.io/