# 🔬 SCIESCO: Skill–Domain Intelligence for Scientific Software Communities

> A GNN-powered framework for mapping, predicting, and analyzing skill–domain links in scientific software development (SSD)

![License](https://img.shields.io/github/license/yourusername/sciesco)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![PyTorch Geometric](https://img.shields.io/badge/Framework-PyTorchGeometric-green)
![Status](https://img.shields.io/badge/Status-ResearchPrototype-orange)

---

## 🚀 Overview

**SCIESCO** (Skill–Domain Co-occurrence) is a research-driven tool designed to:
- Extract skills from scientific software using ESCO taxonomy
- Build co-occurrence graphs between skills and scientific domains
- Predict emerging or disappearing links using Graph Neural Networks (GNNs)
- Support science policy, curriculum design, and upskilling strategy

![SCIESCO Graph](images/Sci_esco_graph%20(1).png)


> Developed as part of the [SKILLAB EU Project](https://skillab.eu/), and validated on real SSD publications & policies.

---

## 🧠 Features

- 🧩 **Skill Extraction** using NLP & the ESCO ontology  
- 🌐 **Graph Construction** from bibliometric or policy sources  
- 🧠 **GNN-based Link Prediction** with PyTorch Geometric  
- 📊 **Skill Disruption Metrics** (mortality, novelty, centrality, etc.)  
- 📦 Modular, extensible design for your own datasets  

---

## 📸 Screenshots

| Skill–Domain Graph | Emerging Skills | Disruptive Skills |
|--------------------|-----------------|-------------------|
| ![graph](assets/graph.png) | ![growth](assets/growth.png) | ![weak](assets/weak.png) |

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/sciesco.git
cd sciesco
pip install -r requirements.txt
```
```bash
sciesco/
├── data/                  # Sample datasets
├── notebooks/             # Jupyter notebooks for exploration
├── src/                   # Core code (models, utils, pipeline)
├── assets/                # Images for README/plots
├── requirements.txt       # Dependencies
└── README.md              # This file
```

