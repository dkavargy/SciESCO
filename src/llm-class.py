marketing_domains = [
    "Digital Marketing",
    "Consumer Behavior",
    "Marketing Analytics",
    "Brand Management",
    "Content Marketing",
    "Social Media Marketing",
    "International Marketing",
    "Marketing Strategy"
]


def build_marketing_curriculum_prompt(domain):
    return f"""
You are an expert curriculum designer working for a European university.

Your task is to create a synthetic but realistic **undergraduate marketing course** in the field of **{domain}**. This course should align with European university standards, targeting Bachelor's students in Business or Marketing programs.

Please generate the following information:

- **Course Title**: A clear and engaging course name
- **Short Description**: A concise summary (50words) of the course, including what it covers and why it's relevant in today’s marketing landscape
- **Learning Outcomes**: 3–5 specific, measurable outcomes that students are expected to achieve by the end of the course
- **Skills Acquired**: 5–10 concrete skills students will gain (technical, analytical, or strategic)
- **Semester**: Recommended semester within a typical 3-year Bachelor's structure (e.g., 2nd or 5th semester)

Respond in the following format:

Course Title: ...
Description: ...
Learning Outcomes:
- ...
Skills:
- ...
Semester: ...
""".strip()

def generate_curriculum(prompt):
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
        return result.get("response", "").strip()
    except Exception as e:
        print(f"❌ Error generating curriculum: {e}")
        return None

synthetic_curricula = []

for domain in science_domains:
    print(f"\n📘 Generating curriculum for: {domain}")
    prompt = build_curriculum_prompt(domain)
    result = generate_curriculum(prompt)
    if result:
        print(f"✅ Result for {domain}:\n{result}\n")
        synthetic_curricula.append({
            "Domain": domain,
            "Generated Output": result
        })

import pandas as pd

df_curricula = pd.DataFrame(synthetic_curricula)
df_curricula.to_csv("/content/synthetic_curricula.csv", index=False)

print("\n✅ Saved to: synthetic_curricula.csv")
