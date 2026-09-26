# Systematic Review Protocol: Large Language Models and Foundation Models for Time Series

## 1. Protocol Identification and Changelog
- **Protocol Version**: 1.6.0
- **Initial Date**: 2026-09-24
- **Last Amended**: 2026-09-26
- **Methodological Standard**: PRISMA 2020 (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)
- **Target Repository**: `lihuirui/awesome-llm-time-series-foundation-models-survey`

### Changelog
- **2026-09-26 (v1.6.0)**: Iteration 8 update: Formalized multi-agent collaborative ensembles, swarm deliberation, and dynamic consensus (MC-Debate, TimeEvo, Hu et al. 2026 self-evolving policies, Traceable-Agent, MetaCaster); formulated extreme 1-bit binary parameterization and deep equilibrium quantization (Sparse Binary Transformers with addition-only ALU accumulation, Q-DEQ with INT4/INT8 Picard-Broyden contractive solvers, SGA state-guided autoregressive uncertainty calibration); deployed automated data contamination auditing harness (`scripts/audit_contamination.py`, `make audit`) implementing quantile n-gram hashing and mutual information permutation testing; synthesized pretraining familiarity bias, temporal hold-out leakage, and replayable agent environments (TSFMAudit, Moghadasi & Ghaderi 2026, Pan & Ezzat 2026 electricity price stress-testing, Forecast-Dojo); expanded synthesis to Table 8; updated PRISMA cohort to 125 verified included studies.
- **2026-09-26 (v1.5.0)**: Iteration 7 update: Integrated interactive time-series agents, tool-augmented reasoning, and autonomous multi-model arbitration (TimeInteract, Cast-R1, TimeART, TS-Reasoner, DCATS, TimeAgent); synthesized extreme low-bit post-training quantization and edge microcontroller adaptation (TQS-PTQ dynamical systems sensitivity, 4-bit activation calibration audit across 560 models, and MCU-FQT on-device fully quantized training for ARM Cortex-M); integrated living streaming benchmarks and multi-turn agentic evaluation suites (Impermanent on top-400 GitHub daily streams, TimeSage-MT across 240 tasks and 2,680 turns); synthesized leakage-free macroeconomic pretraining (MACROCAST on synthetic BVAR/DFMs); expanded synthesis to Table 7; updated PRISMA cohort to 113 verified included studies.
- **2026-09-26 (v1.4.0)**: Iteration 6 update: Formalized non-stationary temporal drift and test-time adaptation (TTA; TSF-TTA, AdaNODEs, RG-TTA, FAC framework); integrated causal discovery, structural causal priors (SCMs), and counterfactual foundation models (Causal-PT, CausalTimePrior, CaTSG, CausalTime benchmark, Jander et al. causal audit uncovering persistence bias); incorporated production-grade TimesFM-3 (330M, 1T tokens) and Cadence error-bounded lossy compression; integrated living community leaderboards (TIME benchmark across 50 fresh datasets and HuggingFace Spaces); expanded synthesis to Table 6; updated PRISMA cohort to 102 verified included studies.
- **2026-09-26 (v1.3.0)**: Iteration 5 update: Deepened omni-modal representations binding continuous numerical sensor waveforms, 2D visual spectrograms/satellite imagery, and time-aligned textual event logs (VisionTS++, VLT, Chronicle, ChronoSteer, TiMo); synthesized empirical energy profiles, integer-only quantization degradation (FP16 $\to$ INT8 $\to$ INT4), and edge hardware envelopes across microcontrollers, FPGAs, and embedded IoT devices (Table 5; HoliBench, FM-CAC, Ling et al., Cheraghinia et al., APEX-Edge, Tiny-TSM); deployed autonomous living discovery watchdog script (`scripts/watchdog.py`, `make watchdog`); updated PRISMA cohort to 92 verified included studies.
- **2026-09-26 (v1.2.0)**: Iteration 4 update: Extended temporal search window to 2026-09-26; incorporated Spatio-Temporal Foundation Models (STFMs) unifying 1D temporal series with spatial graph topologies (OpenCity, UniST, UrbanDiT, UrbanFM, UrbanGPT, ST-LLM); expanded formal RQ6 to encompass algorithmic time complexity, KV-cache memory footprints, and sub-5ms hard real-time latency profiling across six foundation paradigms; automated continuous citation snowballing pipeline (`scripts/snowball.py`); updated PRISMA cohort to 81 verified included studies.
- **2026-09-25 (v1.1.0)**: Iteration 3 update: Extended temporal search window to 2026-09-25; added explicit focus on fine-tuning vs. in-context adaptation trade-offs (PEFT, LoRA, PFN in-context priors) and scaling laws meta-regression ($\alpha_N, \alpha_D$); integrated continuous delta search and snowballing for emerging 2025–2026 preprints.
- **2026-09-24 (v1.0.0)**: Initialized protocol for iteration 1 bootstrap: defined Research Questions RQ1–RQ7, Boolean query formulations across 4 scholarly engines, 2-stage screening criteria, data extraction schema, quality scoring rubric, and forward/backward snowballing procedure.

