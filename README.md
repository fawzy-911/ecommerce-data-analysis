# E-Commerce Data Analysis with Pandas

Explore the UCI Online Retail transactions by taking a reproducible 10% sample, cleaning the records, calculating revenue, and charting the top 10 countries.

**Roadmap project:** <https://roadmap.sh/projects/ecommerce-data-analysis>

## Requirements

- Python 3.10 or later
- Internet access for downloading the source dataset

## Run the analysis

```bash
python -m venv .venv
```

Activate the environment, then install the packages and download the dataset:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

python -m pip install -r requirements.txt
python download_data.py
python analyze_retail.py
```

The script selects a seeded 10% sample, removes rows missing required fields, converts dates and numeric columns, excludes canceled/return transactions and zero or negative prices, then adds `Revenue = Quantity × UnitPrice`.

Results are written to `outputs/`:

- `cleaned_retail_sample.csv`
- `top_10_countries_by_revenue.csv`
- `top_10_countries_by_revenue.png`

To explore the same workflow interactively, open `ecommerce_analysis.ipynb` after installing the requirements:

```bash
jupyter notebook ecommerce_analysis.ipynb
```

## Data source and attribution

Chen, D. (2015). **Online Retail** [Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5BW33>. The dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The original workbook is downloaded locally and is not committed to this repository.

