"""Fetch the original UCI workbook without adding third-party download dependencies."""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "Online Retail.xlsx"
URL = "https://archive.ics.uci.edu/static/public/352/online%2Bretail.zip"
EXPECTED_SHA256 = "43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d"


def main():
    if TARGET.exists():
        if sha256(TARGET.read_bytes()).hexdigest() == EXPECTED_SHA256:
            print("Original workbook already present; checksum verified.")
            return
        raise SystemExit("Existing workbook has a different checksum. Review it before replacing it.")

    print("Downloading the original UCI Online Retail archive...")
    request = Request(URL, headers={"User-Agent": "OnlineRetailAnalysis/1.0"})
    try:
        with urlopen(request, timeout=120) as response:
            archive_bytes = response.read()
        with ZipFile(BytesIO(archive_bytes)) as archive:
            matches = [name for name in archive.namelist()
                       if Path(name).name == "Online Retail.xlsx"]
            if len(matches) != 1:
                raise ValueError("Expected exactly one Online Retail.xlsx workbook in the archive.")
            workbook = archive.read(matches[0])
        if sha256(workbook).hexdigest() != EXPECTED_SHA256:
            raise ValueError("Downloaded workbook checksum differs from the project source; file not saved.")
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_bytes(workbook)
        print("Saved data/Online Retail.xlsx; checksum verified.")
    except Exception as error:
        raise SystemExit(
            f"Download failed: {error}\n"
            "Use the UCI dataset page and follow data/README.md for manual download."
        ) from error


if __name__ == "__main__":
    main()
