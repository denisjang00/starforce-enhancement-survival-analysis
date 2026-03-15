import pandas as pd
import os

def export_results(results, path="output/ab_results.csv"):
    os.makedirs("output", exist_ok=True)

    df = pd.DataFrame(results)
    df.to_csv(path, index=False)

    print("Saved:", path)