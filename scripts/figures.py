#!/usr/bin/env python3
"""figures.py: Generate publication-quality survey figures.

Outputs both PNG (>= 200 dpi) and PDF vector formats:
1. paper/figures/fig_taxonomy.{png,pdf}
2. paper/figures/fig_prisma.{png,pdf}
3. paper/figures/fig_timeline.{png,pdf}
4. paper/figures/fig_params_corpus.{png,pdf}
5. paper/figures/fig_category_dist.{png,pdf}
"""

import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "paper", "figures")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PRISMA_FILE = os.path.join(DATA_DIR, "prisma_counts.json")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")

os.makedirs(FIGURES_DIR, exist_ok=True)

# Styling defaults
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

def generate_taxonomy_figure():
    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
    ax.axis('off')

    # Color palette
    c_root = '#1f4e78'
    c_p1 = '#2e75b6'
    c_p2 = '#d6604d'
    c_p3 = '#2ca02c'
    c_leaf = '#f2f2f2'

    # Root Box
    root_box = patches.FancyBboxPatch((0.02, 0.40), 0.16, 0.20, boxstyle="round,pad=0.02", fc=c_root, ec="none")
    ax.add_patch(root_box)
    ax.text(0.10, 0.50, "Large Models\nfor Time Series\n(LLM & TSFM)", ha='center', va='center', color='white', weight='bold', fontsize=11)

    # 3 Main Branches
    branches = [
        ("Native TSFMs\n(Pretrained ab initio)", 0.80, c_p1, [
            ("Autoregressive Decoder-only", "Chronos, TimesFM, Timer,\nSundial, Lag-Llama, Toto"),
            ("Masked Encoder & Enc-Dec", "MOMENT, MOIRAI, TTM,\nPatchTST, TimeMixer++"),
            ("Mixture-of-Experts (MoE)", "Time-MoE, Moirai-MoE,\nTimer-S1")
        ]),
        ("Repurposed LLM4TS\n(Cross-Modal & Adapters)", 0.50, c_p2, [
            ("Cross-Modal Reprogramming", "Time-LLM, GPT4TS / OFA,\nTEMPO, TEST"),
            ("Direct Prompting & Binning", "LLMTime, PromptCast,\nLSTPrompt"),
            ("Multimodal & Agentic Reasoning", "Time-MQA, TimeOmni-1,\nChatTime, OpenTSLM")
        ]),
        ("Evaluations, Scaling &\nEmpirical Critiques", 0.20, c_p3, [
            ("Standardized Benchmarks", "GIFT-Eval, fev-bench,\nTime-MMD"),
            ("Leakage & Calibration Audits", "Rethinking Evaluation,\nProbabilistic Reliability"),
            ("Foundational Critiques", "Are LLMs Useful for TS?,\nObservability Perspectives")
        ])
    ]

    for b_title, b_y, b_col, subcats in branches:
        # Branch box
        b_box = patches.FancyBboxPatch((0.26, b_y - 0.08), 0.22, 0.16, boxstyle="round,pad=0.015", fc=b_col, ec="none")
        ax.add_patch(b_box)
        ax.text(0.37, b_y, b_title, ha='center', va='center', color='white', weight='bold', fontsize=10)

        # Arrow from root to branch
        ax.annotate('', xy=(0.26, b_y), xytext=(0.18, 0.50),
                    arrowprops=dict(arrowstyle="-|>", color='#555555', lw=1.5, mutation_scale=12))

        # Subcategories
        n_sub = len(subcats)
        for i, (sc_name, sc_models) in enumerate(subcats):
            sc_y = b_y + (0.075 - i * 0.075)
            # Subcat box
            sc_box = patches.FancyBboxPatch((0.54, sc_y - 0.035), 0.20, 0.07, boxstyle="round,pad=0.01", fc='#e9ecef', ec='#adb5bd', lw=1)
            ax.add_patch(sc_box)
            ax.text(0.64, sc_y, sc_name, ha='center', va='center', color='#212529', weight='bold', fontsize=8.5)

            # Models leaf box
            leaf_box = patches.FancyBboxPatch((0.77, sc_y - 0.035), 0.21, 0.07, boxstyle="round,pad=0.01", fc='#f8f9fa', ec=b_col, lw=1)
            ax.add_patch(leaf_box)
            ax.text(0.875, sc_y, sc_models, ha='center', va='center', color='#333333', fontsize=7.5)

            # Connector from branch to subcat
            ax.annotate('', xy=(0.54, sc_y), xytext=(0.48, b_y),
                        arrowprops=dict(arrowstyle="-", color='#888888', lw=1))
            # Connector from subcat to leaf
            ax.annotate('', xy=(0.77, sc_y), xytext=(0.74, sc_y),
                        arrowprops=dict(arrowstyle="-", color='#aaaaaa', lw=1))

    ax.set_title("Taxonomy of Foundation Models and Large Language Models for Time Series", fontsize=14, weight='bold', pad=15, color='#1f4e78')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_taxonomy.png"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "fig_taxonomy.pdf"))
    plt.close()
    print("✓ fig_taxonomy generated")

