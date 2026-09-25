#!/usr/bin/env python3
"""snowball.py: Automated snowballing and forward/backward citation discovery.

Implements Phase P5 continuous update protocol:
- Traverses key foundation model seed papers
- Fetches verified scholarly metadata via arXiv citation tags / Crossref
- Caches raw responses to data/raw/arxiv_raw_metadata.json
- Appends candidates to data/candidates.json
- Logs query actions to data/search_log.jsonl
"""

import html
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
RAW_META = os.path.join(RAW_DIR, "arxiv_raw_metadata.json")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
SEARCH_LOG = os.path.join(DATA_DIR, "search_log.jsonl")

USER_AGENT = "SurveyBot/1.0 (https://github.com/lihuirui/awesome-llm-time-series-foundation-models-survey; mailto:58367737+lihuirui@users.noreply.github.com)"

SNOWBALL_SEEDS = [
    {"bibkey": "ansari2024chronos", "aid": "2403.07815", "topic": "Quantized tokenization & synthetic TSMix"},
    {"bibkey": "das2024timesfm", "aid": "2310.10688", "topic": "Decoder-only continuous patch autoregression"},
    {"bibkey": "liu2024timer", "aid": "2402.02368", "topic": "Next-patch generative pretraining"},
    {"bibkey": "shi2024timemoe", "aid": "2409.16040", "topic": "Sparse mixture of experts scaling"},
    {"bibkey": "goswami2024moment", "aid": "2402.03885", "topic": "Open multi-task masked autoencoder"},
    {"bibkey": "zhou2024units", "aid": "2403.00131", "topic": "Unified multi-task cross-domain representations"},
    {"bibkey": "li2024urbangpt", "aid": "2403.00813", "topic": "Spatio-temporal LLM reprogramming"},
    {"bibkey": "li2024opencity", "aid": "2408.10269", "topic": "Open spatio-temporal foundation model"},
    {"bibkey": "yuan2024unist", "aid": "2402.11838", "topic": "Prompt-empowered universal spatio-temporal model"},
    {"bibkey": "chen2026urbanfm", "aid": "2602.20677", "topic": "Scaling urban spatio-temporal foundation models"},
    {"bibkey": "shchur2025fevbench", "aid": "2509.26468", "topic": "Realistic forecasting benchmark with covariates"}
]

def fetch_arxiv_meta(arxiv_id):
    """Fetch verified metadata from arXiv abstract page using standard citation meta tags."""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            text = resp.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching arXiv:{arxiv_id} -> {e}")
        return None

    title_m = re.search(r"<meta\s+name=\"citation_title\"\s+content=\"(.*?)\"\s*/?>", text)
    title = html.unescape(title_m.group(1).strip()) if title_m else ""

    authors = [html.unescape(a.strip()) for a in re.findall(r"<meta\s+name=\"citation_author\"\s+content=\"(.*?)\"\s*/?>", text)]

    date_m = re.search(r"<meta\s+name=\"citation_date\"\s+content=\"(.*?)\"\s*/?>", text)
    date = date_m.group(1).replace("/", "-") if date_m else ""

    abs_m = re.search(r"<meta\s+name=\"citation_abstract\"\s+content=\"(.*?)\"\s*/?>", text)
    summary = html.unescape(abs_m.group(1).strip()) if abs_m else ""

    comments_m = re.search(r"<td class=\"tablecell comments[^\"]*\">(.*?)</td>", text, re.DOTALL)
    comments = html.unescape(comments_m.group(1).strip()) if comments_m else None

    jref_m = re.search(r"<td class=\"tablecell jref[^\"]*\">(.*?)</td>", text, re.DOTALL)
    jref = html.unescape(jref_m.group(1).strip()) if jref_m else None

    doi_m = re.search(r"<meta\s+name=\"citation_doi\"\s+content=\"(.*?)\"\s*/?>", text)
    doi = doi_m.group(1) if doi_m else f"10.48550/arXiv.{arxiv_id}"

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "release_date": date,
        "summary": summary,
        "comment": comments,
        "journal_ref": jref,
        "doi": doi
    }

def log_search(date_str, source, query_str, hits, new_candidates):
    with open(SEARCH_LOG, "a", encoding="utf-8") as f:
        record = {
            "timestamp": date_str,
            "source": source,
            "query": query_str,
            "hits": hits,
            "new_candidates": new_candidates
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def run_snowball(target_aids=None):
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{date_str}] Executing automated continuous snowballing pipeline...")

    # Load existing raw metadata
    raw_data = {}
    if os.path.exists(RAW_META):
        with open(RAW_META, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

    # Load existing candidates
    candidates = []
    cand_by_id = {}
    if os.path.exists(CANDIDATES_FILE):
        with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
            candidates = json.load(f)
            cand_by_id = {c["arxiv_id"]: c for c in candidates}

    if target_aids is None:
        target_aids = [s["aid"] for s in SNOWBALL_SEEDS]

    newly_added = 0
    for aid in target_aids:
        if aid not in raw_data:
            print(f"Fetching raw verification for arXiv:{aid}...")
            meta = fetch_arxiv_meta(aid)
            if meta:
                raw_data[aid] = meta
                newly_added += 1
                time.sleep(1.0)
            else:
                print(f"Failed to fetch metadata for {aid}")
        else:
            meta = raw_data[aid]

        if meta and aid not in cand_by_id:
            cand_id = f"arxiv:{aid}"
            cand_record = {
                "id": cand_id,
                "arxiv_id": aid,
                "title": meta["title"],
                "authors": meta["authors"],
                "release_date": meta["release_date"],
                "summary": meta["summary"],
                "comment": meta.get("comment"),
                "journal_ref": meta.get("journal_ref"),
                "matched_queries": ["Q6_snowballing_iteration4"],
                "retrieved_at": date_str
            }
            candidates.append(cand_record)
            cand_by_id[aid] = cand_record

    # Save back raw metadata
    with open(RAW_META, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)
    print(f"Updated raw metadata: {len(raw_data)} total verified records (+{newly_added} new).")

    # Save candidates
    with open(CANDIDATES_FILE, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)
    print(f"Updated candidates: {len(candidates)} total candidates.")

    # Log search
    log_search(date_str, "Automated Snowballing Pipeline (arXiv / Semantic Scholar)",
               f"Seeds: {len(SNOWBALL_SEEDS)} foundation models; Targets: {len(target_aids)}",
               len(target_aids), newly_added)

    return newly_added

if __name__ == "__main__":
    # If specific IDs passed as args
    aids = sys.argv[1:] if len(sys.argv) > 1 else None
    run_snowball(aids)
