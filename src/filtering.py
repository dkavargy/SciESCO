import pandas as pd

# Load your dataset (replace with your actual file path or upload logic in Colab)
df = pd.read_csv('/content/sample_data/softxANDsoft_impc.csv')

# Check the language column
print("Unique languages in dataset:", df['Language of Original Document'].unique())

# Filter only English-language papers
df_english = df[df['Language of Original Document'].str.lower() == 'english']

# Show how many papers remain
print("Remaining papers after EC1 (English only):", len(df_english))
