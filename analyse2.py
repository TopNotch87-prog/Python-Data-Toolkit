import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter
from itertools import tee
from pathlib import Path

# ---------- LOAD FILE ----------

def load_file(path):
    if path.lower().endswith(".csv"):
        return pd.read_csv(path)

    elif path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)

    raise ValueError("Unsupported file type")

# ---------- CLEANING ----------

def clean_data(df):

    df = df.copy()

    df.columns = [
        str(c).strip().lower().replace(" ", "_")
        for c in df.columns
    ]

    before = len(df)

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    after = len(df)

    print(f"\nRemoved {before-after} duplicate rows")

    return df

# ---------- PROFILE ----------

def profile(df):

    print("\n=== DATASET PROFILE ===")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn Names:")
    print(list(df.columns))

    print("\nMissing Values:")
    print(df.isnull().sum())

    num = df.select_dtypes(include=np.number)

    if not num.empty:
        print("\nNumeric Summary:")
        print(num.describe())

# ---------- TEXT ----------

def all_text(df):
    return " ".join(
        df.fillna("").astype(str).values.flatten()
    )

def search_phrase(df, phrase):

    total = 0

    for col in df.columns:

        text = " ".join(
            df[col].fillna("").astype(str)
        )

        total += text.lower().count(
            phrase.lower()
        )

    return total

def regex_search(df, pattern):

    text = all_text(df)

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    return matches

# ---------- WORDS ----------

def top_words(text, n=20):

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    stop = {
        "the","and","is","in","to","of",
        "a","an","for","on","at","with",
        "by","from","or","as","it"
    }

    words = [
        w for w in words
        if w not in stop
    ]

    return Counter(words).most_common(n)

def bigrams(words):

    a, b = tee(words)

    next(b, None)

    return zip(a, b)

def top_bigrams(text, n=20):

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    pairs = [
        " ".join(x)
        for x in bigrams(words)
    ]

    return Counter(pairs).most_common(n)

# ---------- OUTLIERS ----------

def detect_outliers(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    for col in numeric.columns:

        q1 = numeric[col].quantile(0.25)
        q3 = numeric[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = numeric[
            (numeric[col] < lower)
            | (numeric[col] > upper)
        ]

        print(
            f"\n{col}: {len(outliers)} outliers"
        )

# ---------- CORRELATION ----------

def correlations(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    if numeric.empty:
        return

    print("\nCorrelation Matrix:")
    print(numeric.corr())

# ---------- CHARTS ----------

def create_charts(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    if numeric.empty:
        print("No numeric columns")
        return

    output = Path("charts")
    output.mkdir(exist_ok=True)

    for col in numeric.columns:

        plt.figure()

        df[col].hist()

        plt.title(col)

        plt.savefig(
            output / f"{col}.png"
        )

        plt.close()

    print("\nCharts saved")

# ---------- EXPORT ----------

def export_clean(df, original):

    ext = Path(original).suffix

    outfile = (
        Path(original).stem
        + "_cleaned"
        + ext
    )

    if ext == ".csv":
        df.to_csv(outfile, index=False)
    else:
        df.to_excel(outfile, index=False)

    print(
        f"\nSaved cleaned file: {outfile}"
    )

# ---------- MAIN ----------

def main():

    path = input(
        "Enter CSV/XLS/XLSX path: "
    )

    df = load_file(path)

    while True:

        print("\n=== MENU ===")
        print("1 Profile")
        print("2 Search Phrase")
        print("3 Regex Search")
        print("4 Top Words")
        print("5 Top Bigrams")
        print("6 Clean Data")
        print("7 Correlations")
        print("8 Outliers")
        print("9 Charts")
        print("10 Export Clean")
        print("0 Exit")

        choice = input("> ")

        if choice == "1":
            profile(df)

        elif choice == "2":

            phrase = input(
                "Phrase: "
            )

            print(
                search_phrase(
                    df,
                    phrase
                )
            )

        elif choice == "3":

            pattern = input(
                "Regex: "
            )

            print(
                regex_search(
                    df,
                    pattern
                )[:50]
            )

        elif choice == "4":

            text = all_text(df)

            for w, c in top_words(text):
                print(w, c)

        elif choice == "5":

            text = all_text(df)

            for w, c in top_bigrams(text):
                print(w, c)

        elif choice == "6":
            df = clean_data(df)

        elif choice == "7":
            correlations(df)

        elif choice == "8":
            detect_outliers(df)

        elif choice == "9":
            create_charts(df)

        elif choice == "10":
            export_clean(df, path)

        elif choice == "0":
            break

if __name__ == "__main__":
    main()