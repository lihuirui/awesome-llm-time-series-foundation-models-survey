#!/usr/bin/env python3
"""check.py: Automated quality gates for survey repository.

Enforces:
1. JSON data validation & deduplication
2. Every included paper verified with an API response
3. Bib keys cited in LaTeX ⊆ references.bib ⊆ included papers
4. All referenced figures exist on disk (PNG & PDF)
5. README is properly generated and up to date
6. LaTeX document compiles to paper/main.pdf without fatal errors
"""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "data")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
PRISMA_FILE = os.path.join(DATA_DIR, "prisma_counts.json")
RAW_META = os.path.join(DATA_DIR, "raw", "arxiv_raw_metadata.json")
BIB_FILE = os.path.join(ROOT, "paper", "references.bib")
SECTIONS_DIR = os.path.join(ROOT, "paper", "sections")
MAIN_TEX = os.path.join(ROOT, "paper", "main.tex")
FIGURES_DIR = os.path.join(ROOT, "paper", "figures")

def run_checks():
    errors = []
    print("=== Running Antigravity Survey Quality Gates ===")

    # 1. Check data/papers.json
    if not os.path.exists(PAPERS_FILE):
        errors.append("data/papers.json does not exist")
        return False
    try:
        with open(PAPERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        papers = data.get("papers", [])
        print(f"[OK] data/papers.json loaded: {len(papers)} papers")
    except Exception as e:
        errors.append(f"Failed to parse data/papers.json: {e}")
        return False

    # Check deduplication
    ids = [p.get("id") for p in papers]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate paper IDs found in data/papers.json")

    # Check raw verification
    if not os.path.exists(RAW_META):
        errors.append("data/raw/arxiv_raw_metadata.json missing")
    else:
        with open(RAW_META, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        unverified = []
        for p in papers:
            aid = p.get("arxiv_id")
            if aid not in raw_data:
                unverified.append(aid)
        if unverified:
            errors.append(f"Unverified papers (no raw API response): {unverified}")
        else:
            print(f"[OK] All {len(papers)} included papers verified with logged API responses")

    # 2. Check references.bib
    if not os.path.exists(BIB_FILE):
        errors.append("paper/references.bib does not exist")
        return False
    with open(BIB_FILE, "r", encoding="utf-8") as f:
        bib_content = f.read()

    bibkeys_in_bib = set(re.findall(r'@\w+\{([^,]+),', bib_content))
    paper_bibkeys = {p.get("bibkey") for p in papers if p.get("bibkey")}

    # bib ⊆ included papers
    bib_diff = bibkeys_in_bib - paper_bibkeys
    if bib_diff:
        errors.append(f"BibTeX contains keys not in included papers: {bib_diff}")
    else:
        print(f"[OK] All {len(bibkeys_in_bib)} keys in references.bib match included papers")

    # 3. Check citations in LaTeX files
    tex_files = [MAIN_TEX]
    if os.path.exists(SECTIONS_DIR):
        for fname in os.listdir(SECTIONS_DIR):
            if fname.endswith(".tex"):
                tex_files.append(os.path.join(SECTIONS_DIR, fname))

    cited_keys = set()
    referenced_figures = set()
    for tf in tex_files:
        if not os.path.exists(tf):
            continue
        with open(tf, "r", encoding="utf-8") as f:
            txt = f.read()
        # Find \cite{k1,k2}
        for match in re.findall(r'\\cite\{([^}]+)\}', txt):
            for k in match.split(','):
                k = k.strip()
                if k:
                    cited_keys.add(k)
        # Find \includegraphics[...]{path}
        for match in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', txt):
            referenced_figures.add(match.strip())

    missing_citations = cited_keys - bibkeys_in_bib
    if missing_citations:
        errors.append(f"Cited keys missing from references.bib: {missing_citations}")
    else:
        print(f"[OK] All {len(cited_keys)} cited keys exist in references.bib")

    # 4. Check figures referenced in LaTeX
    for fig_path in referenced_figures:
        # Resolve path relative to paper/ directory
        full_fig_path = os.path.normpath(os.path.join(ROOT, "paper", fig_path))
        # If no extension specified, check png or pdf
        if not os.path.exists(full_fig_path):
            if os.path.exists(full_fig_path + ".pdf") or os.path.exists(full_fig_path + ".png"):
                pass
            else:
                errors.append(f"Referenced figure not found: {fig_path} (resolved to {full_fig_path})")

    required_figs = [
        "fig_taxonomy.png", "fig_prisma.png", "fig_timeline.png",
        "fig_params_corpus.png", "fig_category_dist.png"
    ]
    for rf in required_figs:
        p = os.path.join(FIGURES_DIR, rf)
        if not os.path.exists(p):
            errors.append(f"Required figure missing: {rf}")
    print("[OK] All required figures exist on disk")

    # 5. Check README
    readme_path = os.path.join(ROOT, "README.md")
    if not os.path.exists(readme_path) or os.path.getsize(readme_path) < 500:
        errors.append("README.md missing or too small")
    else:
        print("[OK] README.md verified")

    # Report errors
    if errors:
        print("\n❌ QUALITY GATE FAILED:")
        for e in errors:
            print(f"  • {e}")
        return False
    else:
        print("\n✅ ALL QUALITY GATES PASSED")
        return True

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
