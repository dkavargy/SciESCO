from tqdm import tqdm
import torch

# 1. Get skill and domain nodes
skills = [n for n, d in B.nodes(data=True) if d["type"] == "skill"]
domains = [n for n, d in B.nodes(data=True) if d["type"] == "domain"]

skill_ids = [node2id[s] for s in skills]
domain_ids = [node2id[d] for d in domains]

# 2. Generate all possible (skill, domain) pairs that are not already in the graph
existing_edges = set((node2id[u], node2id[v]) for u, v in B.edges())
candidate_pairs = []
for s in tqdm(skill_ids, desc="Generating pairs"):
    for d in domain_ids:
        if (s, d) not in existing_edges and (d, s) not in existing_edges:
            candidate_pairs.append((s, d))

# 3. Encode node embeddings
model.eval()
h = model.encode(data.x, data.edge_index)

# 4. Predict scores for all candidate edges
edge_tensor = torch.tensor(candidate_pairs, dtype=torch.long).t()
scores = model.decode(h, edge_tensor).sigmoid()

# 5. Get top N predictions
top_k = 30  # Change to 50 or 100 as needed
top_indices = torch.topk(scores, k=top_k).indices
top_edges = [candidate_pairs[i] for i in top_indices]

# 6. Map node IDs back to names
top_predictions = [(le.classes_[s], le.classes_[d], float(scores[i])) for i, (s, d) in zip(top_indices, top_edges)]

# 7. Display results
print("🔮 Top Predicted Skill–Domain Links:")
for i, (skill, domain, score) in enumerate(top_predictions, 1):
    print(f"{i:02d}. Skill: {skill} ↔ Domain: {domain} → Score: {score:.4f}")
