"""Download accessible bibliography PDFs from Unpaywall + direct URLs.

Usage:
    python3 scripts/download_sources.py

Downloads go into fuentes/ (already in .gitignore).
Results are logged to fuentes/download_log.json.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS_PATH = os.path.join(ROOT, "references.json")
FUENTES_DIR = os.path.join(ROOT, "fuentes")

SUBDIRS = {
    "articulos": os.path.join(FUENTES_DIR, "articulos"),
    "reportes": os.path.join(FUENTES_DIR, "reportes"),
    "legislacion": os.path.join(FUENTES_DIR, "legislacion"),
}

LOG_PATH = os.path.join(FUENTES_DIR, "download_log.json")

UNPAYWALL_EMAIL = "hesusgc@gmail.com"
UNPAYWALL_BASE = "https://api.unpaywall.org/v2"

USER_AGENT = "AulaDelFuturo-BibDownloader/1.0 (mailto:hesusgc@gmail.com)"

# References whose PDFs already live in libros/ — skip these
SKIP_IDS = {"diaz-barriga-2006"}

# Direct download URLs that don't need Unpaywall
DIRECT_DOWNLOADS = {
    "lges-2021": {
        "url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LGES_200421.pdf",
        "subdir": "legislacion",
        "filename": "LGES_200421.pdf",
    },
    "fraser-1982": {
        "url": "https://files.eric.ed.gov/fulltext/ED223649.pdf",
        "subdir": "reportes",
        "filename": "fraser-1982-LEI-MCI.pdf",
    },
    "fullan-langworthy-2014": {
        "url": "https://michaelfullan.ca/wp-content/uploads/2014/01/3897.Rich_Seam_web.pdf",
        "subdir": "reportes",
        "filename": "fullan-langworthy-2014-rich-seam.pdf",
    },
}

# UNESCO documents — try PDF download via unesdoc
UNESCO_DOWNLOADS = {
    "unesco-2015a": {
        "ark": "pf0000245656",
        "filename": "unesco-2015a-incheon.pdf",
    },
    "unesco-2015b": {
        "ark": "pf0000232555",
        "filename": "unesco-2015b-replantear-educacion.pdf",
    },
    "unesco-2018": {
        "ark": "pf0000265721",
        "filename": "unesco-2018-tic-docentes.pdf",
    },
    "unesco-2019": {
        "ark": "pf0000366994",
        "filename": "unesco-2019-ia-educacion.pdf",
    },
    "unesco-2020": {
        "ark": "pf0000373718",
        "filename": "unesco-2020-covid.pdf",
    },
    "unesco-2021": {
        "ark": "pf0000379707",
        "filename": "unesco-2021-reimaginar-futuros.pdf",
    },
    "unesco-2023": {
        "ark": "pf0000385723",
        "filename": "unesco-2023-gem-tecnologia.pdf",
    },
}


def ensure_dirs():
    """Create the fuentes/ directory structure."""
    for d in SUBDIRS.values():
        os.makedirs(d, exist_ok=True)
    print(f"Directory structure ready under {FUENTES_DIR}/")


def load_references():
    """Load references.json and return as list of dicts."""
    with open(REFS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sanitize_filename(name):
    """Turn a string into a safe filename."""
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"\s+", "-", name.strip())
    return name[:80]


def download_file(url, dest_path, max_redirects=5):
    """Download a file from url to dest_path using urllib. Returns True on success."""
    headers = {"User-Agent": USER_AGENT}
    req = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(req, timeout=60)
        content = response.read()

        # Check we actually got a PDF (or at least something substantial)
        if len(content) < 1000:
            print(f"    WARNING: Response too small ({len(content)} bytes), may not be a valid PDF")

        with open(dest_path, "wb") as f:
            f.write(content)

        size_kb = len(content) / 1024
        print(f"    Saved: {dest_path} ({size_kb:.0f} KB)")
        return True

    except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
        print(f"    Download failed: {e}")
        return False


def query_unpaywall(doi):
    """Query Unpaywall API for a DOI. Returns (pdf_url, oa_status) or (None, reason)."""
    url = f"{UNPAYWALL_BASE}/{doi}?email={UNPAYWALL_EMAIL}"
    headers = {"User-Agent": USER_AGENT}
    req = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(req, timeout=30)
        data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, "not_found_in_unpaywall"
        return None, f"http_error_{e.code}"
    except (urllib.error.URLError, OSError) as e:
        return None, f"network_error: {e}"

    # Try best_oa_location first
    best = data.get("best_oa_location")
    if best:
        pdf_url = best.get("url_for_pdf")
        if pdf_url:
            return pdf_url, "oa_pdf"

        # Fallback to landing page URL (not a direct PDF but logged)
        landing = best.get("url")
        if landing:
            return landing, "oa_landing_only"

    # Check all OA locations
    for loc in data.get("oa_locations", []):
        pdf_url = loc.get("url_for_pdf")
        if pdf_url:
            return pdf_url, "oa_pdf_alt"

    if data.get("is_oa"):
        return None, "oa_no_pdf_url"

    return None, "not_oa"


def classify_ref(ref):
    """Determine which subfolder a reference belongs to based on type/author."""
    ref_type = ref.get("type", "")
    ref_id = ref.get("id", "")
    authors = ref.get("author", [])
    author_names = [a.get("literal", "") or a.get("family", "") for a in authors]

    if ref_type == "legislation":
        return "legislacion"
    if any(name in ("UNESCO", "OECD", "OCDE", "SEP") for name in author_names):
        return "reportes"
    if ref_type in ("book",) and ref_id.startswith(("oecd-", "unesco-")):
        return "reportes"
    return "articulos"


def process_doi_references(refs, log):
    """Process all references that have a DOI via Unpaywall."""
    doi_refs = [r for r in refs if r.get("DOI") and r["id"] not in SKIP_IDS
                and r["id"] not in DIRECT_DOWNLOADS
                and r["id"] not in UNESCO_DOWNLOADS]

    print(f"\n{'='*60}")
    print(f"UNPAYWALL: Processing {len(doi_refs)} DOI references")
    print(f"{'='*60}")

    for ref in doi_refs:
        ref_id = ref["id"]
        doi = ref["DOI"]
        subdir_key = classify_ref(ref)
        dest_dir = SUBDIRS[subdir_key]

        print(f"\n  [{ref_id}] DOI: {doi}")

        pdf_url, status = query_unpaywall(doi)

        if pdf_url and status.startswith("oa_pdf"):
            filename = f"{ref_id}.pdf"
            dest_path = os.path.join(dest_dir, filename)

            print(f"    OA PDF found: {pdf_url}")
            success = download_file(pdf_url, dest_path)

            if success:
                log.append({
                    "ref_id": ref_id,
                    "doi": doi,
                    "status": "downloaded",
                    "path": os.path.relpath(dest_path, ROOT),
                    "url": pdf_url,
                })
            else:
                log.append({
                    "ref_id": ref_id,
                    "doi": doi,
                    "status": "error",
                    "url": pdf_url,
                    "error": "Download failed after finding OA URL",
                })
        elif status == "oa_landing_only":
            print(f"    OA landing page only (no direct PDF): {pdf_url}")
            log.append({
                "ref_id": ref_id,
                "doi": doi,
                "status": "not_oa",
                "url": pdf_url or "",
                "error": "Only landing page available, no direct PDF",
            })
        else:
            print(f"    Not available as OA: {status}")
            log.append({
                "ref_id": ref_id,
                "doi": doi,
                "status": "not_oa",
                "url": "",
                "error": status,
            })

        # Rate limit: 1 second between Unpaywall requests
        time.sleep(1)


def process_direct_downloads(log):
    """Download references with known direct URLs."""
    print(f"\n{'='*60}")
    print(f"DIRECT: Processing {len(DIRECT_DOWNLOADS)} direct downloads")
    print(f"{'='*60}")

    for ref_id, info in DIRECT_DOWNLOADS.items():
        url = info["url"]
        dest_dir = SUBDIRS[info["subdir"]]
        filename = info["filename"]
        dest_path = os.path.join(dest_dir, filename)

        print(f"\n  [{ref_id}] {url}")

        success = download_file(url, dest_path)
        if success:
            log.append({
                "ref_id": ref_id,
                "doi": "",
                "status": "downloaded",
                "path": os.path.relpath(dest_path, ROOT),
                "url": url,
            })
        else:
            log.append({
                "ref_id": ref_id,
                "doi": "",
                "status": "error",
                "url": url,
                "error": "Direct download failed",
            })

        time.sleep(1)


def process_unesco_downloads(log):
    """Try downloading UNESCO PDFs from unesdoc."""
    print(f"\n{'='*60}")
    print(f"UNESCO: Processing {len(UNESCO_DOWNLOADS)} UNESCO documents")
    print(f"{'='*60}")

    dest_dir = SUBDIRS["reportes"]

    for ref_id, info in UNESCO_DOWNLOADS.items():
        ark = info["ark"]
        filename = info["filename"]
        dest_path = os.path.join(dest_dir, filename)

        # UNESCO PDF download URL pattern
        # The actual PDF is usually at /ark:/48223/{ark} with content negotiation
        # or at a direct ?posInSet=... URL. We try a few patterns.
        pdf_url = f"https://unesdoc.unesco.org/ark:/48223/{ark}?posInSet=1&queryId=N-EXPLORE"

        print(f"\n  [{ref_id}] Trying: {pdf_url}")

        success = download_file(pdf_url, dest_path)

        if success:
            # Verify it's actually a PDF (check magic bytes)
            with open(dest_path, "rb") as f:
                header = f.read(5)
            if header == b"%PDF-":
                log.append({
                    "ref_id": ref_id,
                    "doi": "",
                    "status": "downloaded",
                    "path": os.path.relpath(dest_path, ROOT),
                    "url": pdf_url,
                })
                time.sleep(1)
                continue
            else:
                print(f"    Not a PDF (got HTML?), removing...")
                os.remove(dest_path)

        # Fallback: try direct ark URL
        pdf_url_alt = f"https://unesdoc.unesco.org/ark:/48223/{ark}"
        print(f"    Fallback: {pdf_url_alt}")
        success = download_file(pdf_url_alt, dest_path)

        if success:
            with open(dest_path, "rb") as f:
                header = f.read(5)
            if header == b"%PDF-":
                log.append({
                    "ref_id": ref_id,
                    "doi": "",
                    "status": "downloaded",
                    "path": os.path.relpath(dest_path, ROOT),
                    "url": pdf_url_alt,
                })
            else:
                print(f"    Fallback also not a PDF, removing...")
                os.remove(dest_path)
                log.append({
                    "ref_id": ref_id,
                    "doi": "",
                    "status": "error",
                    "url": pdf_url_alt,
                    "error": "UNESCO server returned HTML instead of PDF",
                })
        else:
            log.append({
                "ref_id": ref_id,
                "doi": "",
                "status": "error",
                "url": pdf_url,
                "error": "UNESCO download failed",
            })

        time.sleep(1)


def process_oecd_doi_downloads(refs, log):
    """OECD books have DOIs but need special handling (not in Unpaywall usually)."""
    oecd_refs = [r for r in refs if r.get("DOI") and r["id"].startswith("oecd-")]

    print(f"\n{'='*60}")
    print(f"OECD: Processing {len(oecd_refs)} OECD references via Unpaywall")
    print(f"{'='*60}")

    dest_dir = SUBDIRS["reportes"]

    for ref in oecd_refs:
        ref_id = ref["id"]
        doi = ref["DOI"]

        print(f"\n  [{ref_id}] DOI: {doi}")

        pdf_url, status = query_unpaywall(doi)

        if pdf_url and status.startswith("oa_pdf"):
            filename = f"{ref_id}.pdf"
            dest_path = os.path.join(dest_dir, filename)
            print(f"    OA PDF found: {pdf_url}")
            success = download_file(pdf_url, dest_path)

            if success:
                log.append({
                    "ref_id": ref_id,
                    "doi": doi,
                    "status": "downloaded",
                    "path": os.path.relpath(dest_path, ROOT),
                    "url": pdf_url,
                })
            else:
                log.append({
                    "ref_id": ref_id,
                    "doi": doi,
                    "status": "error",
                    "url": pdf_url,
                    "error": "Download failed after finding OA URL",
                })
        else:
            print(f"    Not available as OA: {status}")
            log.append({
                "ref_id": ref_id,
                "doi": doi,
                "status": "not_oa",
                "url": "",
                "error": status,
            })

        time.sleep(1)


def log_no_doi_refs(refs, log):
    """Log references that have no DOI and aren't handled by direct/UNESCO downloads."""
    handled = (
        set(DIRECT_DOWNLOADS.keys())
        | set(UNESCO_DOWNLOADS.keys())
        | SKIP_IDS
    )

    for ref in refs:
        ref_id = ref["id"]
        if ref.get("DOI") or ref_id in handled:
            continue
        # Check if already in log
        if any(e["ref_id"] == ref_id for e in log):
            continue

        log.append({
            "ref_id": ref_id,
            "doi": "",
            "status": "no_doi",
            "path": "",
            "url": ref.get("URL", ""),
            "error": "No DOI available; manual download may be needed",
        })


