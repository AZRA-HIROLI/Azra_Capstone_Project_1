import pandas, numpy, matplotlib, seaborn, plotly, sqlalchemy, requests, scipy, jupyter
print("All packages loaded successfully!")

import pandas as pd
import glob
import os

# Ensure reports folder exists
os.makedirs("C:/Users/Shabnam/project/reports", exist_ok=True)

def load_csvs(path="C:/Users/Shabnam/project/data/raw/*.csv",
              report_file="C:/Users/Shabnam/project/reports/data_ingestion_report.md"):
    files = glob.glob(path)
    with open(report_file, "w", encoding="utf-8") as report:
        report.write("# 📊 Data Ingestion Report\n")

        if not files:
            msg = "No CSV files found in data/raw/"
            print(msg)
            report.write(f"\n⚠️ {msg}\n")
            return

        for f in files:
            try:
                df = pd.read_csv(f)
                filename = os.path.basename(f)

                # Console output
                print(f"\n=== {filename} ===")
                print("Shape:", df.shape)
                print("Dtypes:\n", df.dtypes)
                print("Head:\n", df.head())

                # Write to Markdown report
                report.write(f"\n## 📂 {filename}\n")
                report.write(f"- **Shape:** {df.shape}\n")
                report.write(f"- **Dtypes:**\n```\n{df.dtypes}\n```\n")
                report.write(f"- **Head:**\n```\n{df.head()}\n```\n")

                # Anomaly checks
                missing = df.isnull().sum()
                duplicates = df.duplicated().sum()

                if missing.any():
                    print("⚠️ Missing values detected")
                    report.write("\n- ⚠️ **Missing values per column:**\n```\n")
                    report.write(f"{missing}\n```\n")
                else:
                    report.write("\n- ✅ No missing values detected\n")

                if duplicates > 0:
                    print(f"⚠️ {duplicates} duplicate rows detected")
                    report.write(f"- ⚠️ **{duplicates} duplicate rows detected**\n")
                else:
                    report.write("- ✅ No duplicate rows detected\n")

            except Exception as e:
                error_msg = f"Error loading {f}: {e}"
                print(error_msg)
                report.write(f"\n❌ {error_msg}\n")

    print(f"\nMarkdown ingestion report written to {report_file}")

if __name__ == "__main__":
    load_csvs()
