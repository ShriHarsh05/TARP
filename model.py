import torch
import torch.nn as nn

class DT_GCN_Lite(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DT_GCN_Lite, self).__init__()
        self.lin = nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index, edge_weight):
        row, col = edge_index
        # Spatial Aggregation: weight * neighbor_feature
        out = torch.zeros((x.size(0), x.size(1)), device=x.device)
        
        # Ensure weights are shaped correctly for multiplication
        msg = edge_weight.view(-1, 1) * x[col]
        out.index_add_(0, row, msg)
        
        return self.lin(out)