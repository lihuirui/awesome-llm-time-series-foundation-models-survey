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
> Latest Iteration: **Iteration 10 (Earth Observation Foundations, DP Generative Twins & Neuro-Symbolic Temporal Logic)** · Last Updated: **{today}**

---

## 🇨🇳 中文简介 (Overview in Chinese)
本项目致力于对 **时间序列大语言模型 (LLM4TS)** 与 **原生时间序列基座模型 (Native TSFMs)**（2021–2026年）开展系统性文献综述与前沿追踪。遵循 **PRISMA 2020** 规范，严格保证学术真实性：所有收录论文均通过权威学术数据库（arXiv API、Crossref、OpenAlex、Semantic Scholar、DBLP）接口实时检索与元数据交叉校验，开源代码均通过 GitHub 官方 API 验证。

核心覆盖范围包括：
1. **遥感雷达与行星级地球观测时序基座 (Earth Observation & Satellite Radar Foundations)**：将时序基座模型拓展至行星级空间-光谱-时间连续张量，涵盖多时相卫星影像、合成孔径雷达 (SAR) 微波回波与全球气象重分析场，如 Prithvi WxC (NASA/IBM 2.3B参数全球天气与气候基座模型，覆盖40+年MERRA-2与ERA5的160个大气变量)、EarthPT (700M参数自回归解码器，在Sentinel-2超百亿像素时序上无监督预训练)、Prithvi-EO-2.0 (300M参数多时相ViT，420万全球场景预训练)、AgriFM (86M参数全天候Sentinel-1 SAR与Sentinel-2光学跨模态融合农业基座模型)、SpectralGPT (600M参数3D空-谱-时张量掩码自编码器)、Changen2 (120M参数连续流生成扩散变化检测模型)、Presto (4.8M紧凑型多传感器像素时序Transformer) 等。
2. **差分隐私生成孪生与零泄露基准评测 (Differentially Private Generative Twins & Zero-Leakage Benchmarks)**：攻克真实工业、医疗与电力时序评测中的数据污染与隐私逆向泄露难题，构建严格数学证明的 $(\epsilon, \delta)$-差分隐私生成孪生，如 Schuchardt et al. (ICML 2025 Spotlight，针对自相关滑动窗口创立结构化子采样 Rényi 差分隐私计算体系，首次证明时序深度基座模型的无界隐私放大与 $\epsilon < 2.0$ 强保障)、TSGBench (VLDB 2024，提出严格的 Train-on-Synthetic Test-on-Real (TSTR) 统一评估框架与成员推理防御评测) 等。
3. **神经符号时间逻辑与可微形式化约束 (Neuro-Symbolic Temporal Logic & Verifiable Constraints)**：将连续神经网络表征与形式化信号时序逻辑 (Signal Temporal Logic, STL) 的定量鲁棒度语义 $\rho(\varphi, x, t)$ 深度融合，如 Candussio et al. (ECML-PKDD 2025，首创 Transformer 自回归解码器将连续逻辑嵌入逆映射为人类可读离散 STL 语法树)、STARS (Ferfoglia et al. 2025，基于 STL 鲁棒性概念瓶颈层的可解释安全关键分类器)、Confidence over Time (ETH Zurich 2026，将 LLM 多步推理置信度轨迹建模为连续时序并挖掘 STL 异常行为模板以校准幻觉)、ReasonSTL (浙江大学/西湖大学 2026，过程监督强化学习结合 SMT/dReal 求解器实现 91.4% 高准确度自然语言到可执行 STL 规约转化)。
4. **人类与物理反馈强化学习策略优化 (RLHF/RLPF Policy Optimization)**：TimeRFT (HKUST'26 质量与拐点感知分步奖励 $r_t$ 结合高熵样本挑选，OOD误差降低18.6%)、TimeHF (京东 6B 基座模型引入时序策略优化 TPO 与专家偏好对齐，补货决策精度提升33.21%)、COUNTS (JHU NeurIPS'25 RVQ-VAE离散符号化结合分组相对策略优化 GRPO 激发可验证思维链推理)、TimeMaster (浙江大学多模态生理波形分步诊断奖励消减幻觉)、LAST SToP (Vector/Guelph ICML'25 异步时序随机软提示)。
5. **免分布保形预测与有限样本统计覆盖保证 (Distribution-Free Conformal Prediction)**：Achour et al. (零样本基座模型实现 $100\%$ 目标数据投入校准，获得严格 $1-\alpha$ 边际覆盖且置信区间优于 GBDT/ARIMA)、Adaptive Conformal Anomaly Detection (IBM Research ICLR'26 工业 IoT 严格虚警率受控 p 值输出)、RareCP (柏林自由大学 GIFT-Eval 上基于余弦注意力检索 MoE 缩窄区间达22%)。
6. **物理引导基座模型与连续时间异步事件流 (Physics Foundations & Continuous Event Streams)**：GridSFM (UW/微软 2026，内置非线性牛顿潮流方程的物理图网络，万节点电网零样本计算误差仅2.45%)、SurF (多伦多大学/Vector 2026，时间尺度重整化定理 TRT 连续流双射实现多数据集联合预训练)、TradeFM (摩根大通 524M 订单流生成基座模型)。
7. **极端1-Bit端侧量化与多智能体协作辩论 (1-Bit Quantization & Multi-Agent Swarms)**：Sparse Binary Transformers (1-bit权重纯加减累加)、Q-DEQ (0.3M深度平衡Picard-Broyden收缩映射解算器)、MC-Debate (KAIST 多模态多智能体协商)、TimeEvo (动态代码与技能自演化)、TSFMAudit (分位数N-Gram污染扫描器)。

---

## 🗺️ Taxonomy & Overview (分类框架图)

![Taxonomy Tree](paper/figures/fig_taxonomy.png)

```mermaid
graph TD
    Root["Large Models for Time Series (LLM & TSFM)"]
    Root --> P1["Native TSFMs (Pretrained ab initio)"]
    Root --> P2["Repurposed LLM4TS (Language Backbones)"]
    Root --> P3["Evaluations, Benchmarks & Critiques"]

    P1 --> P1_Dec["Autoregressive & Patch Decoders<br/>(Chronos, TimesFM-3, Timer, Sundial, TiRex, Toto, Tabby, Cadence, SGA)"]
    P1 --> P1_EO["Earth Observation & Planetary Foundations<br/>(Prithvi WxC, EarthPT, Prithvi-EO-2.0, AgriFM, SpectralGPT, Changen2, Presto)"]
    P1 --> P1_Phys["Physics, 1-Bit & Continuous Streams<br/>(GridSFM, SurF, TradeFM, Sparse Binary, Q-DEQ, TQS-PTQ, MCU-FQT)"]

    P2 --> P2_Reprog["Cross-Modal Reprogramming<br/>(Time-LLM, GPT4TS/OFA, TEST, CALF, TEMPO)"]
    P2 --> P2_Logic["Neuro-Symbolic & Temporal Logic<br/>(ReasonSTL, STARS, Candussio et al., Confidence-STL)"]
    P2 --> P2_Agent["Policy Optimization & Swarms<br/>(TimeRFT, TimeHF, COUNTS, TimeMaster, TimeEvo, MC-Debate)"]

    P3 --> P3_Bench["DP Twins & Living Benchmarks<br/>(TSGBench, DP-Subsampling, Forecast-Dojo, Impermanent, TimeSage, GIFT-Eval)"]
    P3 --> P3_Conf["Conformal Coverage & Statistical Audits<br/>(Achour et al., Adaptive-CAD, RareCP, TSFMAudit, Familiarity Bias)"]
    P3 --> P3_Energy["Energy, Quantization & Edge Suites<br/>(HoliBench, FM-CAC, QuantCalibration, Table 5, Table 8, Table 10)"]
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
