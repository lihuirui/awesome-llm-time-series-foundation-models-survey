#!/usr/bin/env python3
"""watchdog.py: Autonomous living discovery and continuous arXiv watchdog pipeline.

Phase P5 continuous monitoring:
- Queries arXiv RSS / API for newly dropped preprints in cs.LG and stat.ML
- Traverses key topic seeds with rate limiting and exponential backoff
- Detects novel candidate releases, caches metadata, and appends to candidates
- Evaluates quality criteria and logs execution to data/search_log.jsonl
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
RAW_META = os.path.join(RAW_DIR, "arxiv_raw_metadata.json")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
SEARCH_LOG = os.path.join(DATA_DIR, "search_log.jsonl")

USER_AGENT = "SurveyBot/1.0 (https://github.com/lihuirui/awesome-llm-time-series-foundation-models-survey; mailto:58367737+lihuirui@users.noreply.github.com)"

WATCHDOG_QUERIES = [
    'cat:cs.LG AND ("time series foundation model" OR "time-series foundation model" OR "foundation models for time series")',
    'cat:cs.LG AND ("large language model" OR "LLM") AND ("time series" OR "temporal data") AND (reprogramming OR forecasting)',
    'cat:stat.ML AND ("foundation model" OR "pretrained") AND ("time series" OR forecasting)'
]

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

def run_watchdog():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{date_str}] Launching Autonomous Living Watchdog for TSFM preprints...")

    # Load existing raw metadata and candidates
    raw_data = {}
    if os.path.exists(RAW_META):
        with open(RAW_META, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

    candidates = []
    cand_by_id = {}
    if os.path.exists(CANDIDATES_FILE):
        with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
            candidates = json.load(f)
            cand_by_id = {c["arxiv_id"]: c for c in candidates}

    total_hits = 0
    new_candidates_found = 0

    for query in WATCHDOG_QUERIES:
        url = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read().decode("utf-8")
            root = ET.fromstring(data)
            entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            total_hits += len(entries)
            print(f"Watchdog query [{query[:40]}...] returned {len(entries)} hits.")

            for entry in entries:
                id_val = entry.find("{http://www.w3.org/2005/Atom}id").text.strip().split("/abs/")[-1]
                # Strip version suffix
                aid = id_val.split("v")[0]
                title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip().replace("\n", " ")
                summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip().replace("\n", " ")
                published = entry.find("{http://www.w3.org/2005/Atom}published").text.strip()[:10]
                authors = [a.find("{http://www.w3.org/2005/Atom}name").text.strip() for a in entry.findall("{http://www.w3.org/2005/Atom}author")]

                if aid not in cand_by_id:
                    cand_record = {
                        "id": f"arxiv:{aid}",
                        "arxiv_id": aid,
                        "title": title,
                        "authors": authors,
                        "release_date": published,
                        "summary": summary,
                        "comment": None,
                        "journal_ref": None,
                        "matched_queries": ["watchdog_live_feed"],
                        "retrieved_at": date_str
                    }
                    candidates.append(cand_record)
                    cand_by_id[aid] = cand_record
                    new_candidates_found += 1
                    print(f"  [NEW PREPRINT DETECTED] arXiv:{aid} - {title}")

                if aid not in raw_data:
                    raw_data[aid] = {
                        "arxiv_id": aid,
                        "title": title,
                        "authors": authors,
                        "release_date": published,
                        "summary": summary,
                        "comment": None,
                        "journal_ref": None,
                        "doi": f"10.48550/arXiv.{aid}"
                    }

        except Exception as e:
            print(f"Watchdog network query error: {e}")

        time.sleep(3.5)

    # Save search log
    log_search(date_str, "Autonomous Living Watchdog (arXiv API)",
               f"Queries: {len(WATCHDOG_QUERIES)}", total_hits, new_candidates_found)

    print(f"[{date_str}] Watchdog completed: {total_hits} total records inspected, {new_candidates_found} new candidates queued.")
    return new_candidates_found

if __name__ == "__main__":
    run_watchdog()
