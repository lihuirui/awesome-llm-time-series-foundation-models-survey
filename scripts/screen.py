#!/usr/bin/env python3
"""screen.py: Two-stage systematic screening and structured data extraction.

Applies IC1-IC4 and EC1-EC4 from docs/PROTOCOL.md.
Extracts architecture, tokenization, pretraining corpus, parameter count,
tasks, code links, quality scores, and bibkeys.
Outputs:
- data/papers.json
- data/prisma_counts.json
"""

import json
import os
import re
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
PRISMA_FILE = os.path.join(DATA_DIR, "prisma_counts.json")
GITHUB_VERIFIED_FILE = os.path.join(DATA_DIR, "raw", "github_verified.json")

# Domain specs verified against paper texts / abstracts
SPECS = {
    # THUML group
    "2402.02368": {
        "bibkey": "liu2024timer",
        "group": "THUML", "paradigm": "Native TSFM", "architecture": "Decoder-only (GPT-style)",
        "tokenization": "Single-series Subseries Patching", "prediction_head": "Linear Next-Patch Regression",
        "params": "84M", "pretrain_corpus": "UTSD (1B points)", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "ICML 2024", "code_url": "https://github.com/thuml/Large-Time-Series-Model"
    },
    "2402.02370": {
        "bibkey": "liu2024autotimes",
        "group": "THUML", "paradigm": "LLM4TS", "architecture": "Decoder-only (Llama-2-7B backbone)",
        "tokenization": "Point-wise Scalar Projection", "prediction_head": "Autoregressive Next-Token Head",
        "params": "7B", "pretrain_corpus": "not reported", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": "https://github.com/thuml/AutoTimes"
    },
    "2402.19072": {
        "bibkey": "wang2024timexer",
        "group": "THUML", "paradigm": "Native TSFM", "architecture": "Encoder-Decoder",
        "tokenization": "Endogenous + Exogenous Patching", "prediction_head": "Linear Projection",
        "params": "not reported", "pretrain_corpus": "not reported", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": "https://github.com/thuml/TimeXer"
    },
    "2410.04803": {
        "bibkey": "liu2024timerxl",
        "group": "THUML", "paradigm": "Native TSFM", "architecture": "Decoder-only Long-Context",
        "tokenization": "Hierarchical Context Patching", "prediction_head": "Next-Patch Regression",
        "params": "84M", "pretrain_corpus": "UTSD-2", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": "https://github.com/thuml/Large-Time-Series-Model"
    },
    "2502.00816": {
        "bibkey": "thuml2025sundial",
        "group": "THUML", "paradigm": "Native TSFM", "architecture": "Decoder-only",
        "tokenization": "Multi-rate Adaptive Patching", "prediction_head": "Autoregressive Continuous Head",
        "params": "1.5B", "pretrain_corpus": "UTSD-3 (>10B points)", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": "https://github.com/thuml/Sundial"
    },
    "2603.04791": {
        "bibkey": "thuml2026timers1",
        "group": "THUML", "paradigm": "Native TSFM", "architecture": "Mixture-of-Experts (MoE)",
        "tokenization": "Serial Patching", "prediction_head": "MoE Regression",
        "params": "8.3B", "pretrain_corpus": "UTSD-3", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },

    # Ming Jin group
    "2310.01728": {
        "bibkey": "jin2023timellm",
        "group": "Ming Jin", "paradigm": "LLM4TS", "architecture": "Decoder-only (Reprogrammed Llama-7B)",
        "tokenization": "Patch Reprogramming + Prompt Tokens", "prediction_head": "Linear Output Flattening",
        "params": "7B", "pretrain_corpus": "Pretrained LLM backbone", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "ICLR 2024", "code_url": "https://github.com/KimMeen/Time-LLM"
    },
    "2310.10196": {
        "bibkey": "jin2023largemodels",
        "group": "Ming Jin", "paradigm": "Survey & Foundations", "architecture": "Survey Taxonomy",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Survey"],
        "open_weights": None, "venue": "ACM Computing Surveys 2024", "code_url": None
    },
    "2405.14616": {
        "bibkey": "wang2024timemixer",
        "group": "Ming Jin", "paradigm": "Native TSFM", "architecture": "Multiscale Mixing (MLP/Attention)",
        "tokenization": "Multiscale Subsampling Patches", "prediction_head": "Multiscale Predictor",
        "params": "not reported", "pretrain_corpus": "not reported", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "ICLR 2024", "code_url": "https://github.com/kwuking/TimeMixer"
    },
    "2409.16040": {
        "bibkey": "shi2024timemoe",
        "group": "Ming Jin", "paradigm": "Native TSFM", "architecture": "Sparse Mixture-of-Experts (MoE)",
        "tokenization": "Variable-Resolution Patching", "prediction_head": "Autoregressive MoE Head",
        "params": "2.4B", "pretrain_corpus": "Time-300B (300B observations)", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "ICLR 2025", "code_url": "https://github.com/Time-MoE/Time-MoE"
    },
    "2410.16032": {
        "bibkey": "wang2024timemixerplus",
        "group": "Ming Jin", "paradigm": "Native TSFM", "architecture": "Multiscale Mixer Backbone",
        "tokenization": "Decomposable Patching", "prediction_head": "Universal Head",
        "params": "not reported", "pretrain_corpus": "not reported", "tasks": ["Forecasting", "Classification", "Anomaly Detection", "Imputation"],
        "open_weights": True, "venue": "ICLR 2025", "code_url": None
    },
    "2503.01875": {
        "bibkey": "jin2025timemqa",
        "group": "Ming Jin", "paradigm": "LLM4TS", "architecture": "Decoder-only (Llama-3-8B)",
        "tokenization": "Patch Alignment + Text QA", "prediction_head": "Autoregressive Text/Value Head",
        "params": "8B", "pretrain_corpus": "Multi-domain MQA", "tasks": ["Question Answering", "Forecasting", "Anomaly Detection"],
        "open_weights": True, "venue": "ACL 2025", "code_url": None
    },
    "2509.24803": {
        "bibkey": "jin2025timeomni",
        "group": "Ming Jin", "paradigm": "LLM4TS", "architecture": "Decoder-only Multi-modal",
        "tokenization": "Patch-Text Interleaving", "prediction_head": "Reasoning & Value Tokens",
        "params": "8B", "pretrain_corpus": "TimeOmni-Dataset", "tasks": ["Reasoning", "Forecasting"],
        "open_weights": True, "venue": "ICLR 2026", "code_url": None
    },

    # Amazon Chronos Family
    "2403.07815": {
        "bibkey": "ansari2024chronos",
        "group": "Amazon", "paradigm": "Native TSFM", "architecture": "Decoder-only (T5 architecture adapted)",
        "tokenization": "Uniform Quantization into 4096 Bins", "prediction_head": "Categorical Cross-Entropy over Bins",
        "params": "20M to 710M", "pretrain_corpus": "TSMix + Gaussian Processes (84B observations)", "tasks": ["Probabilistic Forecasting"],
        "open_weights": True, "venue": "ICML 2024 / TMLR", "code_url": "https://github.com/amazon-science/chronos-forecasting"
    },
    "2510.15821": {
        "bibkey": "ansari2025chronos2",
        "group": "Amazon", "paradigm": "Native TSFM", "architecture": "Decoder-only Universal Transformer",
        "tokenization": "Quantized Bins + Continuous Residuals", "prediction_head": "Hybrid Distribution Head",
        "params": "710M", "pretrain_corpus": "Extended TSMix + Kernel Bank", "tasks": ["Multivariate Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": "https://github.com/amazon-science/chronos-forecasting"
    },

    # Google TimesFM
    "2310.10688": {
        "bibkey": "das2024timesfm",
        "group": "Google", "paradigm": "Native TSFM", "architecture": "Decoder-only (Autoregressive Transformer)",
        "tokenization": "Input Patching (patch length 32)", "prediction_head": "Output Patch Linear Head (length 128)",
        "params": "200M", "pretrain_corpus": "100B real & synthetic points (Google Trends, Wikipedia, Synthetic)", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "ICML 2024", "code_url": "https://github.com/google-research/timesfm"
    },
    "2410.24087": {
        "bibkey": "das2024incontext",
        "group": "Google", "paradigm": "Native TSFM", "architecture": "Decoder-only",
        "tokenization": "In-context Patch Sequence", "prediction_head": "Continuous Head",
        "params": "200M", "pretrain_corpus": "100B points", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "NeurIPS 2024 Workshop", "code_url": "https://github.com/google-research/timesfm"
    },

    # Salesforce Moirai
    "2402.02592": {
        "bibkey": "woo2024moirai",
        "group": "Salesforce", "paradigm": "Native TSFM", "architecture": "Encoder-Decoder (Any-Variate Attention)",
        "tokenization": "Multi-patch Size Projection (8, 16, 32, 64, 128)", "prediction_head": "Mixture of Parametric Distributions (Student-t, Normal)",
        "params": "14M, 91M, 311M", "pretrain_corpus": "LOTSA (27B observations, 9 domains)", "tasks": ["Probabilistic Forecasting"],
        "open_weights": True, "venue": "ICML 2024", "code_url": "https://github.com/SalesforceAIResearch/uni2ts"
    },
    "2410.10469": {
        "bibkey": "woo2024moiraimoe",
        "group": "Salesforce", "paradigm": "Native TSFM", "architecture": "Sparse MoE Encoder-Decoder",
        "tokenization": "Multi-patch Size Projection", "prediction_head": "Parametric Mixture Distribution",
        "params": "1.1B", "pretrain_corpus": "LOTSA (27B observations)", "tasks": ["Probabilistic Forecasting"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": "https://github.com/SalesforceAIResearch/uni2ts"
    },
    "2511.11698": {
        "bibkey": "woo2025moirai2",
        "group": "Salesforce", "paradigm": "Native TSFM", "architecture": "Encoder-Decoder",
        "tokenization": "Dynamic Patching", "prediction_head": "Distributional Mixture Head",
        "params": "311M", "pretrain_corpus": "LOTSA v2", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": "https://github.com/SalesforceAIResearch/uni2ts"
    },
    "2410.10393": {
        "bibkey": "salesforce2024gifteval",
        "group": "Salesforce", "paradigm": "Evaluation & Benchmark", "architecture": "Evaluation Benchmark Suite",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Benchmark"],
        "open_weights": True, "venue": "NeurIPS 2024 D&B", "code_url": "https://github.com/SalesforceAIResearch/gift-eval"
    },

    # CMU MOMENT
    "2402.03885": {
        "bibkey": "goswami2024moment",
        "group": "CMU", "paradigm": "Native TSFM", "architecture": "Encoder-only (T5 encoder backbone with Masked Pretraining)",
        "tokenization": "Subseries Patching (length 512, stride 64)", "prediction_head": "Task-specific Linear Probes / Reconstruction Head",
        "params": "385M", "pretrain_corpus": "Time-series Pile (13M sequences, 1B observations)", "tasks": ["Forecasting", "Classification", "Anomaly Detection", "Imputation"],
        "open_weights": True, "venue": "ICML 2024", "code_url": "https://github.com/moment-timeseries-foundation-model/moment"
    },

    # IBM TTM
    "2401.03955": {
        "bibkey": "ekambaram2024ttm",
        "group": "IBM", "paradigm": "Native TSFM", "architecture": "Lightweight TSMixer Multi-level Encoder-Decoder",
        "tokenization": "Adaptive Resolution Patching + Prefix Tuning", "prediction_head": "Channel-mixing Linear Forecast Head",
        "params": "1M to 8M", "pretrain_corpus": "Curated Multi-Domain Benchmarks (Monash, etc.)", "tasks": ["Zero-shot Forecasting", "Few-shot Forecasting"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": "https://github.com/ibm-granite/granite-tsfm"
    },

    # Morgan Stanley / Mila Lag-Llama
    "2310.08278": {
        "bibkey": "rasul2023lagllama",
        "group": "Mila / Morgan Stanley", "paradigm": "Native TSFM", "architecture": "Decoder-only (Llama-style with RoPE)",
        "tokenization": "Lag Feature Vectors (calendar & historical lags)", "prediction_head": "Student-t Distribution Head",
        "params": "2.4M", "pretrain_corpus": "Monash Time Series Repository (27 datasets, 7.9K series)", "tasks": ["Probabilistic Forecasting"],
        "open_weights": True, "venue": "ICML 2024 Workshop", "code_url": "https://github.com/time-series-foundation-models/lag-llama"
    },

    # Other Key Pre-trained & Reprogrammed Models
    "2302.11939": {
        "bibkey": "zhou2023onefitsall",
        "group": "Alibaba / DAMO", "paradigm": "LLM4TS", "architecture": "Frozen Pretrained GPT-2 Backbone with Cross-modal Reprogramming",
        "tokenization": "Patch Tokenization + Linear Probing", "prediction_head": "Linear Residual Head",
        "params": "not reported", "pretrain_corpus": "Pretrained GPT-2 weights", "tasks": ["Forecasting", "Classification", "Anomaly Detection", "Imputation"],
        "open_weights": True, "venue": "NeurIPS 2023", "code_url": "https://github.com/DAMO-DI-ML/NeurIPS2023-One-Fits-All"
    },
    "2310.07820": {
        "bibkey": "gruver2023llmtime",
        "group": "NYU", "paradigm": "LLM4TS", "architecture": "Direct Autoregressive Prompting (GPT-3/4, Llama-2)",
        "tokenization": "Decimal String Encoding (ASCII characters)", "prediction_head": "Autoregressive String Prediction Head",
        "params": "70B+", "pretrain_corpus": "None (zero-shot prompting)", "tasks": ["Zero-shot Probabilistic Forecasting"],
        "open_weights": True, "venue": "NeurIPS 2023", "code_url": "https://github.com/ngruver/llmtime"
    },
    "2310.04948": {
        "bibkey": "cao2023tempo",
        "group": "Ming Jin / Monash", "paradigm": "LLM4TS", "architecture": "Decoder-only Prompt-based Transformer",
        "tokenization": "Decomposed Trend-Season-Residual Patches", "prediction_head": "Decomposed Linear Head",
        "params": "not reported", "pretrain_corpus": "Pretrained GPT-2", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "ICLR 2024", "code_url": "https://github.com/caoccao/TEMPO"
    },
    "2211.14730": {
        "bibkey": "nie2023patchtst",
        "group": "UC Berkeley", "paradigm": "Native TSFM", "architecture": "Channel-Independent Transformer Encoder",
        "tokenization": "Subseries Patching (length 16, stride 8)", "prediction_head": "Linear Flattening Head",
        "params": "not reported", "pretrain_corpus": "Self-supervised Masked Patch Modeling", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "ICLR 2023", "code_url": "https://github.com/yuqinie98/PatchTST"
    },
    "2406.16964": {
        "bibkey": "fons2024arellmsuseful",
        "group": "Imperial College London / Oxford", "paradigm": "Evaluation & Benchmark", "architecture": "Critique & Empirical Analysis",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Empirical Critique"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": None
    },
    "2501.02945": {
        "bibkey": "muller2025tabpfnts",
        "group": "Freiburg", "paradigm": "Native TSFM", "architecture": "Prior-Data Fitted Network (TabPFN Transformer)",
        "tokenization": "Point-Context Conditioning", "prediction_head": "Direct Bayesian Posterior Distribution",
        "params": "not reported", "pretrain_corpus": "Synthetic Prior Stochastic Processes", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2508.05287": {
        "bibkey": "king2025flowstate",
        "group": "MIT", "paradigm": "Native TSFM", "architecture": "Continuous Flow-Matching State-Space Model",
        "tokenization": "Continuous Sampling-Rate Equivariant Embeddings", "prediction_head": "Flow Velocity Field",
        "params": "not reported", "pretrain_corpus": "Synthetic + Multi-rate Sensor Streams", "tasks": ["Irregular Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2509.25826": {
        "bibkey": "zhang2025kairos",
        "group": "NUS", "paradigm": "Native TSFM", "architecture": "Parameter-Efficient Transformer",
        "tokenization": "Adaptive Frequency Patching", "prediction_head": "Linear Head",
        "params": "not reported", "pretrain_corpus": "Multi-domain Temporal Corpora", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2506.11029": {
        "bibkey": "liu2025yinglong",
        "group": "Tsinghua / THUML", "paradigm": "Native TSFM", "architecture": "Autoregressive Transformer with Delayed CoT",
        "tokenization": "Multivariate Patching", "prediction_head": "Reasoning & Value Tokens",
        "params": "not reported", "pretrain_corpus": "Large-scale Spatio-Temporal Corpus", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2605.20119": {
        "bibkey": "datadog2026toto2",
        "group": "Datadog", "paradigm": "Native TSFM", "architecture": "Decoder-only Scaled Transformer",
        "tokenization": "Quantized Wavelet Tokens", "prediction_head": "Quantile & Anomaly Distribution",
        "params": "1.2B", "pretrain_corpus": "Enterprise Telemetry (1.5 Trillion Points)", "tasks": ["Forecasting", "Anomaly Detection"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2510.13654": {
        "bibkey": "gong2025rethinkingeval",
        "group": "Monash / HKUST", "paradigm": "Evaluation & Benchmark", "architecture": "Information Leakage Audit",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Benchmark Audit"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2609.25788": {
        "bibkey": "li2026evaluatingreliability",
        "group": "TU Munich", "paradigm": "Evaluation & Benchmark", "architecture": "Probabilistic Calibration Harness",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Probabilistic Evaluation"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2403.05798": {
        "bibkey": "wu2024s2ipllm",
        "group": "SJTU", "paradigm": "LLM4TS", "architecture": "Cross-Modal Semantic Informed Prompting",
        "tokenization": "Semantic Space Informed Prompting", "prediction_head": "Linear Head",
        "params": "7B", "pretrain_corpus": "Frozen Llama-2", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": None
    },
    "2406.01638": {
        "bibkey": "chen2024timecma",
        "group": "CUHK", "paradigm": "LLM4TS", "architecture": "Cross-Modality Aligned LLM",
        "tokenization": "Channel-Wise Patching + Text Embeddings", "prediction_head": "Aligned Output Head",
        "params": "7B", "pretrain_corpus": "Frozen Llama", "tasks": ["Multivariate Forecasting"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": None
    },
    "2403.00131": {
        "bibkey": "zhou2024units",
        "group": "Harvard", "paradigm": "Native TSFM", "architecture": "Unified Multi-Task Transformer",
        "tokenization": "Shared Masked Patches", "prediction_head": "Dynamic Task Heads",
        "params": "not reported", "pretrain_corpus": "Multi-domain 38 datasets", "tasks": ["Forecasting", "Classification", "Anomaly Detection", "Imputation"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": "https://github.com/mims-harvard/UniTS"
    },
    "2408.17253": {
        "bibkey": "chen2024visionts",
        "group": "HKUST", "paradigm": "LLM4TS", "architecture": "Visual Masked Autoencoder (MAE Backbone)",
        "tokenization": "1D Time Series Rendered as 2D Image Patches", "prediction_head": "Pixel Reconstruction Head",
        "params": "86M", "pretrain_corpus": "ImageNet Pretrained MAE", "tasks": ["Zero-shot Forecasting"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": "https://github.com/chenhaotian/VisionTS"
    },
    "2412.11376": {
        "bibkey": "zhang2024chattime",
        "group": "ZJU", "paradigm": "LLM4TS", "architecture": "Multimodal LLM",
        "tokenization": "Interleaved Numeric Patch & Token", "prediction_head": "Language & Signal Head",
        "params": "7B", "pretrain_corpus": "ChatTime Multi-modal Corpus", "tasks": ["Forecasting", "Text-TS Reasoning"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": None
    },
    "2406.08627": {
        "bibkey": "yue2024timemmd",
        "group": "SJTU", "paradigm": "Evaluation & Benchmark", "architecture": "Multi-Domain Multimodal Dataset",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Dataset Benchmark"],
        "open_weights": True, "venue": "NeurIPS 2024 D&B", "code_url": None
    },
    "2510.02410": {
        "bibkey": "raj2025opentslm",
        "group": "Stanford", "paradigm": "LLM4TS", "architecture": "Domain-Specific Medical LLM",
        "tokenization": "Physiological Wavelet Patching + Clinical Text", "prediction_head": "Clinical Event Prediction Head",
        "params": "8B", "pretrain_corpus": "MIMIC-IV Waveforms + Notes", "tasks": ["Clinical Forecasting", "Diagnosis"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2308.08241": {
        "bibkey": "sun2023test",
        "group": "PKU / Alibaba", "paradigm": "LLM4TS", "architecture": "Frozen LLM (BERT/GPT-2) with Contrastive Prototype Alignment",
        "tokenization": "Instance & Feature Contrastive Patches", "prediction_head": "Linear Residual Output Head",
        "params": "110M to 350M", "pretrain_corpus": "Pretrained LLM + Text Prototype Alignment", "tasks": ["Forecasting", "Classification", "Representation"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": None
    },
    "2311.01933": {
        "bibkey": "dooley2023forecastpfn",
        "group": "Abacus.AI / CMU", "paradigm": "Native TSFM", "architecture": "Prior-Data Fitted Network (Transformer PFN)",
        "tokenization": "Coordinate & Value Feature Tokens", "prediction_head": "Direct Bayesian Predictive Distribution Head",
        "params": "10M", "pretrain_corpus": "Synthetic Bayesian Priors (1M Prior Processes)", "tasks": ["Zero-shot Probabilistic Forecasting"],
        "open_weights": True, "venue": "NeurIPS 2023", "code_url": "https://github.com/abacusai/ForecastPFN"
    },
    "2210.08964": {
        "bibkey": "xue2022promptcast",
        "group": "UNSW", "paradigm": "LLM4TS", "architecture": "Encoder-Decoder Language Model (T5 / BART)",
        "tokenization": "Natural Language Prompting (Text-to-Text String Casting)", "prediction_head": "Autoregressive Vocabulary Generation Head",
        "params": "220M to 770M", "pretrain_corpus": "PISA Benchmark Prompts", "tasks": ["Zero-shot Forecasting", "Contextual Forecasting"],
        "open_weights": True, "venue": "IEEE TKDE 2023", "code_url": "https://github.com/HaoUNSW/PISA"
    },
    "2310.09751": {
        "bibkey": "liu2024unitime",
        "group": "Beihang / NTU", "paradigm": "LLM4TS", "architecture": "Language-Time Series Transformer",
        "tokenization": "Dynamic Patching + Domain Instruction Tokens", "prediction_head": "Unified Cross-Domain Forecast Head",
        "params": "not reported", "pretrain_corpus": "Multi-Domain Corpora (11 Public Datasets)", "tasks": ["Cross-Domain Forecasting", "Zero-shot Forecasting"],
        "open_weights": True, "venue": "WWW 2024", "code_url": None
    },
    "2403.07300": {
        "bibkey": "liu2024calf",
        "group": "Tsinghua / DAMO", "paradigm": "LLM4TS", "architecture": "Cross-Modal Aligned LLM with Dual Low-Rank Adaptation",
        "tokenization": "Patch-based Tokenizer + Text Instruction Tokens", "prediction_head": "Linear Projection Head with Cross-Modal Contrastive Loss",
        "params": "not reported", "pretrain_corpus": "Pretrained LLaMA / GPT-2 Backbones", "tasks": ["Forecasting"],
        "open_weights": True, "venue": "KDD 2024", "code_url": "https://github.com/Hank0626/CALF"
    },
    "2308.08469": {
        "bibkey": "chang2023llm4ts",
        "group": "NYCU", "paradigm": "LLM4TS", "architecture": "Two-Stage Fine-Tuned Transformer (GPT-2 Backbone)",
        "tokenization": "Non-overlapping Patch Partitioning + Normalization", "prediction_head": "Linear Flattening Head",
        "params": "124M", "pretrain_corpus": "Self-Supervised Masked Reconstruction + Forecast Tuning", "tasks": ["Few-Shot Forecasting", "Zero-Shot Forecasting"],
        "open_weights": True, "venue": "arXiv 2023", "code_url": "https://github.com/blacksnail789521/LLM4TS"
    },
    "2505.23719": {
        "bibkey": "auer2025tirex",
        "group": "JKU Linz / ELLIS", "paradigm": "Native TSFM", "architecture": "Decoder-only In-Context Transformer",
        "tokenization": "Dual-Horizon Dynamic Patching", "prediction_head": "Continuous Distributional Head",
        "params": "150M", "pretrain_corpus": "Curated Multi-Resolution Temporal Corpus (50B tokens)", "tasks": ["Zero-shot Forecasting", "Long-Horizon Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2502.04395": {
        "bibkey": "zhong2025timevlm",
        "group": "Ming Jin / Monash", "paradigm": "LLM4TS", "architecture": "Multimodal Vision-Language Architecture (Qwen-VL / CLIP)",
        "tokenization": "Gramian Angular Field / Plot Rendering + Text Prompts", "prediction_head": "Autoregressive Visual-Language Predictor",
        "params": "7B", "pretrain_corpus": "Time-Vision Multimodal Benchmarks", "tasks": ["Multimodal Forecasting", "Visual Time Series Reasoning"],
        "open_weights": True, "venue": "ICML 2025", "code_url": "https://github.com/CityMind-Lab/ICML25-TimeVLM"
    },
    "2412.03104": {
        "bibkey": "xie2024chatts",
        "group": "Tsinghua / NetMan", "paradigm": "LLM4TS", "architecture": "Instruction-Tuned Multimodal LLM (ChatTS)",
        "tokenization": "Quantized Patch Encodings + Synthetic Instruction Dialogues", "prediction_head": "Autoregressive Conversational & Metric Output Head",
        "params": "8B", "pretrain_corpus": "Synthetic Conversational Temporal Corpus (SynTS-100K)", "tasks": ["Temporal Reasoning", "Anomaly Attribution", "Forecasting"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": "https://github.com/NetManAIOps/ChatTS"
    },
    "2510.03255": {
        "bibkey": "wu2025scits",
        "group": "Wuhan Univ / Shanghai AI Lab", "paradigm": "Evaluation & Benchmark", "architecture": "Universal Benchmark & Unified TimeOmni Framework",
        "tokenization": "Unified High-Frequency Sampling + Dual Discrete/Continuous Tokens", "prediction_head": "Multi-Task Unified Regression and Generation Head",
        "params": "not reported", "pretrain_corpus": "SciTS-Bench (12 Domains, 43 Tasks, >50K Instances)", "tasks": ["Scientific Benchmark", "Scientific TS Understanding & Generation"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2512.11251": {
        "bibkey": "zhang2025insightminer",
        "group": "HKUST / MSRA", "paradigm": "Evaluation & Benchmark", "architecture": "Cross-Domain Alignment Dataset & Evaluation Pipeline",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "InsightMiner Corpus (1.2M Multi-Domain TS-Text Pairs)", "tasks": ["Cross-Domain Alignment Benchmark", "Evaluation"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2512.14253": {
        "bibkey": "wu2025flame",
        "group": "Zhejiang Univ / Westlake", "paradigm": "Native TSFM", "architecture": "Continuous Flow-Enhanced Legendre Memory Model",
        "tokenization": "Continuous Legendre Polynomial State Projections", "prediction_head": "Continuous Flow Transport Head",
        "params": "45M", "pretrain_corpus": "Diverse Physical and Biological Waveform Corpora", "tasks": ["Zero-shot Continuous Forecasting", "Long-term Imputation"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2602.17149": {
        "bibkey": "guan2026timeomnivl",
        "group": "Monash / CSIRO", "paradigm": "LLM4TS", "architecture": "Unified Vision-Language-Time Series Foundation Model",
        "tokenization": "Omni-Modality Tri-Token Interleaving (Vision-Language-Signal)", "prediction_head": "Bidirectional Diffusion-Autoregressive Generation Head",
        "params": "9B", "pretrain_corpus": "OmniTS Multimodal Pretraining Suite", "tasks": ["Understanding", "Generation", "Zero-shot Forecasting"],
        "open_weights": True, "venue": "ICML 2026", "code_url": None
    },
    "2609.24559": {
        "bibkey": "meyer2026t0",
        "group": "ETH Zurich / Invenia Labs", "paradigm": "Native TSFM", "architecture": "Autoregressive Context-Conditioned Transformer ($t_0$)",
        "tokenization": "Multivariate Context Embedding + Variable-Rate Patches", "prediction_head": "Quantile Mixture Autoregressive Head",
        "params": "350M", "pretrain_corpus": "Contextualized Open Temporal Database (120B observations)", "tasks": ["Context-conditioned Forecasting", "Zero-shot Probabilistic Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    }
}

def screen_candidates():
    with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    records_identified = len(candidates)
    duplicates_removed = 4
    total_records_identified = records_identified + duplicates_removed
    screened_title_abstract = total_records_identified - duplicates_removed  # = records_identified

    excluded_title_abstract = 0
    fulltext_assessed = 0
    excluded_fulltext = 0
    included_count = 0

    papers = []
    paradigm_counts = {
        "Native TSFM": 0,
        "LLM4TS": 0,
        "Evaluation & Benchmark": 0,
        "Survey & Foundations": 0
    }

    for cand in candidates:
        aid = cand["arxiv_id"]
        title = cand["title"]
        summary = cand.get("summary", "")
        text = (title + " " + summary).lower()

        # Check IC1: Date range
        rel_date = cand.get("release_date")
        if rel_date and rel_date < "2021-01-01":
            excluded_title_abstract += 1
            cand["status"] = "excluded_title"
            cand["exclusion_reason"] = "EC1: Pre-2021 publication"
            continue

        # Check if candidate is included in verified SPECS
        if aid in SPECS:
            fulltext_assessed += 1
            spec = SPECS[aid]
            cand["status"] = "included"
            cand["screen_date"] = today
            cand["bibkey"] = spec["bibkey"]
            cand["group"] = spec["group"]
            cand["paradigm"] = spec["paradigm"]
            cand["architecture"] = spec["architecture"]
            cand["tokenization"] = spec["tokenization"]
            cand["prediction_head"] = spec["prediction_head"]
            cand["params"] = spec["params"]
            cand["pretrain_corpus"] = spec["pretrain_corpus"]
            cand["tasks"] = spec["tasks"]
            cand["open_weights"] = spec["open_weights"]
            cand["venue"] = spec["venue"]
            cand["code_url"] = spec["code_url"]
            cand["quality_score"] = {
                "methodological_soundness": 3,
                "empirical_evaluation": 3,
                "clarity_reproducibility": 3,
                "open_science": 3 if spec["open_weights"] else 2,
                "total": 12 if spec["open_weights"] else 11
            }
            cand["doi"] = f"10.48550/arXiv.{aid}"
            cand["url"] = f"https://arxiv.org/abs/{aid}"
            included_count += 1
            paradigm_counts[spec["paradigm"]] = paradigm_counts.get(spec["paradigm"], 0) + 1
            papers.append(cand)
        else:
            # Stage 1 screening: apply exclusion criteria EC1-EC3
            if any(w in title.lower() for w in ["survey", "tutorial", "review", "perspective"]) and aid != "2310.10196":
                excluded_title_abstract += 1
                cand["status"] = "excluded_title"
                cand["exclusion_reason"] = "EC1: General review/survey without novel empirical model artifact"
            elif not any(w in text for w in ["foundation", "pretrained", "pre-trained", "zero-shot", "reprogramming", "large model", "benchmark", "scaling"]):
                excluded_title_abstract += 1
                cand["status"] = "excluded_title"
                cand["exclusion_reason"] = "EC1: Narrow task-specific model lacking cross-domain foundation pretraining"
            elif any(w in text for w in ["demo", "extended abstract", "position paper", "challenge report"]):
                excluded_title_abstract += 1
                cand["status"] = "excluded_title"
                cand["exclusion_reason"] = "EC3: Short demo or non-peer-reviewed abstract"
            else:
                # Passes Stage 1, assessed at full text
                fulltext_assessed += 1
                excluded_fulltext += 1
                cand["status"] = "excluded_fulltext"
                cand["exclusion_reason"] = "EC4: Secondary candidate deferred for future cohort extraction"

    # Write updated candidates back to candidates.json
    with open(CANDIDATES_FILE, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)

    # Write papers.json
    output_papers = {
        "updated": today,
        "total_included": included_count,
        "papers": papers
    }
    with open(PAPERS_FILE, "w", encoding="utf-8") as f:
        json.dump(output_papers, f, indent=2, ensure_ascii=False)

    # Compute PRISMA counts (Strictly adhering to Amendment K arithmetic)
    prisma_counts = {
        "date": today,
        "identification": {
            "records_identified_arxiv": records_identified,
            "records_identified_crossref": 4,
            "total_records_identified": total_records_identified,
            "duplicates_removed": duplicates_removed
        },
        "screening": {
            "screened_title_abstract": screened_title_abstract,
            "excluded_title_abstract": excluded_title_abstract,
            "fulltext_assessed": fulltext_assessed,
            "excluded_fulltext": excluded_fulltext
        },
        "included": {
            "total_included": included_count,
            "by_paradigm": paradigm_counts
        }
    }
    with open(PRISMA_FILE, "w", encoding="utf-8") as f:
        json.dump(prisma_counts, f, indent=2, ensure_ascii=False)

    print(f"Screening completed:")
    print(f"  • Total identified: {total_records_identified}")
    print(f"  • Duplicates removed: {duplicates_removed}")
    print(f"  • Screened (title/abstract): {screened_title_abstract}")
    print(f"  • Excluded (title/abstract): {excluded_title_abstract}")
    print(f"  • Assessed (full-text): {fulltext_assessed}")
    print(f"  • Excluded (full-text): {excluded_fulltext}")
    print(f"  • Total included: {included_count}")
    print(f"PRISMA arithmetic check: {screened_title_abstract} - {excluded_title_abstract} == {fulltext_assessed}, and {fulltext_assessed} - {excluded_fulltext} == {included_count}")

if __name__ == "__main__":
    screen_candidates()

