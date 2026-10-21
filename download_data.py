"""Download the UCI Online Retail dataset into the local data directory."""

from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import io


DATA_URL = "https://archive.ics.uci.edu/static/public/352/online%2Bretail.zip"
DATA_DIR = Path(__file__).parent / "data"
EXCEL_FILE = DATA_DIR / "OnlineRetail.xlsx"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if EXCEL_FILE.exists():
        print(f"Dataset already exists: {EXCEL_FILE}")
        return

    print("Downloading the UCI Online Retail dataset...")
    with urlopen(DATA_URL, timeout=60) as response:
        archive_bytes = response.read()

    with ZipFile(io.BytesIO(archive_bytes)) as archive:
        candidates = [name for name in archive.namelist() if name.lower().endswith(".xlsx")]
        if not candidates:
            raise RuntimeError("The downloaded archive did not contain an Excel workbook.")
        EXCEL_FILE.write_bytes(archive.read(candidates[0]))

    print(f"Saved dataset to: {EXCEL_FILE}")


if __name__ == "__main__":
    main()

