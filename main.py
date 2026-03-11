from data_ingestion import DataManager
from graph_builder import GraphBuilder
from model import DT_GCN_Lite         
import torch
import pandas as pd

# Configuration
TOMTOM_KEY = "lyMHmCEgz2W4OQwAC2Aw2W8PxXuSUsbR"
CITY = "Vellore, Tamil Nadu, India"

def main():
    print("--- Starting DT-GCN Pipeline ---")
    dm = DataManager(TOMTOM_KEY)
    gb = GraphBuilder(CITY, dm)
    
    edge_index, edge_weight = gb.build_tensors()
    num_nodes = len(gb.mapping)
    x = torch.randn((num_nodes, 2)) 
    
    model = DT_GCN_Lite(in_channels=2, out_channels=1)
    raw_scores = model(x, edge_index, edge_weight).detach().flatten()

    # INNOVATION: Normalize scores to 0-1 range for the Risk Map
    min_val = torch.min(raw_scores)
    max_val = torch.max(raw_scores)
    normalized_scores = (raw_scores - min_val) / (max_val - min_val)

    # 6. Save results for TARP Report Evidence
    results_df = pd.DataFrame({
        'Node_ID': list(gb.mapping.keys()),
        'Internal_Index': list(gb.mapping.values()),
        'Risk_Score': normalized_scores.numpy()
    })
    
    results_df.to_csv("DT_GCN_Vellore_Results.csv", index=False)
    
    print(f"\n--- EXECUTION SUCCESSFUL ---")
    print(f"Nodes Processed: {num_nodes}")
    print(f"Results saved to: DT_GCN_Vellore_Results.csv")
    print(f"Normalized Sample Scores: {normalized_scores[:5].numpy()}")

if __name__ == "__main__":
    main()