import pandas as pd
from pathlib import Path
import re
from collections import Counter

# --------------------------------------------------
# FILE LOADING
# --------------------------------------------------

def load_csv(path):
    return pd.read_csv(path)

def get_excel_sheets(path):
    xls = pd.ExcelFile(path)
    return xls.sheet_names

def load_sheet(path, sheet):
    return pd.read_excel(path, sheet_name=sheet)

def load_all_sheets(path):
    return pd.read_excel(path, sheet_name=None)

# --------------------------------------------------
# TEXT UTILITIES
# --------------------------------------------------

def dataframe_to_text(df):
    return " ".join(
        df.fillna("")
          .astype(str)
          .values.flatten()
    )

def count_phrase(df, phrase):
    text = dataframe_to_text(df)
    return text.lower().count(
        phrase.lower()
    )

def top_words(df, n=20):

    text = dataframe_to_text(df)

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        text.lower()
    )

    stopwords = {
        "the","and","is","in","to",
        "of","a","an","for","on",
        "at","with","by","from",
        "or","as","it"
    }

    words = [
        w for w in words
        if w not in stopwords
    ]

    return Counter(words).most_common(n)

# --------------------------------------------------
# DATASET ANALYSIS
# --------------------------------------------------

def sheet_statistics(df):

    stats = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": int(
            df.duplicated().sum()
        ),
        "missing_values": int(
            df.isnull().sum().sum()
        )
    }

    return stats

def print_statistics(df):

    stats = sheet_statistics(df)

    print("\nRows:", stats["rows"])
    print("Columns:", stats["columns"])
    print(
        "Duplicate Rows:",
        stats["duplicates"]
    )
    print(
        "Missing Values:",
        stats["missing_values"]
    )

    print("\nColumn Names:\n")

    for col in df.columns:
        print("-", col)

# --------------------------------------------------
# TOWN DETECTION
# --------------------------------------------------

KENYAN_TOWNS = {
    "nairobi",
    "mombasa",
    "kisumu",
    "nakuru",
    "eldoret",
    "thika",
    "machakos",
    "nyeri",
    "meru",
    "kitale",
    "malindi",
    "naivasha",
    "garissa",
    "isiolo",
    "kakamega",
    "busia",
    "kisii",
    "migori",
    "narok",
    "kiambu"
}

def find_towns(df):

    text = dataframe_to_text(df)

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        text.lower()
    )

    towns = [
        w for w in words
        if w in KENYAN_TOWNS
    ]

    return Counter(towns)

# --------------------------------------------------
# WORKBOOK SUMMARY
# --------------------------------------------------

def workbook_summary(path):

    sheets = load_all_sheets(path)

    summary = []

    for name, df in sheets.items():

        stats = sheet_statistics(df)

        summary.append({
            "Sheet": name,
            "Rows": stats["rows"],
            "Columns": stats["columns"],
            "Duplicates": stats["duplicates"],
            "MissingValues":
                stats["missing_values"]
        })

    return pd.DataFrame(summary)

# --------------------------------------------------
# EXPORT
# --------------------------------------------------

def export_summary(path):

    report = workbook_summary(path)

    outfile = (
        Path(path).stem
        + "_summary.xlsx"
    )

    report.to_excel(
        outfile,
        index=False
    )

    print(
        f"\nSummary exported:"
        f" {outfile}"
    )

# --------------------------------------------------
# ANALYZE SINGLE SHEET
# --------------------------------------------------

def analyze_sheet(path):

    sheets = get_excel_sheets(path)

    print("\nAvailable Sheets:\n")

    for i, sheet in enumerate(
        sheets,
        start=1
    ):
        print(f"{i}. {sheet}")

    choice = int(
        input("\nChoose sheet: ")
    )

    sheet_name = sheets[
        choice - 1
    ]

    df = load_sheet(
        path,
        sheet_name
    )

    print(
        f"\nAnalyzing:"
        f" {sheet_name}"
    )

    print_statistics(df)

    while True:

        print("\n")
        print("1 Search Phrase")
        print("2 Top Words")
        print("3 Find Towns")
        print("4 Show Head")
        print("0 Back")

        option = input("> ")

        if option == "1":

            while True:

                phrase = input(
                    "\nPhrase (0 to go back): "
                ).strip()

                if phrase == "0":
                    break

                count = count_phrase(
                    df,
                    phrase
                )

                print(
                    f"\nOccurrences: {count}"
                )

                mask = df.astype(str).apply(
                    lambda row:
                    row.str.contains(
                        phrase,
                        case=False,
                        na=False,
                        regex=False
                    ).any(),
                    axis=1
                )

                matches = df[mask]

                if len(matches) > 0:

                    print(
                        f"\nMatching Rows ({len(matches)} found):"
                    )

                    print(
                        matches.head(20)
                    )

                    if len(matches) > 20:
                        print(
                            f"\nShowing first 20 of {len(matches)} rows."
                        )

                else:

                    print(
                        "\nNo matching rows found."
                    )

        elif option == "2":

            for word, count in \
                top_words(df):

                print(
                    f"{word}: {count}"
                )

        elif option == "3":

            towns = find_towns(df)

            print("\nTowns:\n")

            if len(towns) == 0:

                print(
                    "No Kenyan towns found."
                )

            else:

                for town, count in \
                    towns.most_common():

                    print(
                        town.title(),
                        count
                    )

        elif option == "4":

            print(df.head())

        elif option == "0":

            break

        else:

            print(
                "Invalid option."
            )
# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print(
        "\nWORKBOOK ANALYZER"
    )

    filename = input(
        "\nEnter file path: "
    )

    if not Path(filename).exists():

        print("File not found")
        return

    if filename.lower().endswith(
        ".csv"
    ):

        df = load_csv(filename)

        print_statistics(df)

        return

    while True:

        print("\n")
        print(
            "1 Analyze Sheet"
        )

        print(
            "2 Workbook Summary"
        )

        print(
            "3 Export Summary"
        )

        print("0 Exit")

        choice = input("> ")

        if choice == "1":

            analyze_sheet(
                filename
            )

        elif choice == "2":

            print(
                workbook_summary(
                    filename
                )
            )

        elif choice == "3":

            export_summary(
                filename
            )

        elif choice == "0":
            break

if __name__ == "__main__":
    main()