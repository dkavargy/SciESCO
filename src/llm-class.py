import pandas as pd
from tqdm import tqdm
import requests

# === Step 1: Load your dataset ===
df = pd.read_csv("/content/sample_data/mapped_skills_output_ssd (2).csv")  # Adjust path if needed

# === Step 2: Define the 9 Science-Metrix categories ===
categories = [
    "Life Sciences",
    "Physical Sciences",
    "Mathematics & Statistics",
    "Computer & Information Sciences",
    "Engineering & Technology",
    "Environmental & Agricultural Sciences",
    "Social & Behavioral Sciences",
    "Humanities & Arts",
    "Other"
]

# # === Step 3: Build prompt for each paper ===
# def build_prompt(title, keywords, abstract, skills):
#     return f"""
# You are an expert in classifying scientific papers.

# Classify the following paper into ONE of these 9 Science-Metrix domains:
# {', '.join(categories)}

# Title: {title}
# Author Keywords: {keywords}
# Abstract: {abstract}
# Extracted Skills: {skills}

# Return ONLY the best matching category from the list above. If unsure, return "Other".
# Your answer:
# """.strip()

def build_prompt(title, keywords, abstract, skills):
    categories_description = """
Classify the paper into one or more of the following 9 Science-Metrix domains:

1. Life Sciences – Research related to biology, biomedical sciences, clinical medicine, health, and genetics. Focuses on living organisms and life processes.

2. Physical Sciences – Includes physics, astronomy, and chemistry. Studies non-living systems, matter, energy, and the fundamental forces of nature.

3. Mathematics & Statistics – Covers theoretical and applied mathematics, pure logic, and statistical modeling or data science foundations.

4. Computer & Information Sciences – Encompasses software engineering, machine learning, AI, databases, computational theory, and information systems.

5. Engineering & Technology – Applied sciences focused on building, optimizing, or designing physical systems, hardware, industrial processes, or infrastructure.

6. Environmental & Agricultural Sciences – Related to agriculture, forestry, ecology, and earth/environmental science. Focuses on sustainability, ecosystems, and resource management.

7. Social & Behavioral Sciences – Studies involving psychology, education, economics, politics, or human behavior at the individual or societal level.

8. Humanities & Arts – Includes philosophy, literature, history, culture, theology, and creative disciplines such as music, film, or visual arts.

9. Other – Use this if the paper cannot reasonably be classified in any of the above domains.
""".strip()

    return f"""
You are a domain expert assisting with the classification of scientific software development papers.

Each paper was sourced from peer-reviewed publications such as *SoftwareX* and *Software Impacts*, and includes:
- A scientific software description
- Extracted ESCO skills
- Author keywords
- Title and abstract

Your task is to classify the **scientific domain** of the software based on the provided information.

{categories_description}

Return one or more relevant categories based on the paper's title, abstract, author keywords, and ESCO-aligned skills. Use commas to separate multiple categories, if applicable.

Title: {title}
Author Keywords: {keywords}
Abstract: {abstract}
Extracted ESCO Skills: {skills}

Return the matching Science-Metrix category/categories (comma-separated if needed):
""".strip()


# === Step 4: Call LLaMA 3 via Ollama (running locally) ===
def classify_with_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3:8b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        output = result.get("response", "").strip()
        return output
    except Exception as e:
        print(f"⚠️ Ollama error: {e}")
        return "Other"

# === Step 5: Loop through each paper and classify ===
classifications = []

print("🚀 Starting classification process...\n")
for idx, row in tqdm(df.iterrows(), total=len(df), desc="Classifying papers"):
    title = row.get("Title", "")
    keywords = row.get("Author Keywords", "")
    abstract = row.get("Abstract", "")
    skills = row.get("mapped_labels", "")

    prompt = build_prompt(title, keywords, abstract, skills)
    category = classify_with_ollama(prompt)

    print(f"\n📄 Paper {idx+1}")
    print(f"Prompt →\n{prompt[:300]}...")  # Preview first 300 chars of prompt
    print(f"🧠 LLaMA Response: {category}\n")

    classifications.append(category)

# === Step 6: Save results ===
df["science_metrix_classification"] = classifications
df.to_csv("/content/scientific_software_classified.csv", index=False)

print("\n✅ Classification complete. File saved as: scientific_software_classified.csv")
