import pandas as pd
import networkx as nx

# === Step 1: Load the cleaned dataset ===
file_path = "/content/sample_data/scientific_software_classified_cleaned.csv"
df = pd.read_csv(file_path)

# === Step 2: Clean the 'mapped_labels' column (convert comma-separated strings to lists) ===
df["mapped_labels"] = df["mapped_labels"].fillna("").apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])

# Also clean 'cleaned_classification' if needed (ensure it's a list, even if single entry)
df["cleaned_classification"] = df["cleaned_classification"].fillna("").apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])

# === Step 3: Create the bipartite graph ===
B = nx.Graph()

for _, row in df.iterrows():
    domains = row["cleaned_classification"]
    skills = row["mapped_labels"]

    for domain in domains:
        B.add_node(domain, type="domain")
        for skill in skills:
            B.add_node(skill, type="skill")
            B.add_edge(skill, domain)

# === Step 4: Print basic stats ===
print(f"✅ Bipartite Graph created!")
print(f"Total nodes: {B.number_of_nodes()}")
print(f"Total edges: {B.number_of_edges()}")
print(f"Skill nodes: {len([n for n, d in B.nodes(data=True) if d['type'] == 'skill'])}")
print(f"Domain nodes: {len([n for n, d in B.nodes(data=True) if d['type'] == 'domain'])}")

# !pip install torch torch-geometric scikit-learn
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import negative_sampling
from sklearn.metrics import roc_auc_score

# Step 1: Define GraphSAGE model
class LinkPredictor(nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super().__init__()
        self.sage1 = SAGEConv(in_channels, hidden_channels)
        self.sage2 = SAGEConv(hidden_channels, hidden_channels)
        self.link_predictor = nn.Sequential(
            nn.Linear(hidden_channels * 2, hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, 1)
        )

    def encode(self, x, edge_index):
        h = self.sage1(x, edge_index).relu()
        h = self.sage2(h, edge_index)
        return h

    def decode(self, h, edge_pairs):
        src = h[edge_pairs[0]]
        dst = h[edge_pairs[1]]
        out = torch.cat([src, dst], dim=1)
        return self.link_predictor(out).squeeze()

# Step 2: Prepare model and data
model = LinkPredictor(in_channels=data.num_node_features, hidden_channels=128)
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
epochs = 100

# Step 3: Training loop
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()

    # Encode node features
    h = model.encode(data.x, data.edge_index)

    # Positive edges (true skill-domain links)
    pos_edge_index = data.edge_index

    # Negative edges (random pairs)
    neg_edge_index = negative_sampling(
        edge_index=data.edge_index,
        num_nodes=data.num_nodes,
        num_neg_samples=pos_edge_index.size(1)
    )

    # Predict scores
    pos_preds = model.decode(h, pos_edge_index)
    neg_preds = model.decode(h, neg_edge_index)

    # Labels and loss
    pos_labels = torch.ones(pos_preds.size(0))
    neg_labels = torch.zeros(neg_preds.size(0))
    labels = torch.cat([pos_labels, neg_labels])
    preds = torch.cat([pos_preds, neg_preds])

    loss = F.binary_cross_entropy_with_logits(preds, labels)
    loss.backward()
    optimizer.step()

    # Evaluation metric
    with torch.no_grad():
        auc = roc_auc_score(labels.cpu(), preds.sigmoid().cpu())
        print(f"Epoch {epoch+1:03d} | Loss: {loss.item():.4f} | AUC: {auc:.4f}")
