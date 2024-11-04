# ResNet: A Network Structure for Reference Energy Systems (RES)

> This module, `resnet.py`, provides a framework to define and analyze the structure of a Reference Energy System (RES) using directed graphs. Leveraging `networkx`, it allows users to define nodes (technologies) and edges (energy flows) to represent the static layout and connections in an energy system. This module is particularly useful for energy modeling in research and policy analysis.

## Class Overview - `ResGraph`

The `ResGraph` class extends `networkx.DiGraph` to represent RES structures.

#### Attributes

- `skeleton_path`: Path to the `skeleton.json` file with RES structure details.
- `structure`: Dictionary containing the loaded RES structure with node and edge (*arrow* indeed) data.

#### Key Methods

- `__post_init__()`: Initializes the graph and loads the structure from the specified JSON file.
- `load_structure() -> dict`: Loads and returns the RES structure as a dictionary from `skeleton.json`.
- `get_params(index: str) -> dict`: Retrieves parameters for a specific node or technology.
- `get_variables(index: str) -> dict`: Fetches variables related to a specific node or energy flow.
- `add_technology(tech_label: str, tech_type: str, layer: int, index: str = "t")`: Adds a technology node to the graph with a unique label, type, and layer designation.
- `add_fuel(tech_from: str, tech_to: str, fuel_label: str, fuel_type: str, index: str = "f")`: Adds an energy flow between two technologies, representing a commodity or fuel transfer.

## Usage

1. **Initialize the ResGraph**:
   ```python
   from resnet import ResGraph
   res_graph = ResGraph(skeleton_path='./Structure/skeleton.json')
   ```

2. **Load Structure**:
   The structure loads during initialization, but you can reload it as needed:
   ```python
   structure = res_graph.load_structure()
   ```

3. **Add Technology**:
   Add a technology node to the graph, specifying label, type, and layer:
   ```python
   res_graph.add_technology(tech_label="PWRHYD",
                            tech_type="Hydroelectric Power Plant",
                            layer=0)
   res_graph.add_technology(tech_label="PWRTRN",
                            tech_type="Transmission of Electricity",
                            layer=1)
   ```

4. **Add Fuel Flow**:
   Define an energy flow between two technologies:
   ```python
   res_graph.add_fuel(tech_from="PWRHYD",
                      tech_to="PWRTRN",
                      fuel_label="ELC001",
                      fuel_type="Electricity before Transmission")
   ```

## Features

- **Directed Graph Representation**: Models an RES as a directed graph (DiGraph), where nodes are technologies and edges represent energy flows.
- **Flexible Structure Loading**: Reads network structure from a JSON file, enabling modular and reusable configurations.
- **Technology, Fuel, and Parameter Management**: Supports adding technologies and energy flows, and retrieving specific parameters and variables for nodes and flows.

## Requirements

- Python 3.6+
- `networkx` (for graph structures)
- `matplotlib` (for visualization)
- `json` (for handling JSON structures)

Install dependencies:
```bash
pip install networkx matplotlib
```