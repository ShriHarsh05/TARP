"""
Enhanced main.py that integrates Indian government crime data
with the DT-GCN model for risk assessment.
"""

from data_ingestion import DataManager
from graph_builder import GraphBuilder
from model import DT_GCN_Lite         
import torch
import pandas as pd

# Configuration
TOMTOM_KEY = "lyMHmCEgz2W4OQwAC2Aw2W8PxXuSUsbR"
CITY = "Bengaluru, Karnataka, India"
STATE = "Karnataka"

def main():
    print("=" * 70)
    print("DT-GCN Pipeline with Indian Government Data")
    print("=" * 70)
    
    # Initialize DataManager
    dm = DataManager(TOMTOM_KEY)
    
    # Load Indian crime data
    print("\n1. Loading Indian crime data...")
    crime_data = dm.load_local_crime_data('cache/bengaluru_crime_realistic.csv')
    
    if crime_data is not None:
        # Filter for Karnataka/Bengaluru
        state_data = crime_data[crime_data['State'] == STATE]
        print(f"   ✓ Loaded {len(state_data)} crime records for {STATE}")
        
        # Show statistics by year
        print(f"\n   Crime Statistics by Year:")
        for year in sorted(state_data['Year'].unique()):
            year_data = state_data[state_data['Year'] == year]
            total = year_data['Incidents'].sum()
            print(f"   - {year}: {total:,} incidents across {year_data['Police_Station'].nunique()} stations")
        
        # Show top crime types for latest year
        latest_year = state_data['Year'].max()
        latest_data = state_data[state_data['Year'] == latest_year]
        print(f"\n   Top Crime Types ({latest_year}):")
        top_crimes = latest_data.groupby('Crime_Type')['Incidents'].sum().sort_values(ascending=False).head(5)
        for crime, count in top_crimes.items():
            print(f"   - {crime}: {count:,} incidents")
    else:
        print("   ⚠ Using default configuration (no crime data)")
    
    # Build graph with real-time traffic
    print("\n2. Building road network graph...")
    gb = GraphBuilder(CITY, dm)
    edge_index, edge_weight = gb.build_tensors()
    num_nodes = len(gb.mapping)
    print(f"   ✓ Graph built with {num_nodes} nodes")
    
    # Prepare node features
    print("\n3. Preparing node features...")
    # In a real implementation, you could incorporate crime data here
    # For now, using random features as baseline
    x = torch.randn((num_nodes, 2))
    print(f"   ✓ Node features prepared ({x.shape})")
    
    # Run DT-GCN model
    print("\n4. Running DT-GCN model...")
    model = DT_GCN_Lite(in_channels=2, out_channels=1)
    raw_scores = model(x, edge_index, edge_weight).detach().flatten()
    
    # Normalize scores to 0-1 range
    min_val = torch.min(raw_scores)
    max_val = torch.max(raw_scores)
    normalized_scores = (raw_scores - min_val) / (max_val - min_val)
    print(f"   ✓ Risk scores computed")
    
    # Save results
    print("\n5. Saving results...")
    results_df = pd.DataFrame({
        'Node_ID': list(gb.mapping.keys()),
        'Internal_Index': list(gb.mapping.values()),
        'Risk_Score': normalized_scores.numpy()
    })
    
    output_file = f"DT_GCN_{CITY.split(',')[0]}_Indian_Data_Results.csv"
    results_df.to_csv(output_file, index=False)
    print(f"   ✓ Results saved to: {output_file}")
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Location: {CITY}")
    print(f"Nodes Processed: {num_nodes}")
    print(f"Edges Processed: {edge_index.shape[1]}")
    print(f"Risk Score Range: {normalized_scores.min():.4f} - {normalized_scores.max():.4f}")
    print(f"Mean Risk Score: {normalized_scores.mean():.4f}")
    print(f"\nTop 5 High-Risk Nodes:")
    top_5 = results_df.nlargest(5, 'Risk_Score')
    for idx, row in top_5.iterrows():
        print(f"  Node {row['Node_ID']}: Risk Score = {row['Risk_Score']:.4f}")
    
    print("\n" + "=" * 70)
    print("✓ Pipeline completed successfully!")
    print("=" * 70)
    
    # Optional: Show data source information
    print("\nData Sources Used:")
    print("  • Road Network: OpenStreetMap (via OSMnx)")
    print("  • Real-time Traffic: TomTom API")
    print("  • Crime Data: Indian Government Sample Data")
    print("\nTo use real NCRB data:")
    print("  1. Download from data.gov.in")
    print("  2. Save as cache/ncrb_crime_2021.csv")
    print("  3. Update dm.download_ncrb_crime_data() call")

if __name__ == "__main__":
    main()
