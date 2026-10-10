from data_utils import make_demo_data

df = make_demo_data()
df.to_csv("data/campaigns_demo.csv", index=False)
print(f"Created data/campaigns_demo.csv with {len(df)} rows and {df['campaign_id'].nunique()} campaigns.")
