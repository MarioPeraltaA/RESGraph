"""Network Structure of the RES.

Focused on the network structure of a Reference Energy System.
The actual layout or arrangement of the network components.
In the case of an RES, the structure would refer to the static
connections between technologies (nodes)
and the pathways for commodities or energy flows (edges).

Existing framework
    The layout and connections between
    nodes (technologies, commodities) as they are.
    In a Reference Energy System (RES),
    this would include knowing which technologies
    connect to each other via commodity flows
    (e.g., coal to power generation or electricity to demand).

Topology
    The structure or pattern of these connections,
    often represented as nodes (technologies)
    and edges (flows or commodities).
    In essence, it's the "map" of the network
    without information on how it functions.

**Network structure** thus emphasizes the arrangement
and configuration of nodes and edges in the RES.

"""
from dataclasses import dataclass, field
import networkx as nx
import matplotlib.pyplot as plt
import json


@dataclass()
class ResGraph(nx.DiGraph):
    """Set RES as a DiGraph."""

    skeleton_path: str = field(default="./Structure/skeleton.json")
    structure: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        """Initialize DiGraph and load the structure.

        Load the structure from the JSON file
        specified by skeleton_path and set as attribute.

        """
        super().__init__()
        self.structure = self.load_structure()

    def load_structure(self) -> dict:
        """Load OSeMOSYS model structure from the skeleton JSON file."""
        try:
            with open(self.skeleton_path, "r") as json_file:
                skeleton_data = json.load(json_file)
            return skeleton_data
        except FileNotFoundError:
            print(f"Warning: {self.skeleton_path} not found.")
            return {}

    def get_params(
            self,
            index: str,
    ) -> dict:
        """Retrieve parameters from structure."""
        params = self.structure['params']
        return {param: param_ft['default']
                for param, param_ft in params.items()
                if index in param_ft['indices']}

    def get_variables(
            self,
            index: str
    ) -> dict:
        """Retrieve variables from structure."""
        vars = self.structure['variables']
        return {var: var_ft['default']
                for var, var_ft in vars.items()
                if index in var_ft['indices']}

    def add_technology(
            self,
            tech_label: str,
            tech_type: str,
            layer: int,
            index: str = "t"
    ) -> None:
        """Add technology as a node.

        Abstract component that uses fuel,
        supplies it or convert it from one kind
        to another.

        Note: The modeller is free to interpret the role
        of a technology at will, where relevant.
        It may for example represent a single real
        technology (such as a power plant) or can represent
        a heavily aggregated collection of technologies
        (such as the stock of several million light bulbs),
        or may even simply be a *dummy technology*,
        perhaps used for accounting purposes.
        **Storage** facilities on the other hand
        is well-adviced to model them apart.

        Parameters
        ----------
        tech_label : str
            Acronyms following naming convention format.
        tech_type : str
            Verbose style of the corresponding label.

        Note: The node *Label* must be unique.

        """
        node_params = self.get_params(index)
        node_vars = self.get_variables(index)

        self.add_node(tech_label,
                      tech_type=tech_type,
                      layer=layer,
                      index=index,
                      **node_params,
                      **node_vars)

    def add_fuel(
            self,
            tech_from: str,
            tech_to: str,
            fuel_label: str,
            fuel_type: str,
            index: str = "f"
    ) -> None:
        """Add energy flow as an arrow.

        Includes a energetic flow vector from
        one technology to another one.

        Parameters
        ----------
        tech_from : str
            Technology label arrow tail.
        tech_to : str
            Technology label arrow head.

        Note: *Label* refers to the acronyms
        following naming convention and must be unique.
        """
        edge_params = self.get_params(index)
        edge_vars = self.get_variables(index)
        self.add_edge(tech_from,
                      tech_to,
                      fuel_label=fuel_label,
                      fuel_type=fuel_type,
                      index=index,
                      **edge_params,
                      **edge_vars)

    def add_region(self, index: str = "r"):
        """Set the region to be modeled."""
        pass

    def add_emission(self, index: str = "e"):
        """Include emission due to technology."""
        pass

    def add_year(self, index: str = "y"):
        """Define time frame of the model."""
        pass

    def add_timeslice(self, index: str = "l"):
        """Define time split of each modeled year."""
        pass

    def add_mode_of_operation(self, index: str = "m"):
        """Define the number of modes technologies can have."""
        pass

    def add_season(self, index: str = "ls"):
        """Indicate number of seasons."""
        pass

    def add_daytype(self, index: str = "ld"):
        """Indicate number of day types."""
        pass

    def add_dailytimebracket(self, index: str = "lh"):
        """Indicate number of parts the day is split into."""
        pass

    def add_storage(self, index: str = "s"):
        """Include storage facilities in the model."""
        pass

    def draw_res(self):
        """Draw RES network."""
        # Network structure
        pos = nx.multipartite_layout(self, subset_key="layer")
        # Retrieve commodities code
        fuel_labels = nx.get_edge_attributes(self, "fuel_label")
        # Draw RES
        options = {
            "node_size": 1000,
            "alpha": 0.6,
            "node_color": "blue",
            "font_size": 5,
            "font_weight": "bold",
            "arrowsize": 10
        }
        nx.draw_networkx(self, pos, **options)
        nx.draw_networkx_edge_labels(
            self,
            pos=pos,
            edge_labels=fuel_labels,
            font_color="blue"
        )
        plt.title("Reference Energy System (RES)")
        plt.show()


