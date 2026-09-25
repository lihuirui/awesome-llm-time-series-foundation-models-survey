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
    fig, ax = plt.subplots(figsize=(13.5, 7.8), dpi=300)
    ax.axis('off')

    # Color palette
    c_root = '#1f4e78'
    c_p1 = '#2e75b6'
    c_p2 = '#d6604d'
    c_p3 = '#2ca02c'

    # Root Box
    root_box = patches.FancyBboxPatch((0.015, 0.40), 0.165, 0.20, boxstyle="round,pad=0.02", fc=c_root, ec="none")
    ax.add_patch(root_box)
    ax.text(0.0975, 0.50, "Large Models\nfor Time Series\n(LLM & TSFM)", ha='center', va='center', color='white', weight='bold', fontsize=11)

    # 3 Main Branches
    branches = [
        ("Native TSFMs\n(Pretrained ab initio)", 0.80, c_p1, [
            ("Autoregressive & Patch Decoders", "Chronos, TimesFM, Timer,\nSundial, TiRex, Toto, Tabby, $t_0$"),
            ("Masked, PFN & Mixer Models", "MOMENT, MOIRAI, TTM, ICTSP,\nForecastPFN, TabPFN-TS, LightGTS"),
            ("Spatio-Temporal & Dynamical", "OpenCity, UniST, UrbanDiT, UrbanFM,\nTime-MoE, EIDOS, FlowState")
        ]),
        ("Repurposed LLM4TS\n(Cross-Modal & Adapters)", 0.50, c_p2, [
            ("Reprogramming & Prototyping", "Time-LLM, GPT4TS / OFA,\nTEST, CALF, TEMPO, LLM-Mixer"),
            ("Prompting & Spatio-Temporal", "PromptCast, LLMTime, UniTime,\nUrbanGPT, ST-LLM, AutoTimes"),
            ("Multimodal & Agentic Reasoning", "Time-VLM, ChatTS, TimeOmni-VL,\nTRACE, Time-MQA, OpenTSLM")
        ]),
        ("Evaluations, Scaling &\nEmpirical Critiques", 0.20, c_p3, [
            ("Standardized Benchmarks", "GIFT-Eval, fev-bench, TimesX,\nSciTS, TimeSeriesExam, Insight Miner"),
            ("Leakage & Calibration Audits", "It's TIME, Rethinking Evaluation,\nLiveHouse-TS, Probabilistic Reliab."),
            ("Multimodal & Agentic Suites", "Beyond Numerical, AION, TimeVista,\nForecast Workflow, Are LLMs Useful?")
        ])
    ]

    for b_title, b_y, b_col, subcats in branches:
        # Branch box
        b_box = patches.FancyBboxPatch((0.245, b_y - 0.08), 0.23, 0.16, boxstyle="round,pad=0.015", fc=b_col, ec="none")
        ax.add_patch(b_box)
        ax.text(0.36, b_y, b_title, ha='center', va='center', color='white', weight='bold', fontsize=10)

        # Arrow from root to branch
        ax.annotate('', xy=(0.245, b_y), xytext=(0.18, 0.50),
                    arrowprops=dict(arrowstyle="-|>", color='#555555', lw=1.5, mutation_scale=12))

        # Subcategories
        for i, (sc_name, sc_models) in enumerate(subcats):
            sc_y = b_y + (0.075 - i * 0.075)
            # Subcat box
            sc_box = patches.FancyBboxPatch((0.52, sc_y - 0.035), 0.21, 0.07, boxstyle="round,pad=0.01", fc='#e9ecef', ec='#adb5bd', lw=1)
            ax.add_patch(sc_box)
            ax.text(0.625, sc_y, sc_name, ha='center', va='center', color='#212529', weight='bold', fontsize=8.5)

            # Models leaf box
            leaf_box = patches.FancyBboxPatch((0.755, sc_y - 0.035), 0.23, 0.07, boxstyle="round,pad=0.01", fc='#f8f9fa', ec=b_col, lw=1)
            ax.add_patch(leaf_box)
            ax.text(0.87, sc_y, sc_models, ha='center', va='center', color='#333333', fontsize=7.5)

            # Connector from branch to subcat
            ax.annotate('', xy=(0.52, sc_y), xytext=(0.475, b_y),
                        arrowprops=dict(arrowstyle="-", color='#888888', lw=1))
            # Connector from subcat to leaf
            ax.annotate('', xy=(0.755, sc_y), xytext=(0.73, sc_y),
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

    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
    ax.axis('off')

    c_box = '#edf2f7'
    c_edge = '#2b6cb0'

    # Identification
    ax.text(0.04, 0.92, "IDENTIFICATION", fontsize=10.5, weight='bold', color='#2b6cb0', ha='left')
    b1 = patches.FancyBboxPatch((0.14, 0.82), 0.72, 0.085, boxstyle="round,pad=0.01", fc=c_box, ec=c_edge, lw=1.5)
    ax.add_patch(b1)
    ax.text(0.50, 0.862, f"Records identified through scholarly database queries (N = {counts['identification']['total_records_identified']})\n"
                          f"arXiv API: {counts['identification']['records_identified_arxiv']} | Crossref: {counts['identification']['records_identified_crossref']}",
            ha='center', va='center', fontsize=9.5)

    # Duplicates
    ax.annotate('', xy=(0.50, 0.74), xytext=(0.50, 0.82), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#4a5568'))
    b2 = patches.FancyBboxPatch((0.18, 0.66), 0.64, 0.075, boxstyle="round,pad=0.01", fc='#f7fafc', ec='#718096', lw=1.2)
    ax.add_patch(b2)
    ax.text(0.50, 0.697, f"Duplicates removed (N = {counts['identification']['duplicates_removed']})\n"
                          f"Records after deduplication (N = {counts['screening']['screened_title_abstract']})",
            ha='center', va='center', fontsize=9)

    # Screening
    ax.text(0.04, 0.58, "SCREENING", fontsize=10.5, weight='bold', color='#2b6cb0', ha='left')
    ax.annotate('', xy=(0.36, 0.535), xytext=(0.36, 0.66), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#4a5568'))

    b3 = patches.FancyBboxPatch((0.14, 0.44), 0.44, 0.09, boxstyle="round,pad=0.01", fc=c_box, ec=c_edge, lw=1.5)
    ax.add_patch(b3)
    ax.text(0.36, 0.485, f"Records screened by title & abstract\n(N = {counts['screening']['screened_title_abstract']})",
            ha='center', va='center', fontsize=9)

    # Excluded Stage 1 box to the right of screening
    ax.annotate('', xy=(0.60, 0.485), xytext=(0.58, 0.485), arrowprops=dict(arrowstyle="-|>", lw=1.2, color='#c53030'))
    b_exc1 = patches.FancyBboxPatch((0.60, 0.425), 0.35, 0.12, boxstyle="round,pad=0.01", fc='#fff5f5', ec='#e53e3e', lw=1.2)
    ax.add_patch(b_exc1)
    ax.text(0.775, 0.485, f"Excluded at Stage 1 (N = {counts['screening']['excluded_title_abstract']})\n"
                           f"• EC1 (Narrow / non-foundation): 5\n"
                           f"• EC1 (Review / tutorial without artifact): 5",
            ha='center', va='center', fontsize=8, color='#9b2c2c')

    # Eligibility
    ax.text(0.04, 0.35, "ELIGIBILITY", fontsize=10.5, weight='bold', color='#2b6cb0', ha='left')
    ax.annotate('', xy=(0.36, 0.32), xytext=(0.36, 0.44), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#4a5568'))

    b4 = patches.FancyBboxPatch((0.14, 0.225), 0.44, 0.09, boxstyle="round,pad=0.01", fc=c_box, ec=c_edge, lw=1.5)
    ax.add_patch(b4)
    ax.text(0.36, 0.27, f"Full-text records assessed\nfor eligibility (N = {counts['screening']['fulltext_assessed']})",
            ha='center', va='center', fontsize=9)

    # Excluded Stage 2 box to the right of eligibility
    ax.annotate('', xy=(0.60, 0.27), xytext=(0.58, 0.27), arrowprops=dict(arrowstyle="-|>", lw=1.2, color='#c53030'))
    b_exc2 = patches.FancyBboxPatch((0.60, 0.215), 0.35, 0.11, boxstyle="round,pad=0.01", fc='#fff5f5', ec='#e53e3e', lw=1.2)
    ax.add_patch(b_exc2)
    ax.text(0.775, 0.27, f"Excluded at full-text (N = {counts['screening']['excluded_fulltext']})\n"
                          f"• EC4 (Deferred for P4/P5 extraction): {counts['screening']['excluded_fulltext']}",
            ha='center', va='center', fontsize=8, color='#9b2c2c')

    # Included
    ax.text(0.04, 0.14, "INCLUDED", fontsize=10.5, weight='bold', color='#2b6cb0', ha='left')
    ax.annotate('', xy=(0.50, 0.145), xytext=(0.36, 0.225), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#4a5568'))

    b5 = patches.FancyBboxPatch((0.14, 0.02), 0.72, 0.125, boxstyle="round,pad=0.01", fc='#f0fff4', ec='#38a169', lw=1.8)
    ax.add_patch(b5)
    ax.text(0.50, 0.082, f"Studies included in systematic review synthesis (N = {counts['included']['total_included']})\n"
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
    fig, ax = plt.subplots(figsize=(15.2, 6.4), dpi=300)

    # Carefully staggered events: (date_float, y_pos, label, group, color)
    models = [
        (2022.75, 2.0, "PromptCast", "UNSW", "#d62728"),
        (2022.95, 3.5, "PatchTST", "UCB", "#1f77b4"),
        (2023.20, 1.2, "GPT4TS / OFA", "DAMO", "#d62728"),
        (2023.55, 2.3, "TEST", "PKU/Alibaba", "#d62728"),
        (2023.65, 4.3, "LLM4TS", "NYCU", "#d62728"),
        (2023.80, 0.8, "LLMTime", "NYU", "#d62728"),
        (2023.82, 3.2, "Lag-Llama", "Mila/MS", "#1f77b4"),
        (2023.86, 4.5, "TimesFM", "Google", "#1f77b4"),
        (2023.90, 2.5, "Time-LLM", "Ming Jin", "#d62728"),
        (2023.95, 1.7, "ForecastPFN", "Abacus/CMU", "#1f77b4"),
        (2023.98, 2.9, "UniTime", "Beihang/NTU", "#d62728"),
        (2024.05, 4.6, "TTM", "IBM", "#1f77b4"),
        (2024.12, 1.5, "Timer", "THUML", "#1f77b4"),
        (2024.16, 3.3, "Moirai", "Salesforce", "#1f77b4"),
        (2024.14, 4.2, "UniST", "THU FIB", "#1f77b4"),
        (2024.15, 2.0, "UrbanGPT", "HKU/Baidu", "#d62728"),
        (2024.18, 3.8, "MOMENT", "CMU", "#1f77b4"),
        (2024.23, 2.4, "Chronos", "Amazon", "#1f77b4"),
        (2024.26, 0.9, "CALF", "THU/DAMO", "#d62728"),
        (2024.32, 1.4, "ICTSP", "Georgia Tech", "#1f77b4"),
        (2024.40, 2.8, "TimeMixer", "Ming Jin", "#1f77b4"),
        (2024.50, 1.0, "Are LLMs Useful?", "Critique", "#2ca02c"),
        (2024.62, 3.5, "OpenCity", "HKU/Baidu", "#1f77b4"),
        (2024.70, 4.4, "Time-MoE", "Ming Jin", "#1f77b4"),
        (2024.76, 2.3, "LLM-Mixer", "UCF", "#d62728"),
        (2024.80, 3.2, "Timer-XL", "THUML", "#1f77b4"),
        (2024.84, 4.8, "TimeSeriesExam", "CMU", "#2ca02c"),
        (2024.88, 1.1, "GIFT-Eval", "Salesforce", "#2ca02c"),
        (2024.90, 1.9, "UrbanDiT", "THU FIB", "#1f77b4"),
        (2024.95, 2.7, "ChatTS", "THU/NetMan", "#d62728"),
        (2025.10, 4.3, "Sundial", "THUML", "#1f77b4"),
        (2025.15, 2.1, "Time-VLM", "Ming Jin", "#d62728"),
        (2025.38, 1.3, "Toto 1.0", "Datadog", "#1f77b4"),
        (2025.40, 3.2, "TiRex", "JKU Linz", "#1f77b4"),
        (2025.45, 2.3, "LightGTS", "ECNU", "#1f77b4"),
        (2025.70, 3.8, "Chronos-2", "Amazon", "#1f77b4"),
        (2025.75, 4.7, "fev-bench", "AWS", "#2ca02c"),
        (2025.80, 1.2, "SciTS", "Wuhan/Shanghai", "#2ca02c"),
        (2025.90, 2.5, "Moirai 2.0", "Salesforce", "#1f77b4"),
        (2025.95, 4.5, "FLAME", "ZJU/Westlake", "#1f77b4"),
        (2026.12, 1.5, "EIDOS", "Ming Jin", "#1f77b4"),
        (2026.15, 3.9, "UrbanFM", "HKUST/THU", "#1f77b4"),
        (2026.16, 2.7, "TimeOmni-VL", "Monash", "#d62728"),
        (2026.25, 4.2, "Timer-S1", "THUML", "#1f77b4"),
        (2026.40, 2.9, "AION", "Ming Jin", "#2ca02c"),
        (2026.42, 3.3, "Toto 2.0", "Datadog", "#1f77b4"),
        (2026.45, 2.2, "TimeVista", "THUML", "#2ca02c"),
        (2026.50, 4.6, "TimesX", "Google/GT", "#2ca02c"),
        (2026.58, 1.0, "LiveHouse-TS", "HKUST", "#2ca02c"),
        (2026.70, 1.8, "$t_0$", "ETH Zurich", "#1f77b4"),
        (2026.72, 3.5, "Tabby", "Huawei", "#1f77b4"),
        (2026.75, 2.6, "TAC-Time", "ECNU", "#d62728"),
        (2026.78, 4.4, "WorkflowBench", "Tokyo", "#2ca02c")
    ]

    # Draw timeline line
    ax.axhline(0, color='#444444', lw=2, zorder=1)
    ax.set_xlim(2022.4, 2026.95)
    ax.set_ylim(-0.8, 5.2)

    # Years markers
    for yr in range(2023, 2027):
        ax.axvline(yr, color='#e0e0e0', linestyle='--', lw=0.8, zorder=0)
        ax.text(yr, -0.4, str(yr), ha='center', va='center', weight='bold', fontsize=11, color='#333333')

    for x, y, label, grp, col in models:
        ax.plot([x, x], [0, y], color=col, alpha=0.6, lw=1.2, zorder=2)
        ax.scatter(x, y, s=75, color=col, edgecolors='white', lw=1.5, zorder=3)
        ax.text(x, y + 0.16, f"{label}\n({grp})", ha='center', va='bottom', fontsize=6.8, weight='bold', color='#222222')

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
        ("ForecastPFN", 2023.90, 1.0e7, "Native TSFM", "#1f77b4", (8, 0)),
        ("Lag-Llama", 2023.85, 2.4e6, "Native TSFM", "#1f77b4", (8, 0)),
        ("LightGTS", 2025.45, 5.8e6, "Native TSFM", "#1f77b4", (8, -8)),
        ("TTM", 2024.05, 8.0e6, "Native TSFM", "#1f77b4", (8, -8)),
        ("ForecastPFN", 2023.90, 1.0e7, "Native TSFM", "#1f77b4", (8, 0)),
        ("OpenCity", 2024.62, 2.6e7, "Native TSFM", "#1f77b4", (8, -8)),
        ("ICTSP", 2024.35, 4.2e7, "Native TSFM", "#1f77b4", (8, 0)),
        ("FLAME", 2025.95, 4.5e7, "Native TSFM", "#1f77b4", (8, 0)),
        ("UrbanDiT", 2024.90, 4.5e7, "Native TSFM", "#1f77b4", (8, 6)),
        ("Timer", 2024.15, 8.4e7, "Native TSFM", "#1f77b4", (8, -8)),
        ("VisionTS", 2024.65, 8.6e7, "LLM4TS / VLM", "#d62728", (8, -9)),
        ("Timer-XL", 2024.80, 8.4e7, "Native TSFM", "#1f77b4", (-14, 8)),
        ("EIDOS", 2026.12, 8.8e7, "Native TSFM", "#1f77b4", (8, 0)),
        ("UrbanFM", 2026.15, 1.2e8, "Native TSFM", "#1f77b4", (8, -8)),
        ("Tabby", 2026.70, 1.2e8, "Native TSFM", "#1f77b4", (-12, 7)),
        ("LLM4TS", 2023.65, 1.24e8, "LLM4TS", "#d62728", (8, 0)),
        ("TiRex", 2025.40, 1.5e8, "Native TSFM", "#1f77b4", (8, 6)),
        ("Toto 1.0", 2025.38, 1.51e8, "Native TSFM", "#1f77b4", (-14, -12)),
        ("TimesFM", 2023.85, 2.0e8, "Native TSFM", "#1f77b4", (8, 0)),
        ("PromptCast", 2022.85, 2.2e8, "LLM4TS", "#d62728", (8, 0)),
        ("Moirai", 2024.15, 3.11e8, "Native TSFM", "#1f77b4", (8, -8)),
        ("TAC-Time", 2026.72, 3.5e8, "LLM4TS", "#d62728", (8, 6)),
        ("$t_0$", 2026.70, 3.5e8, "Native TSFM", "#1f77b4", (-12, -12)),
        ("MOMENT", 2024.15, 3.85e8, "Native TSFM", "#1f77b4", (8, 8)),
        ("Chronos", 2024.20, 7.1e8, "Native TSFM", "#1f77b4", (-10, 8)),
        ("Moirai-MoE", 2024.80, 1.1e9, "Native TSFM", "#1f77b4", (8, 0)),
        ("Toto 2.0", 2026.35, 1.2e9, "Native TSFM", "#1f77b4", (8, 0)),
        ("Sundial", 2025.10, 1.5e9, "Native TSFM", "#1f77b4", (8, 0)),
        ("Time-MoE", 2024.70, 2.4e9, "Native TSFM", "#1f77b4", (8, 0)),
        ("UrbanGPT", 2024.15, 7.0e9, "LLM4TS", "#d62728", (8, 6)),
        ("Time-LLM", 2023.80, 7.0e9, "LLM4TS", "#d62728", (-12, 7)),
        ("AutoTimes", 2024.15, 7.0e9, "LLM4TS", "#d62728", (8, -9)),
        ("Time-VLM", 2025.10, 7.0e9, "LLM4TS", "#d62728", (8, -9)),
        ("ChatTS", 2024.95, 8.0e9, "LLM4TS", "#d62728", (-12, 8)),
        ("TimeOmni-1", 2025.75, 8.0e9, "LLM4TS", "#d62728", (-14, 8)),
        ("TimeOmni-VL", 2026.15, 9.0e9, "LLM4TS", "#d62728", (8, 7)),
        ("Timer-S1", 2026.20, 8.3e9, "Native TSFM", "#1f77b4", (8, -10)),
    ]

    for name, date, p_cnt, cat, col, offset in param_data:
        ax1.scatter(date, p_cnt, s=70, color=col, edgecolors='black', lw=0.6, zorder=3)
        ax1.annotate(name, (date, p_cnt), textcoords="offset points", xytext=offset, fontsize=7, weight='bold')

    ax1.set_yscale('log')
    ax1.set_xlabel("Release Date", weight='bold', labelpad=8)
    ax1.set_ylabel("Reported Parameters (Log Scale)", weight='bold', labelpad=8)
    ax1.set_title("(a) Model Parameter Count vs. Release Date", fontsize=11, weight='bold', color='#1f4e78')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.set_xlim(2022.6, 2026.95)

    # Panel B: Stated Pretraining Corpus Size (Points / Observations)
    corpus_data = [
        ("UTSD (Timer)", 2024.15, 1e9, "#1f77b4", (-12, 7)),
        ("Time-series Pile (MOMENT)", 2024.15, 1e9, "#1f77b4", (8, -9)),
        ("UTSD-3 (Sundial)", 2025.10, 1e10, "#1f77b4", (8, -3)),
        ("LOTSA (Moirai)", 2024.15, 2.7e10, "#1f77b4", (8, -3)),
        ("TiRex Corpus", 2025.40, 5e10, "#1f77b4", (8, -3)),
        ("TSMix (Chronos)", 2024.20, 8.4e10, "#1f77b4", (8, -3)),
        ("TimesFM Corpus", 2023.85, 1e11, "#1f77b4", (8, -3)),
        ("$t_0$ Corpus", 2026.70, 1.2e11, "#1f77b4", (8, -12)),
        ("Tabby Open Corpus", 2026.70, 1.5e11, "#1f77b4", (8, 6)),
        ("Time-300B (Time-MoE)", 2024.70, 3e11, "#1f77b4", (8, -3)),
        ("Toto Telemetry (Toto 1.0)", 2025.38, 1e12, "#1f77b4", (-12, 7)),
        ("Datadog Telemetry (Toto 2.0)", 2026.35, 1.5e12, "#1f77b4", (8, -3))
    ]

    for name, date, c_size, col, offset in corpus_data:
        ax2.scatter(date, c_size, s=80, color=col, edgecolors='black', lw=0.6, zorder=3)
        ax2.annotate(name, (date, c_size), textcoords="offset points", xytext=offset, fontsize=7.5, weight='bold')

    ax2.set_yscale('log')
    ax2.set_xlabel("Release Date", weight='bold', labelpad=8)
    ax2.set_ylabel("Pretraining Corpus Size (Data Points, Log Scale)", weight='bold', labelpad=8)
    ax2.set_title("(b) Stated Pretraining Corpus Size vs. Release Date", fontsize=11, weight='bold', color='#1f4e78')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.set_xlim(2023.5, 2026.95)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fig_params_corpus.png"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "fig_params_corpus.pdf"))
    plt.close()
    print("✓ fig_params_corpus generated")

def generate_category_dist_figure():
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    papers = data.get("papers", [])

    # Dynamic year and paradigm counts
    years = ['2022', '2023', '2024', '2025', '2026']
    p_native = np.zeros(len(years))
    p_llm = np.zeros(len(years))
    p_eval = np.zeros(len(years))
    p_survey = np.zeros(len(years))

    venue_counts = {}
    for p in papers:
        yr = p.get('release_date', '2024')[:4]
        if yr in years:
            idx = years.index(yr)
            paradigm = p.get('paradigm', '')
            if paradigm == 'Native TSFM':
                p_native[idx] += 1
            elif paradigm == 'LLM4TS':
                p_llm[idx] += 1
            elif paradigm == 'Evaluation & Benchmark':
                p_eval[idx] += 1
            elif paradigm == 'Survey & Foundations':
                p_survey[idx] += 1

        v = p.get('venue') or 'arXiv Preprint'
        v_clean = 'arXiv Preprint'
        for vname in ['NeurIPS', 'ICML', 'ICLR', 'KDD', 'WWW', 'ACL', 'TKDE', 'TMLR', 'ACM Computing Surveys']:
            if vname.lower() in v.lower():
                v_clean = vname
                break
        venue_counts[v_clean] = venue_counts.get(v_clean, 0) + 1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.2), dpi=300)

    # Panel A: Stacked bar chart
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

    # Panel B: Venue Distribution sorted descending
    sorted_venues = sorted(venue_counts.items(), key=lambda x: x[1])
    v_names = [x[0] for x in sorted_venues]
    v_vals = [x[1] for x in sorted_venues]

    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(v_names)))
    ax2.barh(v_names, v_vals, color=colors, edgecolor='#333333', lw=0.6)
    for i, v in enumerate(v_vals):
        ax2.text(v + 0.3, i, str(v), va='center', weight='bold', fontsize=9)

    ax2.set_xlabel("Number of Included Studies", weight='bold')
    ax2.set_title("(b) Distribution Across Premier Venues", weight='bold', fontsize=11, color='#1f4e78')
    ax2.grid(axis='x', linestyle=':', alpha=0.6)
    ax2.set_xlim(0, max(v_vals) + 3)

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
