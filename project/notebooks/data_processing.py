import pandas as pd
import glob
import os

# Ensure processed and reports folders exist
os.makedirs("C:/Users/Shabnam/project/data/processed", exist_ok=True)
os.makedirs("C:/Users/Shabnam/project/reports", exist_ok=True)

def process_csvs(path="C:/Users/Shabnam/project/data/raw/*.csv",
                 report_file="C:/Users/Shabnam/project/reports/data_processing_report.md"):
    files = glob.glob(path)
    with open(report_file, "w", encoding="utf-8") as report:
        report.write("# 🧹 Data Processing Report\n")

        if not files:
            msg = "No CSV files found in data/raw/"
            print(msg)
            report.write(f"\n⚠️ {msg}\n")
            return

        for f in files:
            try:
                df = pd.read_csv(f)
                filename = os.path.basename(f)

                # Count anomalies before cleaning
                duplicates = df.duplicated().sum()
                missing = df.isnull().sum()

                # Clean data
                df = df.drop_duplicates()
                df = df.fillna(method="ffill").fillna(method="bfill")

                # Save to processed folder
                out_path = f"C:/Users/Shabnam/project/data/processed/{filename}"
                df.to_csv(out_path, index=False)

                # Console output
                print(f"Processed and saved: {out_path}")

                # Write to Markdown report
                report.write(f"\n## 📂 {filename}\n")
                report.write(f"- **Original shape:** {df.shape}\n")
                report.write(f"- **Duplicates removed:** {duplicates}\n")

                if missing.any():
                    report.write("\n- ⚠️ **Missing values per column (before fill):**\n```\n")
                    report.write(f"{missing}\n```\n")
                else:
                    report.write("- ✅ No missing values detected\n")

                report.write(f"- **Cleaned file saved to:** `data/processed/{filename}`\n")

            except Exception as e:
                error_msg = f"Error processing {f}: {e}"
                print(error_msg)
                report.write(f"\n❌ {error_msg}\n")

    print(f"\nMarkdown processing report written to {report_file}")

if __name__ == "__main__":
    process_csvs()
