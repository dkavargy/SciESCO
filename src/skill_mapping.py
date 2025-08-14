import pandas as pd

# === File paths ===
skills_file_path = '/content/sample_data/scientific_software_with_esco_skills.csv'
esco_mapping_file_path = '/content/sample_data/ESCO_Mapping_csv.csv'
output_file_path = 'mapped_skills_output_ssd.csv'

# === Load input data ===
skills_df = pd.read_csv(skills_file_path, encoding='utf-8', on_bad_lines='skip')
esco_mapping_df = pd.read_csv(esco_mapping_file_path, encoding='utf-8', delimiter=';', on_bad_lines='skip')

# === Debug: check column names ===
print("✅ Columns in skills_df:", skills_df.columns.tolist())
print("✅ Columns in esco_mapping_df:", esco_mapping_df.columns.tolist())

# === Ensure required columns exist ===
if 'conceptUri' in esco_mapping_df.columns and 'preferredLabel' in esco_mapping_df.columns:

    # === Create a mapping dictionary from URI → label ===
    concept_to_label = esco_mapping_df.set_index('conceptUri')['preferredLabel'].to_dict()

    # === Function to map a comma-separated list of URIs to labels ===
    def map_esco_uris(uri_string):
        if pd.isna(uri_string):
            return ""
        uris = [u.strip() for u in uri_string.split(',')]
        labels = [concept_to_label.get(uri, 'Unknown') for uri in uris if uri]
        return ", ".join(labels)

    # === Apply mapping to 'esco_skills' column ===
    if 'esco_skills' in skills_df.columns:
        skills_df['mapped_labels'] = skills_df['esco_skills'].apply(map_esco_uris)

        # === Save to final output ===
        skills_df.to_csv(output_file_path, index=False, encoding='utf-8')
        print(f"\n✅ Mapping completed. File saved as: {output_file_path}")
    else:
        print("❌ Error: 'skills_uris' column not found in input file.")
else:
    print("❌ Error: 'conceptUri' or 'preferredLabel' not found in ESCO mapping file.")
