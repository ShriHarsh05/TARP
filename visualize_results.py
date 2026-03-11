"""
Visualization script for DT-GCN Risk Assessment Results
Creates multiple visualizations to showcase the project output
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import osmnx as ox
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_results():
    """Load the risk assessment results"""
    df = pd.read_csv('DT_GCN_Vellore_Results.csv')
    print(f"Loaded {len(df)} nodes with risk scores")
    return df

def create_risk_distribution_plot(df):
    """Create histogram of risk score distribution"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(df['Risk_Score'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].axvline(df['Risk_Score'].mean(), color='red', linestyle='--', 
                    linewidth=2, label=f'Mean: {df["Risk_Score"].mean():.3f}')
    axes[0].axvline(df['Risk_Score'].median(), color='green', linestyle='--', 
                    linewidth=2, label=f'Median: {df["Risk_Score"].median():.3f}')
    axes[0].set_xlabel('Risk Score', fontsize=12)
    axes[0].set_ylabel('Number of Nodes', fontsize=12)
    axes[0].set_title('Distribution of Risk Scores Across Vellore', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Box plot
    box_data = [
        df[df['Risk_Score'] <= 0.33]['Risk_Score'],
        df[(df['Risk_Score'] > 0.33) & (df['Risk_Score'] <= 0.67)]['Risk_Score'],
        df[df['Risk_Score'] > 0.67]['Risk_Score']
    ]
    bp = axes[1].boxplot(box_data, labels=['Low\n(0-0.33)', 'Medium\n(0.33-0.67)', 'High\n(0.67-1.0)'],
                         patch_artist=True)
    
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    axes[1].set_ylabel('Risk Score', fontsize=12)
    axes[1].set_title('Risk Score by Category', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('risk_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: risk_distribution.png")
    plt.close()

def create_risk_categories_plot(df):
    """Create pie chart and bar chart of risk categories"""
    # Categorize risk levels
    df['Risk_Category'] = pd.cut(df['Risk_Score'], 
                                  bins=[0, 0.33, 0.67, 1.0],
                                  labels=['Low Risk', 'Medium Risk', 'High Risk'])
    
    category_counts = df['Risk_Category'].value_counts()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Pie chart
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    explode = (0.05, 0.05, 0.1)
    axes[0].pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
                colors=colors, explode=explode, shadow=True, startangle=90)
    axes[0].set_title('Risk Category Distribution', fontsize=14, fontweight='bold')
    
    # Bar chart with counts
    bars = axes[1].bar(category_counts.index, category_counts.values, color=colors, alpha=0.7, edgecolor='black')
    axes[1].set_ylabel('Number of Nodes', fontsize=12)
    axes[1].set_title('Node Count by Risk Category', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}\n({height/len(df)*100:.1f}%)',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('risk_categories.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: risk_categories.png")
    plt.close()

def create_top_risk_nodes_plot(df):
    """Create visualization of top high-risk and low-risk nodes"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Top 10 highest risk
    top_high = df.nlargest(10, 'Risk_Score')
    axes[0].barh(range(len(top_high)), top_high['Risk_Score'], color='#e74c3c', alpha=0.7, edgecolor='black')
    axes[0].set_yticks(range(len(top_high)))
    axes[0].set_yticklabels([f"Node {int(nid)}" for nid in top_high['Node_ID']], fontsize=9)
    axes[0].set_xlabel('Risk Score', fontsize=12)
    axes[0].set_title('Top 10 Highest Risk Nodes', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='x')
    axes[0].invert_yaxis()
    
    # Add value labels
    for i, (idx, row) in enumerate(top_high.iterrows()):
        axes[0].text(row['Risk_Score'] + 0.02, i, f"{row['Risk_Score']:.3f}",
                    va='center', fontsize=9, fontweight='bold')
    
    # Top 10 lowest risk
    top_low = df.nsmallest(10, 'Risk_Score')
    axes[1].barh(range(len(top_low)), top_low['Risk_Score'], color='#2ecc71', alpha=0.7, edgecolor='black')
    axes[1].set_yticks(range(len(top_low)))
    axes[1].set_yticklabels([f"Node {int(nid)}" for nid in top_low['Node_ID']], fontsize=9)
    axes[1].set_xlabel('Risk Score', fontsize=12)
    axes[1].set_title('Top 10 Lowest Risk Nodes', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='x')
    axes[1].invert_yaxis()
    
    # Add value labels
    for i, (idx, row) in enumerate(top_low.iterrows()):
        axes[1].text(row['Risk_Score'] + 0.02, i, f"{row['Risk_Score']:.3f}",
                    va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('top_risk_nodes.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: top_risk_nodes.png")
    plt.close()

def create_statistics_summary(df):
    """Create a summary statistics visualization"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Calculate statistics
    stats = {
        'Total Nodes Analyzed': len(df),
        'Mean Risk Score': f"{df['Risk_Score'].mean():.4f}",
        'Median Risk Score': f"{df['Risk_Score'].median():.4f}",
        'Std Deviation': f"{df['Risk_Score'].std():.4f}",
        'Min Risk Score': f"{df['Risk_Score'].min():.4f}",
        'Max Risk Score': f"{df['Risk_Score'].max():.4f}",
        'High Risk Nodes (>0.67)': len(df[df['Risk_Score'] > 0.67]),
        'Medium Risk Nodes (0.33-0.67)': len(df[(df['Risk_Score'] > 0.33) & (df['Risk_Score'] <= 0.67)]),
        'Low Risk Nodes (<0.33)': len(df[df['Risk_Score'] <= 0.33]),
    }
    
    # Create table
    table_data = [[key, value] for key, value in stats.items()]
    table = ax.table(cellText=table_data, colLabels=['Metric', 'Value'],
                    cellLoc='left', loc='center', colWidths=[0.6, 0.4])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Style header
    for i in range(2):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        if i % 2 == 0:
            table[(i, 0)].set_facecolor('#ecf0f1')
            table[(i, 1)].set_facecolor('#ecf0f1')
    
    plt.title('DT-GCN Risk Assessment - Summary Statistics\nVellore, Tamil Nadu, India',
             fontsize=16, fontweight='bold', pad=20)
    
    plt.savefig('statistics_summary.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: statistics_summary.png")
    plt.close()

def create_map_visualization(df):
    """Create a map visualization with risk scores"""
    try:
        print("\nDownloading Vellore road network for map visualization...")
        G = ox.graph_from_place("Vellore, Tamil Nadu, India", network_type='drive')
        
        # Create node colors based on risk scores
        node_colors = []
        node_sizes = []
        
        for node in G.nodes():
            node_data = df[df['Node_ID'] == node]
            if not node_data.empty:
                risk = node_data['Risk_Score'].values[0]
                # Color mapping: green (low) -> yellow (medium) -> red (high)
                if risk < 0.33:
                    node_colors.append('#2ecc71')
                    node_sizes.append(10)
                elif risk < 0.67:
                    node_colors.append('#f39c12')
                    node_sizes.append(15)
                else:
                    node_colors.append('#e74c3c')
                    node_sizes.append(25)
            else:
                node_colors.append('#95a5a6')
                node_sizes.append(5)
        
        # Plot
        fig, ax = ox.plot_graph(G, node_color=node_colors, node_size=node_sizes,
                                edge_color='#bdc3c7', edge_linewidth=0.5,
                                bgcolor='white', show=False, close=False,
                                figsize=(15, 15))
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#e74c3c', label='High Risk (0.67-1.0)'),
            Patch(facecolor='#f39c12', label='Medium Risk (0.33-0.67)'),
            Patch(facecolor='#2ecc71', label='Low Risk (0.0-0.33)'),
            Patch(facecolor='#95a5a6', label='No Data')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=12)
        ax.set_title('DT-GCN Risk Map - Vellore, Tamil Nadu\nDynamic Traffic-Weighted Risk Assessment',
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.savefig('risk_map_vellore.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: risk_map_vellore.png")
        plt.close()
        
    except Exception as e:
        print(f"⚠ Map visualization skipped: {e}")
        print("  (This requires internet connection and may take time)")

def print_summary_report(df):
    """Print a text summary report"""
    print("\n" + "="*70)
    print("DT-GCN RISK ASSESSMENT REPORT - VELLORE, TAMIL NADU")
    print("="*70)
    
    print(f"\n📊 DATASET OVERVIEW")
    print(f"   Total Nodes Analyzed: {len(df):,}")
    print(f"   Risk Score Range: {df['Risk_Score'].min():.4f} - {df['Risk_Score'].max():.4f}")
    print(f"   Mean Risk Score: {df['Risk_Score'].mean():.4f}")
    print(f"   Median Risk Score: {df['Risk_Score'].median():.4f}")
    
    print(f"\n🎯 RISK DISTRIBUTION")
    high_risk = len(df[df['Risk_Score'] > 0.67])
    medium_risk = len(df[(df['Risk_Score'] > 0.33) & (df['Risk_Score'] <= 0.67)])
    low_risk = len(df[df['Risk_Score'] <= 0.33])
    
    print(f"   🔴 High Risk (>0.67):     {high_risk:,} nodes ({high_risk/len(df)*100:.1f}%)")
    print(f"   🟡 Medium Risk (0.33-0.67): {medium_risk:,} nodes ({medium_risk/len(df)*100:.1f}%)")
    print(f"   🟢 Low Risk (<0.33):      {low_risk:,} nodes ({low_risk/len(df)*100:.1f}%)")
    
    print(f"\n⚠️  TOP 5 HIGHEST RISK NODES")
    for i, (idx, row) in enumerate(df.nlargest(5, 'Risk_Score').iterrows(), 1):
        print(f"   {i}. Node {int(row['Node_ID'])}: Risk Score = {row['Risk_Score']:.4f}")
    
    print(f"\n✅ TOP 5 LOWEST RISK NODES")
    for i, (idx, row) in enumerate(df.nsmallest(5, 'Risk_Score').iterrows(), 1):
        print(f"   {i}. Node {int(row['Node_ID'])}: Risk Score = {row['Risk_Score']:.4f}")
    
    print("\n" + "="*70)
    print("VISUALIZATIONS GENERATED")
    print("="*70)
    print("   1. risk_distribution.png - Histogram and box plots")
    print("   2. risk_categories.png - Pie chart and bar chart")
    print("   3. top_risk_nodes.png - Top 10 high/low risk nodes")
    print("   4. statistics_summary.png - Summary table")
    print("   5. risk_map_vellore.png - Geographic risk map (if generated)")
    print("="*70 + "\n")

def main():
    print("="*70)
    print("DT-GCN VISUALIZATION GENERATOR")
    print("="*70)
    
    # Load data
    df = load_results()
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    create_risk_distribution_plot(df)
    create_risk_categories_plot(df)
    create_top_risk_nodes_plot(df)
    create_statistics_summary(df)
    
    # Print summary
    print_summary_report(df)
    
    # Optional: Create map (can be slow)
    response = input("Generate geographic risk map? (This may take 1-2 minutes) [y/n]: ")
    if response.lower() == 'y':
        create_map_visualization(df)
    
    print("\n✓ All visualizations complete!")
    print("  Check the current directory for PNG files.")

if __name__ == "__main__":
    main()
