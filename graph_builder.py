import osmnx as ox
import torch

class GraphBuilder:
    def __init__(self, location_name, data_mgr):
        self.location_name = location_name
        self.dm = data_mgr
        self.graph = None
        self.mapping = {}

    def download_map(self):
        print(f"Downloading road network for {self.location_name}...")
        self.graph = ox.graph_from_place(self.location_name, network_type='drive')
        self.mapping = {node: i for i, node in enumerate(self.graph.nodes())}
        return self.graph

    def build_tensors(self):
        """This is the method your main.py is calling."""
        if self.graph is None:
            self.download_map()
            
        edge_index = []
        edge_weights = []

        print("Calculating dynamic traffic weights...")
        # Limiting to 50 edges for the initial test to save API calls
        for i, (u, v, data) in enumerate(self.graph.edges(data=True)):
            if i > 50: break
            
            distance = data.get('length', 100)
            u_lat, u_lon = self.graph.nodes[u]['y'], self.graph.nodes[u]['x']
            
            # Fetch speed from your DataManager
            current_speed = self.dm.get_live_traffic(u_lat, u_lon)
            
            # Innovation: Weight = Distance / Speed_t
            weight = distance / (max(current_speed, 5) * 0.277) 
            
            edge_index.append([self.mapping[u], self.mapping[v]])
            edge_weights.append(weight)

        return torch.tensor(edge_index, dtype=torch.long).t().contiguous(), torch.tensor(edge_weights, dtype=torch.float)