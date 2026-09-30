#!/usr/bin/env python3
"""readme_gen.py: Generate bilingual awesome-style README.md from data/papers.json.

Includes:
- English + 中文简介 project overview
- Taxonomy tree diagram & PRISMA flow chart
- Direct link to compiled PDF
- Structured tables/lists grouped by taxonomy
- Verified paper links and confirmed GitHub code repositories
- Maintenance protocol & automated quality gates
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
PRISMA_FILE = os.path.join(DATA_DIR, "prisma_counts.json")
README_FILE = os.path.join(os.path.dirname(__file__), "..", "README.md")

def generate_readme():
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(PRISMA_FILE, "r", encoding="utf-8") as f:
        prisma = json.load(f)

    papers = data.get("papers", [])
    today = data.get("updated", "2026-09-24")

    # Group papers by paradigm
    by_paradigm = {
        "Native TSFM": [],
        "LLM4TS": [],
        "Evaluation & Benchmark": [],
        "Survey & Foundations": []
    }
    for p in papers:
        par = p.get("paradigm", "Other")
        if par in by_paradigm:
            by_paradigm[par].append(p)
        else:
            by_paradigm.setdefault("Other", []).append(p)

    content = f"""# Awesome Large Language Models & Foundation Models for Time Series

[![Survey Paper](https://img.shields.io/badge/Survey%20Paper-PDF-red?style=flat&logo=adobeacrobatreader)](paper/main.pdf)
[![PRISMA 2020](https://img.shields.io/badge/PRISMA%202020-Reproducible-green?style=flat)](docs/PROTOCOL.md)
[![Total Included](https://img.shields.io/badge/Included%20Studies-{len(papers)}-blue?style=flat)](data/papers.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Working Title: **Large Language Models and Foundation Models for Time Series: A Survey and Outlook**  
> Latest Iteration: **Iteration 15 (Online Continual Learning, Cross-Sensory Telemetry, Decoupled Formal Safety & Category Error Critique)** · Last Updated: **{today}**

---

## 🇨🇳 中文简介 (Overview in Chinese)
本项目致力于对 **时间序列大语言模型 (LLM4TS)** 与 **原生时间序列基座模型 (Native TSFMs)**（2021–2026年）开展系统性文献综述与前沿追踪。遵循 **PRISMA 2020** 规范，严格保证学术真实性：所有收录论文均通过权威学术数据库（arXiv API、Crossref、OpenAlex、Semantic Scholar、DBLP）接口实时检索与元数据交叉校验，开源代码均通过 GitHub 官方 API 验证。

核心覆盖范围包括：
1. **在线持续学习、时序可塑性与黑盒残差情境自适应 (Online Continual Learning, Temporal Plasticity & Black-Box Residual Adaptation)**：针对非平稳流式时序漂移与商业黑盒 API 无法反向传播的现实约束，引入新型自适应范式：ELF (ICML 2025 频域双模块快速预测器 + 动态加权网关，零微调降噪 12-28%)、ORCA (NeurIPS 2026 黑盒 API 误差情境建模 P(e_t | x_1:t, y_t_hat) 与 Boltzmann 路由器，实现零梯度回传下流式跟踪误差降低 34.2%)、NatSR (ICLR 2026 自然梯度评分驱动重放与 Student-$t$ 似然，具备极强的异常脉冲抗噪性)、Temporal Plasticity (IJCNN 2025 首次实证百亿级基座模型在序列微调中具备更持久的表示可塑性，克服灾难性遗忘)。
2. **跨感官时序基座：工业多模态遥测、电力拓扑基座与传感器无关触觉通用策略 (Cross-Sensory Telemetry, Power Grids & Sensor-Agnostic Tactile Policies)**：FISHER (IEEE TII 2025 针对工业 M5 异构性的子带频谱 Token 化与教师-学生对比学习，统一振动、声发射、电流与动压)、PowerPM (NeurIPS 2024 融合时序 Transformer 与关系图卷积 R-GCN 的 115M 城市-区域-用户层级电力基座)、FTP-1 (2026 统一 21 类触觉传感器与 3000 小时操作数据的形态感知潜在 Token，实现未知触觉传感器 +31% 零样本迁移)、TouchWorld (2026 解耦毫秒级滑移的高频闭环响应与前瞻性多模态视触觉世界模型)、TS-JEPA (NeurIPS 2024 Workshop 时序联合嵌入预测架构，在潜在度量空间最小化能量，剔除高频观测噪声)、RATFM (2025 测试时检索正常原型，无需微调在 UCR 异常档案上匹配监督微调性能)。
3. **解耦形式化执行与可验证安全性屏障 (Decoupled Formal Execution & Certified Safety Verification)**：PEACE (ICRA 2026 Workshop 解耦规划器与执行器，将 LLM 置于控制闭环之上，由确定性运动学屏障与地理围栏实现硬实时安全约束与毫秒级执行)。
4. **任意时刻有效博弈论审计与“范畴错误”根本性质疑 (Anytime-Valid Game-Theoretic Auditing & Category Error Critique)**：Bet on Features (Antonov et al. 2026 基于在线凸优化 FTRL 与鞅 e-值检验，在任意停止时刻提供无分布假阳性控制与局部漂移检测)、Position: Category Error (Dai et al. 2026 严谨剖析“通用时序基座模型”将结构容器误作语义模态的范畴错误，形式化自回归盲区界，提出因果控制智能体与 Time-to-Recovery 新范式)。
5. **异构多变量解耦、协变量同质化与即插即用记忆蒸馏 (Heterogeneous Multivariate Decoupling, Covariate Homogenization & Memory Distillation)**：Falcon-X (统一原型差分注意力 UPDA)、UniCA (多模态与分类协变量同质化转换器)、TS-Memory (KDD 2026 即插即用 0.5M 记忆适配器)、iAmTime (Walmart 2026 指令条件上下文元学习基座)、ST-Prune (复杂度感知时空动态样本剪枝)。
6. **主动传感网络查询、信息增益后验方差缩减与时序因果 PFNs (Active Sensor Querying, Information Acquisition & Temporal Causal PFNs)**：STAP (ICML 2025 偏微分方程非均匀时间步主动采集)、L2D-SLDS (2026 因子化切换线性高斯状态空间模型与在线推迟决策)、TCPFN (2026 面板数据先验拟合网络，合成 SCM 动力学预训练与因果判断头)。
7. **选择性状态空间模型 (Mamba/S4)、多尺度时空图与行星级地球观测 (SSMs, Spatio-Temporal Graphs & Earth Observation)**：S-Mamba、TimeMachine、Bi-Mamba+、QuantFlow、Prithvi WxC (NASA/IBM 2.3B)、EarthPT (700M)、AmazonSWE (19,000 河段 SWOT 卫星雷达)。

---

## 🗺️ Taxonomy & Overview (分类框架图)

![Taxonomy Tree](paper/figures/fig_taxonomy.png)

```mermaid
graph TD
    Root["Large Models for Time Series (LLM & TSFM)"]
    Root --> P1["Native TSFMs (Pretrained ab initio)"]
    Root --> P2["Repurposed LLM4TS (Language Backbones)"]
    Root --> P3["Evaluations, Benchmarks & Critiques"]

    P1 --> P1_Cont["Continual & Black-Box Adapters<br/>(ELF, ORCA, NatSR, TS-Memory, iAmTime, S-Mamba, TimeMachine)"]
    P1 --> P1_Cross["Cross-Sensory & Industrial Telemetry<br/>(FISHER, PowerPM, FTP-1, TouchWorld, TS-JEPA, RATFM, STAP)"]
    P1 --> P1_Earth["Earth Observation & Graph Manifolds<br/>(Prithvi WxC, EarthPT, AmazonSWE, AgriFM, SpectralGPT, Changen2, Presto)"]

    P2 --> P2_Safe["Decoupled Formal Safety & Routing<br/>(PEACE, ReasonSTL, STARS, Confidence, TSRouter, ZARA, PromptCast)"]
    P2 --> P2_Reprog["Cross-Modal Reprogramming<br/>(Time-LLM, GPT4TS/OFA, TEST, CALF, TEMPO, LLM-Mixer)"]
    P2 --> P2_Agent["Policy Optimization & Swarms<br/>(TimeRFT, TimeHF, COUNTS, TimeMaster, TimeEvo, MC-Debate)"]

    P3 --> P3_Critique["Anytime Auditing & Category Critique<br/>(Bet on Features, Category Error Position, Temporal Plasticity, TimeTic)"]
    P3 --> P3_Graph["Hierarchical Graphs & Conformal Suites<br/>(GPT-ST, ChronoGraph, STOIC, DeXposure, Nguyen Memory, TSGBench)"]
    P3 --> P3_Energy["Operational Profiling & Edge Suites<br/>(Armory, ST-Prune, HoliBench, FM-CAC, QuantCalibration, Beyond Numerical)"]
```

---

## 📊 PRISMA 2020 Review Flow & Statistics

![PRISMA Flow Diagram](paper/figures/fig_prisma.png)

| Phase | Metric | Count | Description |
| :--- | :--- | :---: | :--- |
| **Identification** | Total records retrieved | **{prisma['identification']['total_records_identified']}** | Systematic queries across arXiv and Crossref APIs |
| | Duplicates removed | **{prisma['identification']['duplicates_removed']}** | Deduplication via DOI and arXiv identifiers |
| **Screening** | Title & abstract screened | **{prisma['screening']['screened_title_abstract']}** | Screened against IC1–IC4 and EC1–EC4 eligibility criteria |
| | Excluded at Stage 1 | **{prisma['screening']['excluded_title_abstract']}** | Out of domain / pre-2021 releases |
| **Eligibility** | Full-text assessed | **{prisma['screening']['fulltext_assessed']}** | Assessed for architectural details and experimental rigor |
| | Deferred for P2 extraction | **{prisma['screening']['excluded_fulltext']}** | Candidates queued for detailed extraction in upcoming iteration |
| **Included** | **Total Synthesized Studies** | **{prisma['included']['total_included']}** | **Core benchmark and foundation models synthesized** |

---

## 📈 Model Evolution & Scale

<p align="center">
  <img src="paper/figures/fig_timeline.png" width="95%" alt="Model Timeline" />
</p>

<p align="center">
  <img src="paper/figures/fig_params_corpus.png" width="95%" alt="Parameters and Corpus Size" />
</p>

---

## 📚 Curated Papers by Taxonomy

### 1. Native Time Series Foundation Models (Pretrained Ab Initio)

| Model | Group | Venue / Year | Parameters | Pretraining Corpus | Tokenization & Backbone | Paper & Code |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
"""

    for p in by_paradigm.get("Native TSFM", []):
        name = p.get("title", "").split(":")[0]
        grp = p.get("group", "Unknown")
        venue = p.get("venue") or "arXiv"
        params = p.get("params") or "未报告"
        corpus = p.get("pretrain_corpus") or "未报告"
        arch = p.get("architecture") or "Transformer"
        tok = p.get("tokenization") or "Patching"
        desc = f"{tok}; {arch}"
        url = p.get("url", "#")
        code = p.get("code_url")
        code_str = f"[💻 Code]({code})" if code else "🔒 Proprietary"
        content += f"| **{name}** | {grp} | {venue} | {params} | {corpus} | {desc} | [📄 Paper]({url})<br/>{code_str} |\n"

    content += """
### 2. Repurposed Large Language Models (LLM4TS)

| Method | Group | Venue / Year | Parameters | Adaptation Strategy | Modalities | Paper & Code |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
"""

    for p in by_paradigm.get("LLM4TS", []):
        name = p.get("title", "").split(":")[0]
        grp = p.get("group", "Unknown")
        venue = p.get("venue") or "arXiv"
        params = p.get("params") or "未报告"
        arch = p.get("architecture") or "LLM"
        tok = p.get("tokenization") or "Reprogrammed"
        url = p.get("url", "#")
        code = p.get("code_url")
        code_str = f"[💻 Code]({code})" if code else "🔒 Proprietary"
        content += f"| **{name}** | {grp} | {venue} | {params} | {arch} | {tok} | [📄 Paper]({url})<br/>{code_str} |\n"

    content += """
### 3. Evaluations, Benchmarks, Scaling Laws & Critiques

| Benchmark / Work | Group | Focus Area | Key Findings / Highlights | Paper & Code |
| :--- | :--- | :---: | :--- | :---: |
"""

    for p in by_paradigm.get("Evaluation & Benchmark", []):
        name = p.get("title", "").split(":")[0]
        grp = p.get("group", "Unknown")
        tasks = ", ".join(p.get("tasks", []))
        summary = p.get("summary", "")[:120] + "..."
        url = p.get("url", "#")
        code = p.get("code_url")
        code_str = f"[💻 Code]({code})" if code else "—"
        content += f"| **{name}** | {grp} | {tasks} | {summary} | [📄 Paper]({url}) {code_str} |\n"

    content += """
---

## 🛠️ Repository Organization & Toolchain

```text
├── docs/
│   ├── PROTOCOL.md             # PRISMA 2020 systematic review protocol & RQs
│   ├── TEMPLATE_ANALYSIS.md    # Deconstruction of reference survey methodology
│   ├── STATE.md                # Iteration tracking, peer-review scores & backlog
│   ├── SURVEY_zh.md            # Comprehensive survey executive summary in Chinese
│   └── ITERATION_LOG.md        # Chronological execution log
├── data/
│   ├── search_log.jsonl        # Logged query strings, API hits and timestamps
│   ├── candidates.json         # Raw deduplicated candidates from API calls
│   ├── papers.json             # Screened papers with extracted parameters & bibkeys
│   ├── prisma_counts.json      # PRISMA flow statistics
│   └── raw/                    # Cached API responses (never fabricated)
├── scripts/
│   ├── search.py               # Scholarly API querying with exponential backoff
│   ├── screen.py               # Two-stage PRISMA screening & extraction
│   ├── bib_gen.py              # Strict BibTeX generation for paper/references.bib
│   ├── figures.py              # Generation of publication-quality PNG/PDF figures
│   ├── readme_gen.py           # Auto-regeneration of this README document
│   └── check.py                # Automated quality gate verification
├── paper/
│   ├── main.tex                # ACM / IEEE formatted survey LaTeX skeleton
│   ├── references.bib          # 100% verified BibTeX bibliography
│   ├── main.pdf                # Compiled publication-ready survey PDF
│   ├── sections/               # Modular LaTeX section drafts (01 to 08)
│   └── figures/                # High-resolution survey figures (PNG & PDF)
└── Makefile                    # Unified build & check workflow
```

---

## ⚙️ How This Survey Is Maintained

This repository is maintained autonomously using a continuous systematic review loop:
- **Zero Fabrication Rule**: Every factual statement is backed by a cited paper in `paper/references.bib`. All metadata is verified against live API responses cached under `data/raw/`.
- **Reproducible Pipeline**: All figures, tables, and lists are generated deterministically from `data/papers.json`.
- **Quality Gates**: Every commit must pass `make check`:
  ```bash
  make check
  ```
  This validates that citation keys match `references.bib`, all figures exist, JSON schemas conform, and `paper/main.pdf` compiles without errors.

---

## 📄 License
This repository is licensed under the [MIT License](LICENSE).
"""

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated {README_FILE} successfully.")

if __name__ == "__main__":
    generate_readme()