def main():
    """Build up RES estructure."""
    # Initialize a directed graph
    resnet = ResGraph()

    # Define conversion technologies
    resnet.add_technology("PWRHYD",
                          "Hydroelectric Power Plant",
                          layer=0)
    resnet.add_technology("PWRGEO",
                          "Geothermal Power Plant",
                          layer=0)
    resnet.add_technology("PWRSOL001",
                          "Photovoltaic Power Plant",
                          layer=0)
    resnet.add_technology("PWRDSL",
                          "Thermal Power Plant - Diesel",
                          layer=0)
    resnet.add_technology("PWRBIO",
                          "Biomass Power Plant",
                          layer=0)
    resnet.add_technology("PWRSOL002",
                          "Decentralised Solar PV",
                          layer=1)
    # Define transmission technology
    resnet.add_technology("PWRTRN",
                          "Transmission of Electricity",
                          layer=1)
    # Define distribution technology
    resnet.add_technology("PWRDIS",
                          "Distribution of Electricity",
                          layer=2)
    # Define demand technology
    resnet.add_technology("DEMRESELC",
                          "Residential Demand for Electricity",
                          layer=3)
    resnet.add_technology("DEMCOMELC",
                          "Commercial Demand for Electricity",
                          layer=3)
    resnet.add_technology("DEMINDELC",
                          "Industrial Demand for Electricity",
                          layer=3)
    resnet.add_technology("DEMTRAELC",
                          "Electric Vehicles",
                          layer=3)

    # Define arrows for commodity flows
    resnet.add_fuel(
        "PWRHYD",
        "PWRTRN",
        "ELC001",
        "Electricity before Transmission"
    )
    resnet.add_fuel(
        "PWRGEO",
        "PWRTRN",
        "ELC001",
        "Electricity before Transmission"
    )
    resnet.add_fuel(
        "PWRSOL001",
        "PWRTRN",
        "ELC001",
        "Electricity before Transmission"
    )
    resnet.add_fuel(
        "PWRDSL",
        "PWRTRN",
        "ELC001",
        "Electricity before Transmission"
    )
    resnet.add_fuel(
        "PWRBIO",
        "PWRTRN",
        "ELC001",
        "Electricity before Transmission"
    )
    resnet.add_fuel(
        "PWRTRN",
        "PWRDIS",
        "ELC002",
        "Electricity after Transmission"
    )
    resnet.add_fuel(
        "PWRSOL002",
        "PWRDIS",
        "ELC002",
        "Electricity after Transmissions"
    )
    resnet.add_fuel(
        "PWRDIS",
        "DEMRESELC",
        "ELC003",
        "Electricity for Residential Consumers"
    )
    resnet.add_fuel(
        "PWRDIS",
        "DEMCOMELC",
        "ELC003",
        "Electricity for Commercial Consumers"
    )
    resnet.add_fuel(
        "PWRDIS",
        "DEMINDELC",
        "ELC003",
        "Electricity for Industrial Consumers"
    )
    resnet.add_fuel(
        "PWRDIS",
        "DEMTRAELC",
        "ELC003",
        "Electricity for EV"
    )

    return resnet


if __name__ == "__main__":
    main()