def save_log(log):
    """Write the download log."""
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    print(f"\nLog saved to {LOG_PATH}")


def print_summary(log):
    """Print a summary of results."""
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    by_status = {}
    for entry in log:
        s = entry["status"]
        by_status.setdefault(s, []).append(entry)

    for status, entries in sorted(by_status.items()):
        print(f"\n  {status.upper()} ({len(entries)}):")
        for e in entries:
            path_or_note = e.get("path") or e.get("error", "")
            print(f"    - {e['ref_id']}: {path_or_note}")


def main():
    print("Aula del Futuro — Bibliography Source Downloader")
    print(f"{'='*60}")

    ensure_dirs()
    refs = load_references()
    print(f"Loaded {len(refs)} references from {REFS_PATH}")

    log = []

    # 1) Process DOI references via Unpaywall (excluding OECD, direct, UNESCO)
    process_doi_references(refs, log)

    # 2) Process OECD DOI references via Unpaywall
    process_oecd_doi_downloads(refs, log)

    # 3) Direct downloads (LGES, ERIC, Fullan)
    process_direct_downloads(log)

    # 4) UNESCO documents
    process_unesco_downloads(log)

    # 5) Log references with no DOI
    log_no_doi_refs(refs, log)

    # Save and summarize
    save_log(log)
    print_summary(log)


if __name__ == "__main__":
    main()
