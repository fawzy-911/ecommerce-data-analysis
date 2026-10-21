"""Sample, clean, and analyze the UCI Online Retail transactions."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_DIR = Path(__file__).parent
DATA_FILE = PROJECT_DIR / "data" / "OnlineRetail.xlsx"
OUTPUT_DIR = PROJECT_DIR / "outputs"
SAMPLE_SEED = 42


def load_sample(path: Path = DATA_FILE, fraction: float = 0.10) -> pd.DataFrame:
    """Read the source workbook and select a reproducible 10% row sample."""
    if not path.exists():
        raise FileNotFoundError("Dataset not found. Run `python download_data.py` first.")
    raw = pd.read_excel(path, engine="openpyxl")
    return raw.sample(frac=fraction, random_state=SAMPLE_SEED).copy()


def clean_transactions(sample: pd.DataFrame) -> pd.DataFrame:
    """Drop incomplete records, normalize types, and exclude returns/free items."""
    data = sample.copy()
    data.columns = data.columns.str.strip()
    required = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]
    data = data.dropna(subset=required)

    data["InvoiceNo"] = data["InvoiceNo"].astype("string").str.strip()
    data["StockCode"] = data["StockCode"].astype("string").str.strip()
    data["Description"] = data["Description"].astype("string").str.strip()
    data["Country"] = data["Country"].astype("string").str.strip()
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["UnitPrice"] = pd.to_numeric(data["UnitPrice"], errors="coerce")
    data["CustomerID"] = pd.to_numeric(data["CustomerID"], errors="coerce").astype("Int64")
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")
    data = data.dropna(subset=["Quantity", "UnitPrice", "CustomerID", "InvoiceDate"])

    is_return = data["InvoiceNo"].str.upper().str.startswith("C", na=False) | (data["Quantity"] <= 0)
    is_free = data["UnitPrice"] <= 0
    data = data.loc[~is_return & ~is_free].copy()
    data["Quantity"] = data["Quantity"].astype("int64")
    data["Revenue"] = data["Quantity"] * data["UnitPrice"]
    return data.reset_index(drop=True)


def revenue_by_country(cleaned: pd.DataFrame) -> pd.DataFrame:
    """Return the top 10 countries ranked by revenue."""
    return (
        cleaned.groupby("Country", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )


def save_results(cleaned: pd.DataFrame, countries: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_DIR / "cleaned_retail_sample.csv", index=False)
    countries.to_csv(OUTPUT_DIR / "top_10_countries_by_revenue.csv", index=False)

    chart_data = countries.sort_values("Revenue")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(chart_data["Country"], chart_data["Revenue"], color="#2f6fed")
    ax.set_title("Top 10 Countries by Revenue (10% Sample)")
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("Country")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: f"£{value:,.0f}"))
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "top_10_countries_by_revenue.png", dpi=160)
    plt.close(fig)


def main() -> None:
    sample = load_sample()
    cleaned = clean_transactions(sample)
    countries = revenue_by_country(cleaned)
    save_results(cleaned, countries)

    print(f"Sampled rows: {len(sample):,}")
    print(f"Clean rows:   {len(cleaned):,}")
    print("\nTop 10 countries by revenue:")
    print(countries.to_string(index=False, formatters={"Revenue": "£{:,.2f}".format}))
    print(f"\nOutputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

