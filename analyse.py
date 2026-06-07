import os
import pandas as pd

files = [f for f in os.listdir() if f.endswith((".xlsx", ".xls"))]

print("\nExcel files found:")
for f in files:
    print(" -", f)

filename = input("\nEnter file name: ")

df = pd.read_excel(filename)

print("\nRows:", len(df))
print("Columns:", len(df.columns))
print(df.head())

import pandas as pd
from collections import Counter
import re
from tkinter import Tk, filedialog


def load_file(file_path):
    try:
        if file_path.lower().endswith(".csv"):
            return pd.read_csv(file_path)

        elif file_path.lower().endswith((".xlsx", ".xls")):
            return pd.read_excel(file_path)

        else:
            raise ValueError("Only CSV, XLS and XLSX files are supported.")

    except Exception as e:
        print(f"\nError loading file:\n{e}")
        return None


def get_all_text(df):
    return " ".join(
        df.fillna("").astype(str).values.flatten()
    )


def search_phrase(df, phrase):
    phrase = phrase.lower()

    total_count = 0
    column_counts = {}

    for col in df.columns:

        col_text = " ".join(
            df[col].fillna("").astype(str)
        )

        count = col_text.lower().count(phrase)

        if count > 0:
            column_counts[col] = count

        total_count += count

    return total_count, column_counts


def top_words(text, n=20):

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    stopwords = {
        "the", "and", "is", "in", "to",
        "of", "a", "an", "for", "on",
        "at", "with", "by", "from",
        "or", "as", "it", "this",
        "that", "are", "was", "were"
    }

    words = [w for w in words if w not in stopwords]

    return Counter(words).most_common(n)


def dataset_statistics(df):

    print("\n" + "=" * 50)
    print("DATASET STATISTICS")
    print("=" * 50)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn Names:")
    for col in df.columns:
        print(f" - {col}")

    print("\nMissing Values:")
    print(df.isnull().sum())

    numeric = df.select_dtypes(include="number")

    if not numeric.empty:
        print("\nNumeric Summary:")
        print(numeric.describe())


def choose_file():

    root = Tk()
    root.withdraw()

    filename = filedialog.askopenfilename(
        title="Select CSV or Excel File",
        filetypes=[
            ("Data Files", "*.csv *.xlsx *.xls"),
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx *.xls")
        ]
    )

    return filename


def main():

    print("\nCSV / EXCEL ANALYZER")

    file_path = choose_file()

    if not file_path:
        print("No file selected.")
        return

    print(f"\nLoaded: {file_path}")

    df = load_file(file_path)

    if df is None:
        return

    dataset_statistics(df)

    text = get_all_text(df)

    while True:

        print("\n")
        print("1 - Search word/phrase")
        print("2 - Show top 20 words")
        print("3 - Exit")

        choice = input("\nChoose: ").strip()

        if choice == "1":

            phrase = input(
                "\nEnter word or phrase: "
            ).strip()

            total, cols = search_phrase(
                df,
                phrase
            )

            print("\nRESULTS")
            print("-" * 30)
            print(f"Phrase: {phrase}")
            print(f"Occurrences: {total:,}")

            if cols:
                print("\nBy Column:")
                for col, count in sorted(
                    cols.items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    print(f"{col}: {count:,}")

        elif choice == "2":

            print("\nTOP WORDS")
            print("-" * 30)

            for word, count in top_words(text):
                print(
                    f"{word:<20} {count:,}"
                )

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