def generate_prisma_figure():
    with open(PRISMA_FILE, "r", encoding="utf-8") as f:
        counts = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.axis('off')

    c_box = '#edf2f7'
    c_edge = '#2b6cb0'

    # Identification
    ax.text(0.08, 0.90, "IDENTIFICATION", fontsize=11, weight='bold', color='#2b6cb0', ha='left')
    b1 = patches.FancyBboxPatch((0.15, 0.80), 0.70, 0.09, boxstyle="round,pad=0.01", fc=c_box, ec=c_edge, lw=1.5)
    ax.add_patch(b1)
    ax.text(0.50, 0.845, f"Records identified through database queries (N = {counts['identification']['total_records_identified']})\n"
                          f"arXiv API: {counts['identification']['records_identified_arxiv']} | Crossref: {counts['identification']['records_identified_crossref']}",
            ha='center', va='center', fontsize=9.5)

    # Duplicates
    ax.annotate('', xy=(0.50, 0.72), xytext=(0.50, 0.80), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#4a5568'))
    b2 = patches.FancyBboxPatch((0.20, 0.65), 0.60, 0.07, boxstyle="round,pad=0.01", fc='#f7fafc', ec='#718096', lw=1.2)
    ax.add_patch(b2)
    ax.text(0.50, 0.685, f"Duplicates removed (N = {counts['identification']['duplicates_removed']})\n"
                          f"Records after deduplication (N = {counts['screening']['screened_title_abstract']})",
            ha='center', va='center', fontsize=9)

    # Screening
    ax.text(0.08, 0.60, "SCREENING", fontsize=11, weight='bold', color='#2b6cb0', ha='left')
    ax.annotate('', xy=(0.50, 0.54), xytext=(0.50, 0.65), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#4a5568'))

    b3 = patches.FancyBboxPatch((0.20, 0.47), 0.60, 0.07, boxstyle="round,pad=0.01", fc=c_box, ec=c_edge, lw=1.5)
    ax.add_patch(b3)
    ax.text(0.50, 0.505, f"Records screened by title & abstract (N = {counts['screening']['screened_title_abstract']})\n"
                          f"Records excluded at Stage 1 (N = {counts['screening']['excluded_title_abstract']})",
            ha='center', va='center', fontsize=9)

    # Eligibility
    ax.text(0.08, 0.42, "ELIGIBILITY", fontsize=11, weight='bold', color='#2b6cb0', ha='left')
    ax.annotate('', xy=(0.50, 0.36), xytext=(0.50, 0.47), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#4a5568'))

    b4 = patches.FancyBboxPatch((0.15, 0.28), 0.42, 0.08, boxstyle="round,pad=0.01", fc=c_box, ec=c_edge, lw=1.5)
    ax.add_patch(b4)
    ax.text(0.36, 0.32, f"Full-text records assessed\nfor eligibility (N = {counts['screening']['fulltext_assessed']})",
            ha='center', va='center', fontsize=9)

    # Excluded / Deferred box to the right
    ax.annotate('', xy=(0.60, 0.32), xytext=(0.57, 0.32), arrowprops=dict(arrowstyle="-|>", lw=1.2, color='#c53030'))
    b_exc = patches.FancyBboxPatch((0.60, 0.26), 0.33, 0.12, boxstyle="round,pad=0.01", fc='#fff5f5', ec='#e53e3e', lw=1.2)
    ax.add_patch(b_exc)
    ax.text(0.765, 0.32, f"Excluded / Deferred (N = {counts['screening']['excluded_fulltext']})\n"
                          f"• Pre-2021 date: {counts['screening']['excluded_title_abstract']}\n"
                          f"• Deferred for P2 extraction: {counts['screening']['excluded_fulltext']}",
            ha='center', va='center', fontsize=8, color='#9b2c2c')

    # Included
    ax.text(0.08, 0.20, "INCLUDED", fontsize=11, weight='bold', color='#2b6cb0', ha='left')
    ax.annotate('', xy=(0.36, 0.18), xytext=(0.36, 0.28), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#4a5568'))

    b5 = patches.FancyBboxPatch((0.15, 0.05), 0.70, 0.13, boxstyle="round,pad=0.01", fc='#f0fff4', ec='#38a169', lw=1.8)
    ax.add_patch(b5)
    ax.text(0.50, 0.115, f"Studies included in systematic review synthesis (N = {counts['included']['total_included']})\n"
                          f"• Native Time Series Foundation Models: {counts['included']['by_paradigm'].get('Native TSFM', 0)}\n"
                          f"• Repurposed Large Language Models (LLM4TS): {counts['included']['by_paradigm'].get('LLM4TS', 0)}\n"
                          f"• Evaluations, Benchmarks & Audits: {counts['included']['by_paradigm'].get('Evaluation & Benchmark', 0)}\n"
                          f"• Surveys & Foundations: {counts['included']['by_paradigm'].get('Survey & Foundations', 0)}",
            ha='center', va='center', fontsize=9, color='#22543d')

    ax.set_title("PRISMA 2020 Systematic Review Flow Diagram", fontsize=13, weight='bold', pad=12, color='#2b6cb0')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_prisma.png"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "fig_prisma.pdf"))
    plt.close()
    print("✓ fig_prisma generated")

def generate_timeline_figure():
    fig, ax = plt.subplots(figsize=(13, 6), dpi=300)

    # Timeline events: (date_float, y_pos, label, group, color)
    models = [
        (2022.9, 3, "PatchTST", "THUML/UCB", "#1f77b4"),
        (2023.2, 1, "GPT4TS / OFA", "DAMO", "#d62728"),
        (2023.8, 2, "LLM4TS", "Ming Jin", "#d62728"),
        (2023.8, 1, "LLMTime", "NYU", "#d62728"),
        (2023.8, 3, "Lag-Llama", "Mila/MS", "#1f77b4"),
        (2023.8, 4, "TimesFM", "Google", "#1f77b4"),
        (2023.8, 2, "Time-LLM", "Ming Jin", "#d62728"),
        (2024.1, 4, "TTM", "IBM", "#1f77b4"),
        (2024.1, 3, "Moirai", "Salesforce", "#1f77b4"),
        (2024.1, 2, "Timer", "THUML", "#1f77b4"),
        (2024.1, 4, "MOMENT", "CMU", "#1f77b4"),
        (2024.2, 3, "Chronos", "Amazon", "#1f77b4"),
        (2024.4, 2, "TimeMixer", "Ming Jin", "#1f77b4"),
        (2024.5, 1, "Are LLMs Useful?", "Critique", "#2ca02c"),
        (2024.7, 4, "Time-MoE", "Ming Jin", "#1f77b4"),
        (2024.8, 3, "Timer-XL", "THUML", "#1f77b4"),
        (2024.8, 1, "GIFT-Eval", "Salesforce", "#2ca02c"),
        (2025.1, 4, "Sundial", "THUML", "#1f77b4"),
        (2025.7, 3, "Chronos-2", "Amazon", "#1f77b4"),
        (2025.9, 2, "Moirai 2.0", "Salesforce", "#1f77b4"),
        (2026.2, 4, "Timer-S1", "THUML", "#1f77b4"),
        (2026.4, 3, "Toto 2.0", "Datadog", "#1f77b4")
    ]

    # Draw timeline line
    ax.axhline(0, color='#444444', lw=2, zorder=1)
    ax.set_xlim(2022.5, 2026.7)
    ax.set_ylim(-0.8, 4.8)

    # Years markers
    for yr in range(2023, 2027):
        ax.axvline(yr, color='#e0e0e0', linestyle='--', lw=0.8, zorder=0)
        ax.text(yr, -0.4, str(yr), ha='center', va='center', weight='bold', fontsize=11, color='#333333')

    for x, y, label, grp, col in models:
        ax.plot([x, x], [0, y], color=col, alpha=0.6, lw=1.2, zorder=2)
        ax.scatter(x, y, s=80, color=col, edgecolors='white', lw=1.5, zorder=3)
        ax.text(x, y + 0.18, f"{label}\n({grp})", ha='center', va='bottom', fontsize=7.5, weight='bold', color='#222222')

    ax.scatter(0, 0, color='#1f77b4', label='Native TSFM', s=60)
    ax.scatter(0, 0, color='#d62728', label='Repurposed LLM4TS', s=60)
    ax.scatter(0, 0, color='#2ca02c', label='Benchmark / Critique', s=60)
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)

    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.set_title("Genealogy and Chronological Timeline of Time Series Foundation Models and LLM Methods (2022–2026)",
                 fontsize=13, weight='bold', pad=15, color='#1f4e78')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_timeline.png"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "fig_timeline.pdf"))
    plt.close()
    print("✓ fig_timeline generated")

def generate_params_corpus_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Panel A: Parameter counts (only stated in papers)
    param_data = [
        ("TTM", 2024.05, 8e6, "Native TSFM", "#1f77b4"),
        ("Lag-Llama", 2023.85, 2.4e6, "Native TSFM", "#1f77b4"),
        ("Timer", 2024.15, 8.4e7, "Native TSFM", "#1f77b4"),
        ("Timer-XL", 2024.80, 8.4e7, "Native TSFM", "#1f77b4"),
        ("VisionTS", 2024.65, 8.6e7, "LLM4TS / VLM", "#d62728"),
        ("TimesFM", 2023.85, 2.0e8, "Native TSFM", "#1f77b4"),
        ("Moirai", 2024.15, 3.11e8, "Native TSFM", "#1f77b4"),
        ("MOMENT", 2024.15, 3.85e8, "Native TSFM", "#1f77b4"),
        ("Chronos", 2024.20, 7.1e8, "Native TSFM", "#1f77b4"),
        ("Moirai-MoE", 2024.80, 1.1e9, "Native TSFM", "#1f77b4"),
        ("Toto 2.0", 2026.35, 1.2e9, "Native TSFM", "#1f77b4"),
        ("Sundial", 2025.10, 1.5e9, "Native TSFM", "#1f77b4"),
        ("Time-MoE", 2024.70, 2.4e9, "Native TSFM", "#1f77b4"),
        ("Time-LLM", 2023.80, 7.0e9, "LLM4TS", "#d62728"),
        ("AutoTimes", 2024.15, 7.0e9, "LLM4TS", "#d62728"),
        ("TimeOmni-1", 2025.75, 8.0e9, "LLM4TS", "#d62728"),
        ("Timer-S1", 2026.20, 8.3e9, "Native TSFM", "#1f77b4"),
    ]

    for name, date, p_cnt, cat, col in param_data:
        ax1.scatter(date, p_cnt, s=70, color=col, edgecolors='black', lw=0.6, zorder=3)
        offset = (8, 0)
        if name in ["Timer-XL", "Chronos", "AutoTimes"]:
            offset = (-10, 8)
        elif name in ["Timer", "Moirai"]:
            offset = (8, -8)
        ax1.annotate(name, (date, p_cnt), textcoords="offset points", xytext=offset, fontsize=7.5, weight='bold')

    ax1.set_yscale('log')
    ax1.set_xlabel("Release Date", weight='bold', labelpad=8)
    ax1.set_ylabel("Reported Parameters (Log Scale)", weight='bold', labelpad=8)
    ax1.set_title("(a) Model Parameter Count vs. Release Date", fontsize=11, weight='bold', color='#1f4e78')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.set_xlim(2023.5, 2026.6)

    # Panel B: Stated Pretraining Corpus Size (Points / Observations)
    corpus_data = [
        ("UTSD (Timer)", 2024.15, 1e9, "#1f77b4"),
        ("Time-series Pile (MOMENT)", 2024.15, 1e9, "#1f77b4"),
        ("UTSD-3 (Sundial)", 2025.10, 1e10, "#1f77b4"),
        ("LOTSA (Moirai)", 2024.15, 2.7e10, "#1f77b4"),
        ("TSMix (Chronos)", 2024.20, 8.4e10, "#1f77b4"),
        ("TimesFM Corpus", 2023.85, 1e11, "#1f77b4"),
        ("Time-300B (Time-MoE)", 2024.70, 3e11, "#1f77b4"),
        ("Datadog Telemetry (Toto 2.0)", 2026.35, 1.5e12, "#1f77b4")
    ]

    for name, date, c_size, col in corpus_data:
        ax2.scatter(date, c_size, s=80, color=col, edgecolors='black', lw=0.6, zorder=3)
        ax2.annotate(name, (date, c_size), textcoords="offset points", xytext=(8, -3), fontsize=7.5, weight='bold')

    ax2.set_yscale('log')
    ax2.set_xlabel("Release Date", weight='bold', labelpad=8)
    ax2.set_ylabel("Pretraining Corpus Size (Data Points, Log Scale)", weight='bold', labelpad=8)
    ax2.set_title("(b) Stated Pretraining Corpus Size vs. Release Date", fontsize=11, weight='bold', color='#1f4e78')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.set_xlim(2023.5, 2026.6)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_params_corpus.png"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "fig_params_corpus.pdf"))
    plt.close()
    print("✓ fig_params_corpus generated")

def generate_category_dist_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # Panel A: Papers per year by paradigm
    years = ['2022', '2023', '2024', '2025', '2026']
    p_native = np.array([1, 4, 11, 5, 3])
    p_llm = np.array([1, 4, 4, 3, 0])
    p_eval = np.array([0, 0, 2, 1, 1])
    p_survey = np.array([0, 1, 0, 0, 0])

    width = 0.55
    ax1.bar(years, p_native, width, label='Native TSFM', color='#1f77b4')
    ax1.bar(years, p_llm, width, bottom=p_native, label='Repurposed LLM4TS', color='#d62728')
    ax1.bar(years, p_eval, width, bottom=p_native + p_llm, label='Benchmark / Critique', color='#2ca02c')
    ax1.bar(years, p_survey, width, bottom=p_native + p_llm + p_eval, label='Survey', color='#9467bd')

    ax1.set_ylabel("Number of Core Included Studies", weight='bold')
    ax1.set_xlabel("Publication / Release Year", weight='bold')
    ax1.set_title("(a) Publications per Year by Model Paradigm", weight='bold', fontsize=11, color='#1f4e78')
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(axis='y', linestyle=':', alpha=0.6)

    # Panel B: Venue Distribution
    venues = ['NeurIPS', 'ICML', 'ICLR', 'ACL / TMLR', 'TKDE / TIST', 'arXiv Preprint']
    counts = [10, 8, 5, 2, 2, 14]
    colors = ['#2b5c8f', '#3b78b0', '#5694c9', '#78b0e0', '#a3cbed', '#c7dcf0']

    ax2.barh(venues, counts, color=colors, edgecolor='#333333', lw=0.6)
    for i, v in enumerate(counts):
        ax2.text(v + 0.3, i, str(v), va='center', weight='bold', fontsize=9)

    ax2.set_xlabel("Number of Included Studies", weight='bold')
    ax2.set_title("(b) Distribution Across Peer-Reviewed Venues", weight='bold', fontsize=11, color='#1f4e78')
    ax2.grid(axis='x', linestyle=':', alpha=0.6)
    ax2.set_xlim(0, 16)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_category_dist.png"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "fig_category_dist.pdf"))
    plt.close()
    print("✓ fig_category_dist generated")

if __name__ == "__main__":
    generate_taxonomy_figure()
    generate_prisma_figure()
    generate_timeline_figure()
    generate_params_corpus_figure()
    generate_category_dist_figure()
