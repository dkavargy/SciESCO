import pandas as pd

# Load your dataset (replace with your actual file path or upload logic in Colab)
df = pd.read_csv('/content/sample_data/softxANDsoft_impc.csv')

# Check the language column
print("Unique languages in dataset:", df['Language of Original Document'].unique())

# Filter only English-language papers
df_english = df[df['Language of Original Document'].str.lower() == 'english']

# Show how many papers remain
print("Remaining papers after EC1 (English only):", len(df_english))


# EC2: Filter out non-research types
excluded_types = [
    "editorial", "review", "keynote", "poster", "panel",
    "book", "note", "erratum", "conference paper"
]

# Normalize to lowercase for matching
df_english['Document Type Clean'] = df_english['Document Type'].str.lower()

# Filter: keep only papers that are NOT in the excluded types
df_research_only = df_english[~df_english['Document Type Clean'].isin(excluded_types)]

# Print result
print("Remaining papers after EC2 (research articles only):", len(df_research_only))

# Save filtered dataset
df_research_only.to_csv("filtered_after_EC2.csv", index=False)
print("Saved as: filtered_after_EC2.csv")

import pandas as pd

# STEP 1: Load your previously filtered CSV from EC2
df_research_only = pd.read_csv("/content/filtered_after_EC2.csv")

# STEP 2: EC3 - Stricter detection of third-party dependence
strict_keywords = [
    "based on existing software", "built on top of", "uses commercial software",
    "commercial tool", "existing library", "existing tool", "existing framework",
    "integrated third-party software", "adapted from existing", "wrapper for existing",
    "extension of existing software", "plugin for existing software", "commercial package",
    "proprietary system", "not developed in-house", "leveraged existing software",
    "software provided by vendor"
]

# Clean and normalize abstract text
df_research_only["abstract_clean"] = df_research_only["Abstract"].str.lower().fillna("")

# Flag entries that mention reliance on third-party software
def flag_third_party(text):
    return any(phrase in text for phrase in strict_keywords)

df_research_only["third_party_flag"] = df_research_only["abstract_clean"].apply(flag_third_party)

# STEP 3: Filter out flagged papers
df_no_third_party = df_research_only[~df_research_only["third_party_flag"]]

# Save the final result after EC3
df_no_third_party.to_csv("filtered_after_EC3.csv", index=False)
print("Remaining after EC3 (third-party filtered):", len(df_no_third_party))
print("Saved as: filtered_after_EC3.csv")


import pandas as pd

# STEP 1: Load your previously filtered CSV from EC2
df_research_only = pd.read_csv("/content/filtered_after_EC2.csv")

# STEP 2: EC3 - Stricter detection of third-party dependence
strict_keywords = [
    "based on existing software", "built on top of", "uses commercial software",
    "commercial tool", "existing library", "existing tool", "existing framework",
    "integrated third-party software", "adapted from existing", "wrapper for existing",
    "extension of existing software", "plugin for existing software", "commercial package",
    "proprietary system", "not developed in-house", "leveraged existing software",
    "software provided by vendor"
]

# STEP 3: Normalize and clean abstract text
df_research_only["abstract_clean"] = df_research_only["Abstract"].str.lower().fillna("")

# STEP 4: Flag abstracts that mention third-party dependence
def flag_strict_third_party(text):
    return any(kw in text for kw in strict_keywords)

df_research_only["third_party_flag"] = df_research_only["abstract_clean"].apply(flag_strict_third_party)

# STEP 5: Print first 10 abstracts that were flagged
flagged_papers = df_research_only[df_research_only["third_party_flag"]]
print("Total flagged papers (EC3 stricter):", len(flagged_papers))
print(flagged_papers[["Title", "Abstract"]].head(10))

# STEP 6 (optional): Save filtered data without third-party software
df_no_third_party = df_research_only[~df_research_only["third_party_flag"]]
df_no_third_party.to_csv("filtered_after_EC3.csv", index=False)
print("Saved as: filtered_after_EC3.csv")