---

## 2. Research Questions (RQs)

- **RQ1 (Pretraining Corpora & Data Curation)**: What large-scale pretraining datasets (e.g., LOTSA, Monash Time Series Repository, UCR/UEA, synthetic generative datasets) are utilized for training time series foundation models? How are real-world temporal series cleaned, regularized, normalized, and balanced across diverse sampling rates and domains?
- **RQ2 (Architectural Paradigms)**: How do native Time Series Foundation Models (TSFMs)—including decoder-only autoregressive transformers, masked autoencoder encoders, encoder-decoder architectures, and mixture-of-experts (MoE)—compare conceptually and empirically with repurposed Large Language Models (LLM4TS) via parameter-efficient fine-tuning (PEFT), reprogramming, and cross-attention?
- **RQ3 (Tokenization & Input Representation)**: What strategies are employed to map continuous 1D/multidimensional temporal signals into discrete or dense token embeddings (e.g., subseries patching, continuous linear projections, scalar quantization/binning, frequency/wavelet tokenization, and explicit lag embeddings)?
- **RQ4 (Probabilistic Modeling & Uncertainty)**: How do modern foundation models capture epistemic and aleatoric temporal uncertainty? What are the tradeoffs between autoregressive categorical sampling (tokenized cross-entropy), parametric distributions (e.g., Gaussian, Student's t, negative binomial), quantile loss heads, and diffusion/flow matching?
- **RQ5 (Scaling Laws & Generalization)**: Is there empirical evidence for neural scaling laws (parameter count, dataset token volume, compute) in temporal foundation models? Under what data regimes does zero-shot inference match or surpass fully supervised, in-domain specialized deep learning baselines?
- **RQ6 (Efficiency & Practical Deployment)**: What are the computational requirements, parameter efficiency, memory footprint, and inference latency across model families? How do native TSFMs compare with multi-billion parameter LLMs in production settings?
- **RQ7 (Evaluation Protocols & Benchmark Pitfalls)**: What standardized benchmark suites (e.g., GIFT-Eval, fev-bench, Chronos-eval) exist? How do evaluation protocols address data leakage, temporal train-test overlap, and domain contamination?

---

## 3. Eligibility Criteria

### 3.1 Inclusion Criteria (IC)
- **IC1 (Temporal Scope)**: Published or preprint released between **2021-01-01** and the present (**2026-09-26**).
- **IC2 (Topic Relevance)**:
  - (a) Pre-trained time series foundation models trained on cross-domain time-series corpora (e.g., Chronos, TimesFM, Moirai, MOMENT, Lag-Llama, Timer, Sundial, Time-MoE, Toto, TabPFN-TS, TTM, etc.).
  - (b) Large Language Models adapted, reprogrammed, prompted, or fine-tuned for time series analysis (e.g., Time-LLM, GPT4TS/OFA, LLMTime, TEMPO, TEST, S2IP-LLM, etc.).
  - (c) Theoretical studies, scaling law evaluations, benchmark suites, and critical analyses evaluating the effectiveness and foundational validity of LLMs/TSFMs.
- **IC3 (Methodological Soundness)**: Clear architectural description, reproducible methodology, and empirical evaluation on recognized time-series tasks (forecasting, imputation, anomaly detection, classification, reasoning).
- **IC4 (Language & Verifiability)**: Peer-reviewed conference/journal paper or verifiable arXiv preprint with complete metadata verified by scholarly APIs (arXiv, OpenAlex, Semantic Scholar, DBLP, or Crossref).

### 3.2 Exclusion Criteria (EC)
- **EC1 (Out of Scope)**: Narrow single-dataset models with no pretraining or foundation model aspect (e.g., standard vanilla LSTM/GRU or classic ARIMA applied to a single local sensor without transfer learning or large-scale pretraining).
- **EC2 (Pure Spatio-Temporal Graph without Foundation Pretraining)**: Classic localized traffic GCNs without foundation model or general temporal pretraining capabilities.
- **EC3 (Non-Verifiable / Incomplete)**: Works lacking formal publication metadata, non-English papers, or unverified claims without code/methodological transparency.
- **EC4 (Duplicate / Superseded)**: Earlier preprint drafts completely subsumed by an updated peer-reviewed conference/journal version (the authoritative peer-reviewed version is retained).

---

## 4. Information Sources and Search Strategies

Searches are executed programmatically using automated scripts (`scripts/search.py`) with full caching under `data/raw/` and logging in `data/search_log.jsonl`.

### 4.1 Target Sources
1. **arXiv API** (`https://export.arxiv.org/api/query`):
   - Categories: `cs.LG`, `cs.AI`, `stat.ML`.
   - Politeness: Descriptive User-Agent, $\ge 3$s delay between queries.
2. **Semantic Scholar Graph API** (`https://api.semanticscholar.org/graph/v1/`):
   - Paper search and citation/reference graph traversal.
3. **OpenAlex API** (`https://api.openalex.org/works`):
   - Broad scholarly indexing and venue verification.
4. **DBLP API** (`https://dblp.org/search/publ/api`):
   - Peer-reviewed venue verification for top conferences (NeurIPS, ICML, ICLR, KDD, AAAI, IJCAI, WWW, TPAMI).

### 4.2 Verbatim Boolean Search Strings
1. **Query 1 (Native TSFM Core)**:
   `("time series foundation model" OR "foundation models for time series" OR "time-series foundation model" OR "large time series model") AND (pretrain OR pretrained OR pre-trained OR "zero-shot")`
2. **Query 2 (Repurposed LLM for Time Series)**:
   `("large language model" OR "LLM") AND ("time series" OR "temporal data") AND (reprogramming OR "prompt tuning" OR "zero-shot" OR "cross-modal" OR forecasting)`
3. **Query 3 (Specific Key Families & Groups)**:
   `("Chronos" OR "TimesFM" OR "MOIRAI" OR "MOMENT" OR "Lag-Llama" OR "Time-LLM" OR "GPT4TS" OR "Timer" OR "Sundial" OR "Time-MoE" OR "Tiny Time Mixer" OR "TTM") AND ("time series" OR forecasting)`
4. **Query 4 (Evaluation, Scaling Laws & Critiques)**:
   `("scaling law" OR "scaling laws" OR "are LLMs actually useful" OR "benchmark" OR "zero-shot forecasting" OR "GIFT-Eval") AND ("time series foundation" OR "LLM for time series")`

---

## 5. Screening and Snowballing Procedures

### 5.1 Two-Stage Screening
1. **Stage 1 (Title and Abstract Screening)**:
   - Automated screening script checks keyword relevance and scope boundaries.
   - Assigns initial screening status: `candidate` vs. `excluded_title` (with explicit `exclusion_reason`).
2. **Stage 2 (Full-Text Eligibility Screening)**:
   - Full text / detailed abstract and methodology reviewed.
   - Evaluated against inclusion/exclusion criteria.
   - Assigns final status: `included` vs. `excluded_fulltext`.

### 5.2 Snowballing Procedure
- For every core included paper (e.g., Chronos, TimesFM, Moirai, Time-LLM, PatchTST, MOMENT, Timer, Lag-Llama):
  - **Backward Snowballing**: Review foundational cited architectures and pretraining datasets.
  - **Forward Snowballing**: Traversal of forward citations via Semantic Scholar Graph API to capture subsequent extensions, derivatives, and critical benchmark evaluations.

---

## 6. Data Extraction Schema and Quality Rubric

### 6.1 Extraction Fields (in `data/papers.json`)
Every included paper records:
```json
{
  "id": "arxiv:2403.07815",
  "bibkey": "ansari2024chronos",
  "title": "Chronos: Learning the Language of Time Series",
  "authors": ["Abdul Fatir Ansari", "Lorenzo Stella", "Caner Turkmen", "..."],
  "year": 2024,
  "venue": "ICML",
  "venue_type": "conference",
  "doi": "10.48550/arXiv.2403.07815",
  "url": "https://arxiv.org/abs/2403.07815",
  "code_url": "https://github.com/amazon-science/chronos-forecasting",
  "status": "included",
  "screening_date": "2026-09-24",
  "exclusion_reason": null,
  "taxonomy": {
    "paradigm": "Native TSFM",
    "architecture": "Decoder-only (T5/T5-based)",
    "tokenization": "Scalar quantization & binning (categorical tokens)",
    "pretraining_objective": "Cross-entropy token classification",
    "prediction_head": "Categorical distribution over quantized bins",
    "pretraining_corpus": "TSMix synthetic data + 14 real-world datasets (~84B observations)",
    "parameters": "20M, 46M, 200M, 710M",
    "scope": "General-purpose",
    "tasks": ["Probabilistic Forecasting", "Zero-shot Forecasting"]
  },
  "quality_score": {
    "methodological_soundness": 3,
    "empirical_evaluation": 3,
    "clarity_reproducibility": 3,
    "open_science": 3,
    "total": 12
  }
}
```

### 6.2 Quality Scoring Rubric (0 to 3 per criterion; Max: 12)
1. **Methodological Rigor**: 3 = novel, theoretically grounded architecture; 2 = standard solid design; 1 = minimal architectural novelty; 0 = vague or flawed.
2. **Empirical Evaluation**: 3 = extensive zero-shot cross-domain evaluation against state-of-the-art baselines; 2 = multiple standard datasets; 1 = narrow benchmark; 0 = single dataset or questionable split.
3. **Reproducibility**: 3 = fully open weights, code, and training data recipes; 2 = open weights and inference code; 1 = code without weights/training details; 0 = proprietary/no code.
4. **Impact & Relevance**: 3 = seminal foundation model or widely adopted benchmark; 2 = solid established extension; 1 = incremental adaptation; 0 = marginal relevance.
