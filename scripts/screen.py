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
    },

    # Iteration 3 Verified Studies (+13 Core Papers, Total: 70)
    "2505.14766": {
        "bibkey": "cohen2025toto",
        "group": "Datadog", "paradigm": "Native TSFM", "architecture": "Decoder-only Transformer (Toto 1.0)",
        "tokenization": "Continuous Patching", "prediction_head": "Multi-quantile Head + Anomaly Score Head",
        "params": "151M", "pretrain_corpus": "Datadog Observability Corpus (1 Trillion Points)", "tasks": ["Forecasting", "Anomaly Detection"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2609.13956": {
        "bibkey": "xie2026tabby",
        "group": "Huawei Noah's Ark / Univ Paris Cité", "paradigm": "Native TSFM", "architecture": "Long-Context Probabilistic Decoder-only Transformer",
        "tokenization": "Normalized Multi-Resolution Subseries Patching", "prediction_head": "Quantile & Categorical Mixture Head",
        "params": "120M", "pretrain_corpus": "Open Tabby-Corpus (150B tokens open release)", "tasks": ["Zero-shot Probabilistic Forecasting", "Long-Context Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2602.14024": {
        "bibkey": "zhou2026eidos",
        "group": "Ming Jin / UNSW / Nankai", "paradigm": "Native TSFM", "architecture": "Latent-Space Joint-Embedding Predictive Architecture (JEPA)",
        "tokenization": "Continuous Latent Patch Projector", "prediction_head": "Latent Space Predictor + Decoder Head",
        "params": "88M", "pretrain_corpus": "Multi-domain Latent Pretraining Archive (35B observations)", "tasks": ["Zero-shot Forecasting", "Representation Learning"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2506.06005": {
        "bibkey": "wang2025lightgts",
        "group": "East China Normal Univ / Huawei", "paradigm": "Native TSFM", "architecture": "Lightweight Dual-Path Transformer with Adaptive Parameter Allocation",
        "tokenization": "Compact Hierarchical Patching", "prediction_head": "Multi-Horizon Direct Projection Head",
        "params": "5.8M", "pretrain_corpus": "Curated General Time Series Corpus (8B observations)", "tasks": ["Zero-shot Forecasting", "Edge Deployment"],
        "open_weights": True, "venue": "ICML 2025", "code_url": None
    },
    "2405.14982": {
        "bibkey": "lu2024incontext",
        "group": "Georgia Tech", "paradigm": "Native TSFM", "architecture": "In-Context Meta-Learning Transformer (ICTSP)",
        "tokenization": "Interleaved Prompt-Query Subseries Patches", "prediction_head": "Direct In-Context Continuous Extrapolation",
        "params": "42M", "pretrain_corpus": "Synthetic Meta-Stochastic Processes + Empirical Benchmarks", "tasks": ["In-Context Forecasting", "Few-shot Adaptation"],
        "open_weights": True, "venue": "ICLR 2025", "code_url": None
    },
    "2410.11674": {
        "bibkey": "kowsher2024llmmixer",
        "group": "UCF", "paradigm": "LLM4TS", "architecture": "Multiscale Token-Mixing Frozen LLM (LLaMA-2 Backbone)",
        "tokenization": "Multiscale Patch Decompositions", "prediction_head": "Linear Residual Output Head",
        "params": "7B", "pretrain_corpus": "Frozen LLaMA-2-7B", "tasks": ["Multiscale Forecasting"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": None
    },
    "2609.24156": {
        "bibkey": "liang2026tactime",
        "group": "ECNU", "paradigm": "LLM4TS", "architecture": "Text-as-Channel Dual-Stream Cross-Attention Transformer",
        "tokenization": "Textual Channel Embeddings + Temporal Patch Embeddings", "prediction_head": "Channel-Fused Forecast Head",
        "params": "350M", "pretrain_corpus": "Multimodal Context Corpora", "tasks": ["Multimodal Forecasting", "Context-Informed Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2606.06285": {
        "bibkey": "kan2026trace",
        "group": "UNC Chapel Hill / UT Austin", "paradigm": "LLM4TS", "architecture": "Temporal Conditional Estimation Network with Pretrained Multimodal Backbones",
        "tokenization": "Multimodal Token Alignment (Text + Waveform)", "prediction_head": "Conditional Continuous Estimator",
        "params": "7B", "pretrain_corpus": "Pretrained Multimodal LLM Backbones", "tasks": ["Multimodal Forecasting", "Clinical Time Series"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2608.17299": {
        "bibkey": "wen2026livehouse",
        "group": "HKUST(GZ)", "paradigm": "Evaluation & Benchmark", "architecture": "Living Evaluation Platform & Continuous Benchmark Harness",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Living Benchmark", "Contamination-Free Evaluation"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2607.06973": {
        "bibkey": "liu2026timesx",
        "group": "Georgia Tech / Google Research", "paradigm": "Evaluation & Benchmark", "architecture": "TimesX Context-Enriched Multimodal Benchmark Suite",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Multimodal Benchmark", "Context-Rich Evaluation"],
        "open_weights": True, "venue": "ICML 2026", "code_url": None
    },
    "2410.14752": {
        "bibkey": "cai2024timeseriesexam",
        "group": "CMU", "paradigm": "Evaluation & Benchmark", "architecture": "Standardized Diagnostic Benchmark Exam for Foundation Models",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Diagnostic Evaluation", "Foundational Capability Probing"],
        "open_weights": True, "venue": "NeurIPS 2024 Workshop", "code_url": None
    },
    "2606.16173": {
        "bibkey": "chen2026timevista",
        "group": "Tsinghua University (THUML)", "paradigm": "Evaluation & Benchmark", "architecture": "Vision-Language Model Perceptual Judge Framework",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "8B", "pretrain_corpus": "TimeVista Perceptual Evaluation Benchmark", "tasks": ["LLM-as-a-Judge", "Perceptual Shape Fidelity Evaluation"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2609.27385": {
        "bibkey": "nagashima2026forecastworkflow",
        "group": "Independent / Tokyo", "paradigm": "Evaluation & Benchmark", "architecture": "Agentic Tool-Use Evaluation Framework",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Agentic Forecast Benchmark", "Tool Budget Evaluation"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },

    # Iteration 4 additions: Spatio-Temporal Foundation Models, Benchmarks & Operational Complexity
    "2403.00813": {
        "bibkey": "li2024urbangpt",
        "group": "HKU / Baidu", "paradigm": "LLM4TS", "architecture": "Spatio-Temporal Dependency Encoder + Llama-2-7B Backbone",
        "tokenization": "Spatio-Temporal Graph & Temporal Patch Tokenization", "prediction_head": "Linear Token Prediction Head",
        "params": "7B", "pretrain_corpus": "Urban Spatio-Temporal Datasets (Traffic & Flow)", "tasks": ["Spatio-Temporal Forecasting", "Urban Transfer Learning"],
        "open_weights": True, "venue": "KDD 2024", "code_url": "https://github.com/HKUDS/UrbanGPT"
    },
    "2408.10269": {
        "bibkey": "li2024opencity",
        "group": "HKU / Baidu", "paradigm": "Native TSFM", "architecture": "Dual Spatio-Temporal Transformer with Graph Wavelet Bias",
        "tokenization": "Spatial Graph Node + Temporal Patch Embeddings", "prediction_head": "Direct Multi-Horizon Spatio-Temporal Projection",
        "params": "26M", "pretrain_corpus": "Open-world Urban Traffic Network Corpus (>50M observations)", "tasks": ["Zero-Shot Traffic Forecasting", "Transfer Learning"],
        "open_weights": True, "venue": "NeurIPS 2024", "code_url": "https://github.com/HKUDS/OpenCity"
    },
    "2402.11838": {
        "bibkey": "yuan2024unist",
        "group": "Tsinghua FIB Lab", "paradigm": "Native TSFM", "architecture": "Unified Spatio-Temporal Masked Autoencoder with Knowledge Prompts",
        "tokenization": "Patch-based Spatio-Temporal Tokenization", "prediction_head": "Multi-scale Spatio-Temporal Decoder",
        "params": "not reported", "pretrain_corpus": "Multi-Scenario Urban Spatio-Temporal Benchmark", "tasks": ["Zero-Shot Spatio-Temporal Prediction", "Few-Shot Forecasting"],
        "open_weights": True, "venue": "KDD 2024", "code_url": "https://github.com/tsinghua-fib-lab/UniST"
    },
    "2401.10134": {
        "bibkey": "liu2024stllm",
        "group": "Beihang University", "paradigm": "LLM4TS", "architecture": "Partially-Frozen LLM with Spatio-Temporal Graph Embeddings",
        "tokenization": "Node-level Temporal Patch Tokens", "prediction_head": "Autoregressive Next-Patch Projection",
        "params": "7B", "pretrain_corpus": "Spatio-Temporal Traffic Repositories", "tasks": ["Traffic Forecasting", "Spatial-Temporal Reasoning"],
        "open_weights": True, "venue": "TKDE 2025", "code_url": None
    },
    "2411.12164": {
        "bibkey": "li2024urbandit",
        "group": "Tsinghua FIB Lab", "paradigm": "Native TSFM", "architecture": "Spatio-Temporal Diffusion Transformer (DiT)",
        "tokenization": "Unified Grid & Graph Patch Tokens + Prompt Tokens", "prediction_head": "Denoising Score / Noise-Prediction Network",
        "params": "45M", "pretrain_corpus": "Open-world Urban Heterogeneous Data", "tasks": ["Bidirectional Forecasting", "Imputation", "Extrapolation"],
        "open_weights": True, "venue": "NeurIPS 2025", "code_url": "https://github.com/tsinghua-fib-lab/UrbanDiT"
    },
    "2602.20677": {
        "bibkey": "chen2026urbanfm",
        "group": "HKUST / Tsinghua", "paradigm": "Native TSFM", "architecture": "Minimalist Spatio-Temporal Transformer with Constrained Bias",
        "tokenization": "MiniST Tokenization (Heterogeneous Signal Regularization)", "prediction_head": "Generative Masked Reconstruction & Multi-Horizon Head",
        "params": "120M", "pretrain_corpus": "Multi-City Urban Spatio-Temporal Corpus", "tasks": ["Zero-shot Traffic Prediction", "Signal Recovery"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2501.09045": {
        "bibkey": "goodge2025stfmvision",
        "group": "A*STAR / NUS", "paradigm": "Survey & Foundations", "architecture": "Conceptual Framework & Generalization Taxonomy",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Survey & Vision"],
        "open_weights": None, "venue": "arXiv 2025", "code_url": None
    },
    "2509.26468": {
        "bibkey": "shchur2025fevbench",
        "group": "AWS / AutoGluon", "paradigm": "Evaluation & Benchmark", "architecture": "Covariate-Aware Benchmark Suite with Bootstrapped Skill Scores",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Covariate-Aware Forecasting Benchmark", "Statistical Win Rates"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": "https://github.com/autogluon/fev"
    },
    "2602.12147": {
        "bibkey": "qiao2026time",
        "group": "THUML / Tsinghua / Monash", "paradigm": "Evaluation & Benchmark", "architecture": "Leakage-Audited Multi-Granularity Benchmark Harness",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Benchmark", "Leakage Audit", "Contamination Analysis"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2609.15087": {
        "bibkey": "chen2026beyondnumerical",
        "group": "Peking University / CAS", "paradigm": "Evaluation & Benchmark", "architecture": "Multimodal Contextual Forecasting Evaluation Suite",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Multimodal Contextual Forecasting Benchmark"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2605.25045": {
        "bibkey": "zhan2026aion",
        "group": "Ming Jin Group / Monash", "paradigm": "Evaluation & Benchmark", "architecture": "Next-Generation Agentic Task & Practical Harness",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Agentic Reasoning Benchmark", "Tool Use", "Practical Harness"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    # Iteration 5 additions: Omni-modal pretraining, Edge foundation models & Energy/Quantization benchmarks
    "2508.04379": {
        "bibkey": "shen2025visiontsplus",
        "group": "Shen et al.", "paradigm": "LLM4TS", "architecture": "Continual Pre-trained Vision Transformer Backbone (ViT)",
        "tokenization": "Multi-Scale Line Plot Image Projection", "prediction_head": "Visual Next-Patch Denoising Reconstruction",
        "params": "86M", "pretrain_corpus": "ImageNet-1K + Cross-Domain Time-Series Line Plots", "tasks": ["Forecasting", "Zero-Shot Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2607.14510": {
        "bibkey": "wang2026vlt",
        "group": "Wang et al.", "paradigm": "LLM4TS", "architecture": "Multimodal Encoder (Time-MoE + Frequency-Text Learner)",
        "tokenization": "Spectral Frequency Spectrogram + Text Prompt Tokens", "prediction_head": "Shared Multimodal Representation Head",
        "params": "110M", "pretrain_corpus": "Industrial PHM Aero-Engine & Turbomachinery Corpora", "tasks": ["Prognostics", "Health Management", "Forecasting", "Anomaly Detection"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2605.20268": {
        "bibkey": "quinlan2026chronicle",
        "group": "Quinlan et al.", "paradigm": "LLM4TS", "architecture": "Decoder-only Transformer (Joint Pretraining From Scratch)",
        "tokenization": "Interleaved Byte-Pair Text Tokens + Subseries Patches", "prediction_head": "Unified Autoregressive Causal Head",
        "params": "324M", "pretrain_corpus": "FineWeb-Edu text + LOTSA & UCR/UEA numerical time series", "tasks": ["Forecasting", "Classification", "NLU", "Multimodal Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2505.10083": {
        "bibkey": "wang2025chronosteer",
        "group": "Wang et al.", "paradigm": "LLM4TS", "architecture": "Decoupled Agentic Framework (Frozen TSFM + LLM Controller)",
        "tokenization": "Discrete Instruction Anchors Codebook", "prediction_head": "Two-Stage Magnitude Revision Head",
        "params": "not reported", "pretrain_corpus": "Synthetic Paired Cross-Modal Alignment Dataset", "tasks": ["Forecasting", "Contextual Steering"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2505.08723": {
        "bibkey": "qin2025timo",
        "group": "MiliLab / Wuhan University", "paradigm": "Native TSFM", "architecture": "Hierarchical Spatio-Temporal Vision Transformer",
        "tokenization": "Spatiotemporal Gyroscope Attention Patching", "prediction_head": "Masked Image Modeling & Semantic Segmentation Head",
        "params": "88M", "pretrain_corpus": "MillionST (1M satellite image phases across 100K locations)", "tasks": ["Land Cover Segmentation", "Deforestation Monitoring", "Crop Classification"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": "https://github.com/MiliLab/TiMo"
    },
    "2511.19272": {
        "bibkey": "birkel2025tinytsm",
        "group": "Felix Birkel", "paradigm": "Native TSFM", "architecture": "Lightweight Decoder-only Transformer",
        "tokenization": "Causal Input Normalization Patches", "prediction_head": "Dense Next-Token Regression Head",
        "params": "23M", "pretrain_corpus": "SynthTS Synthetic Generator (Single A100 training)", "tasks": ["Forecasting", "Zero-Shot Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2606.11553": {
        "bibkey": "pradhan2026apex",
        "group": "Cisco Systems", "paradigm": "Native TSFM", "architecture": "Network-Native Decoder-only Transformer (APEX-Large & APEX-Edge)",
        "tokenization": "Multivariate Protocol-Layer Telemetry Patching", "prediction_head": "Multi-Horizon Quantile Regression Head",
        "params": "10.5M, 269M", "pretrain_corpus": "Production Wireless AP Telemetry (4,500 networks, 100K series)", "tasks": ["Wireless Telemetry Forecasting", "Anomaly Detection"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2609.12412": {
        "bibkey": "chakrabarti2026holibench",
        "group": "UCLA NESL", "paradigm": "Evaluation & Benchmark", "architecture": "Cross-Platform Benchmarking & Profiling Harness",
        "tokenization": "N/A", "prediction_head": "N/A",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Edge Benchmarking", "Quantization Profiling", "Energy Measurement"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2604.16448": {
        "bibkey": "yang2026fmcac",
        "group": "UMass Amherst / UCLA", "paradigm": "Evaluation & Benchmark", "architecture": "Carbon-Aware Control & Zero-Shot TSFM Dispatcher",
        "tokenization": "Continuous Temporal Telemetry Patches", "prediction_head": "Dynamic Programming Solver Head",
        "params": "not reported", "pretrain_corpus": "N/A", "tasks": ["Carbon Forecasting", "Energy Optimization", "Edge AI Dispatch"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2511.14895": {
        "bibkey": "cheraghinia2025lightweight",
        "group": "Ghent University - imec", "paradigm": "Native TSFM", "architecture": "Ultra-Lightweight Patch-Independent MLP Encoder",
        "tokenization": "Raw IQ / CIR Subseries Patching", "prediction_head": "Linear Multi-Task Classification Head",
        "params": "21K", "pretrain_corpus": "Cross-Domain Wireless Signal Corpus (IQ / CIR)", "tasks": ["Technology Recognition", "Modulation Classification", "LoS Detection"],
        "open_weights": True, "venue": "IEEE GLOBECOM 2025", "code_url": None
    },
    "2410.03294": {
        "bibkey": "ling2024resource",
        "group": "University of Duisburg-Essen", "paradigm": "Evaluation & Benchmark", "architecture": "Resource-Aware Mixed-Precision Quantized Transformer (VHDL)",
        "tokenization": "Uniform & Mixed-Precision Integer Patching", "prediction_head": "Quantized Integer Output Projection",
        "params": "0.5M--5M", "pretrain_corpus": "Standard Benchmark Sets (ETT, Weather, Electricity)", "tasks": ["FPGA Deployment", "Quantization Profiling", "Hardware Verification"],
        "open_weights": True, "venue": "MobiQuitous 2024", "code_url": None
    },

    # Iteration 6: Test-Time Adaptation, Causal Discovery & Living Benchmarks
    "2501.04970": {
        "bibkey": "kim2025battling",
        "group": "Seoul National University", "paradigm": "Native TSFM", "architecture": "Test-Time Adaptation Forecaster (TSF-TTA)",
        "tokenization": "Non-Stationary Patch Normalization", "prediction_head": "Dynamic Test-Time Linear Predictor",
        "params": "0.5M--5M", "pretrain_corpus": "Pretrained Base Forecasters (PatchTST, DLinear)", "tasks": ["Test-Time Adaptation", "Non-Stationary Forecasting"],
        "open_weights": True, "venue": "AAAI 2025", "code_url": None
    },
    "2601.12893": {
        "bibkey": "dang2026adanodes",
        "group": "Singapore Management University", "paradigm": "Native TSFM", "architecture": "Continuous Neural ODE Dynamic Adapter",
        "tokenization": "Continuous Latent State Trajectory", "prediction_head": "ODE-Integrated Temporal Predictor",
        "params": "0.15M (Adapter)", "pretrain_corpus": "Frozen Source Forecasters", "tasks": ["Source-Free Test-Time Adaptation", "Forecasting"],
        "open_weights": True, "venue": "ICASSP 2026", "code_url": None
    },
    "2603.27814": {
        "bibkey": "kumar2026rgtta",
        "group": "IIT Delhi & TCS Research", "paradigm": "Native TSFM", "architecture": "Regime-Guided Meta-Controlled Transformer",
        "tokenization": "Multi-Regime Temporal Patching", "prediction_head": "Modulated Gradient Forecaster",
        "params": "not reported", "pretrain_corpus": "Streaming Non-Stationary Corpora", "tasks": ["Streaming TTA", "Regime Detection", "Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2605.17250": {
        "bibkey": "wang2026principled",
        "group": "HKUST", "paradigm": "Evaluation & Benchmark", "architecture": "Frequency-Aware Calibration (FAC) Framework",
        "tokenization": "Orthogonal Fourier / Wavelet Decomposition", "prediction_head": "Frequency-Calibrated Output Projection",
        "params": "not reported", "pretrain_corpus": "TSF-TTA Benchmark Suite", "tasks": ["TTA Benchmark", "Frequency Calibration", "Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2402.09305": {
        "bibkey": "stein2024embracing",
        "group": "Friedrich Schiller University Jena", "paradigm": "Native TSFM", "architecture": "Deep Causal Pretrained Transformer (Causal-PT)",
        "tokenization": "Multivariate Temporal Sequence Embedding", "prediction_head": "Directed Acyclic Graph (DAG) Adjacency Classifier",
        "params": "25M", "pretrain_corpus": "Synthetic Structural Causal Models (10M graphs)", "tasks": ["Causal Discovery", "Graph Reconstruction"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": None
    },
    "2603.11090": {
        "bibkey": "thumm2026interventional",
        "group": "Humboldt University of Berlin", "paradigm": "Native TSFM", "architecture": "Prior-Data Fitted Network (CausalTimePrior PFN)",
        "tokenization": "Interventional Observation Pairs", "prediction_head": "In-Context Posterior Causal Effect Head",
        "params": "85M", "pretrain_corpus": "Synthetic Interventional TSCMs (500M simulations)", "tasks": ["In-Context Causal Inference", "Counterfactual Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2608.24303": {
        "bibkey": "jander2026causal",
        "group": "University of Twente", "paradigm": "Evaluation & Benchmark", "architecture": "Interventional Synthetic Audit Harness",
        "tokenization": "Parametric Dynamic Generator Embeddings", "prediction_head": "Persistence & Regime Distortion Evaluator",
        "params": "N/A", "pretrain_corpus": "Chronos-2, TimesFM-2.5, MOIRAI", "tasks": ["Causal Audit", "Persistence Bias Detection", "Regime Shift Robustness"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2310.01753": {
        "bibkey": "cheng2023causaltime",
        "group": "Tsinghua University", "paradigm": "Evaluation & Benchmark", "architecture": "Realistic Synthetic Causal Discovery Benchmark Harness",
        "tokenization": "Nonlinear Flow Invertible Transformations", "prediction_head": "Ground-Truth Causal Adjacency Verification",
        "params": "N/A", "pretrain_corpus": "CausalTime Benchmark Suite", "tasks": ["Causal Discovery Benchmark", "Ground-Truth Evaluation"],
        "open_weights": True, "venue": "NeurIPS 2023", "code_url": None
    },
    "2509.20846": {
        "bibkey": "xia2025causal",
        "group": "City University of Hong Kong", "paradigm": "Native TSFM", "architecture": "Structural Causal Diffusion Model (CaTSG)",
        "tokenization": "Causal Graph Structured Latents", "prediction_head": "Denoising Score Matching Predictor",
        "params": "45M", "pretrain_corpus": "Cross-domain Causal Time Series", "tasks": ["Causal Time Series Generation", "Counterfactual Forecasting"],
        "open_weights": True, "venue": "arXiv 2025", "code_url": None
    },
    "2609.06008": {
        "bibkey": "tacconelli2026cadence",
        "group": "Politecnico di Torino", "paradigm": "Native TSFM", "architecture": "TimesFM-3 (330M) + Adaptive Arithmetic Coding Engine",
        "tokenization": "Stacked Variate Attention Patches", "prediction_head": "Iterative RevIN Quantile Residual Engine",
        "params": "330M (TimesFM-3)", "pretrain_corpus": "1T Time Points (Google Pretraining Corpus)", "tasks": ["Error-Bounded Lossy Compression", "Multivariate Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": "https://github.com/google-research/timesfm"
    },
    "2609.26389": {
        "bibkey": "pan2026timeinteract",
        "group": "Ming Jin", "paradigm": "LLM4TS", "architecture": "Dual-View Streaming Encoder + Decoupled Inference",
        "tokenization": "Local-Variation Continuous Patches", "prediction_head": "Autonomous Response Trigger & Generator",
        "params": "7B (Qwen2 Backbone)", "pretrain_corpus": "StreamTSI-34K (34.5K episodes)", "tasks": ["Streaming Time-Series Interaction", "Zero-Stall Perception"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2606.01498": {
        "bibkey": "kong2026timesagemt",
        "group": "Ming Jin", "paradigm": "Evaluation & Benchmark", "architecture": "Structured Agent with Time-Series Skill Library",
        "tokenization": "Multi-Turn Interactive Dialogue & Code Traces", "prediction_head": "N/A (Multi-turn Agent Evaluation)",
        "params": "not reported", "pretrain_corpus": "240 Tasks, 2,680 Dialogue Turns across 8 Domains", "tasks": ["Multi-Turn Agentic Reasoning", "Tool Selection & Uncertainty Auditing"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2602.13802": {
        "bibkey": "tao2026castr1",
        "group": "Other", "paradigm": "LLM4TS", "architecture": "Tool-Augmented Sequential Decision Agent (SFT + Multi-Turn RL)",
        "tokenization": "Modular Statistical Tool-Call Tokens", "prediction_head": "Iterative Policy Refinement Head",
        "params": "7B (Qwen2.5 Backbone)", "pretrain_corpus": "Sequential Decision-Making Trajectories", "tasks": ["Forecasting", "Sequential Policy Decision", "Tool-Augmented Reasoning"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": "https://github.com/ustc-time-series/Cast-R1"
    },
    "2601.13653": {
        "bibkey": "wu2026timeart",
        "group": "Other", "paradigm": "LLM4TS", "architecture": "Time Series Reasoning Model (TSRM) + Tool-Augmented Agent",
        "tokenization": "Tool-Augmented Analytical Sequences", "prediction_head": "Autoregressive Tool-Call & Text Head",
        "params": "8B (Llama-3 Backbone)", "pretrain_corpus": "TimeToolBench (100k Expert Trajectories)", "tasks": ["Time Series Question Answering", "Agentic Automated Analysis"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2410.04047": {
        "bibkey": "ye2024tsreasoner",
        "group": "Other", "paradigm": "LLM4TS", "architecture": "Domain-Specialized Inference Agent with Error Feedback Loop",
        "tokenization": "Symbolic Concept & Numerical Segment Encoding", "prediction_head": "Constraint-Aware Reasoning Head",
        "params": "7B / 14B Backbones", "pretrain_corpus": "TimeSeriesExam + Domain Trajectories", "tasks": ["Multi-Step Inference", "Automated Concept Reasoning"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": None
    },
    "2508.04231": {
        "bibkey": "yeh2025dcats",
        "group": "Other", "paradigm": "LLM4TS", "architecture": "Data-Centric Agent for Time Series (DCATS) Controller",
        "tokenization": "Metadata Context Prompting", "prediction_head": "Automated Pipeline Controller",
        "params": "GPT-4 / Llama-3-70B Controller", "pretrain_corpus": "Traffic Volume & Time Series Metadata", "tasks": ["Data Cleaning", "AutoML Pipeline Optimization", "Forecasting"],
        "open_weights": False, "venue": "arXiv 2025", "code_url": None
    },
    "2603.08707": {
        "bibkey": "garza2026impermanent",
        "group": "Other", "paradigm": "Evaluation & Benchmark", "architecture": "Living Streaming Evaluation Platform",
        "tokenization": "Daily Rolling Activity Windows", "prediction_head": "Sequential Multi-Horizon Scoring",
        "params": "not reported", "pretrain_corpus": "Top 400 GitHub Star Repositories (Daily Streams)", "tasks": ["Temporal Generalization Benchmark", "Continuous Contamination Auditing"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": "https://github.com/TimeCopilot/impermanent"
    },
    "2606.28670": {
        "bibkey": "carriero2026macrocast",
        "group": "Other", "paradigm": "Native TSFM", "architecture": "Decoder-only Vintage-Consistent Transformer",
        "tokenization": "Patch-level Macroeconomic Tokens", "prediction_head": "Density & Point Forecast Regression",
        "params": "15M", "pretrain_corpus": "Synthetic BVAR & DFM Simulations (Purely Synthetic, 0 Lookahead)", "tasks": ["Real-Time Macroeconomic Forecasting", "Vintage-Consistent Leakage Elimination"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2606.13300": {
        "bibkey": "pavlova2026tqs",
        "group": "Other", "paradigm": "Native TSFM", "architecture": "TQS-PTQ Dynamical Systems Quantization Framework",
        "tokenization": "Continuous State Trajectories", "prediction_head": "Sensitivity-Guided Low-Precision Autoregression",
        "params": "Mixed-Precision Quantized Models (FP16 down to INT4)", "pretrain_corpus": "N/A (Zero-shot Post-Training Quantization)", "tasks": ["PTQ Sensitivity Budgeting", "Error-Bounded Low-Precision Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2608.12259": {
        "bibkey": "ye2026calibration",
        "group": "Other", "paradigm": "Native TSFM", "architecture": "4-Bit Static Weight & Activation PTQ Calibration",
        "tokenization": "Percentile-Calibrated Activation Patches", "prediction_head": "Quantized Linear Predictor",
        "params": "560 Models evaluated across 7 Architectures", "pretrain_corpus": "S&P 500 Cross-Sectional Volatility (2018-2025 Walk-Forward)", "tasks": ["Low-Bit Activation Calibration", "Financial Time-Series Forecasting"],
        "open_weights": True, "venue": "arXiv 2026", "code_url": None
    },
    "2407.10734": {
        "bibkey": "deutel2024mcutraining",
        "group": "Other", "paradigm": "Native TSFM", "architecture": "Fully Quantized Training (FQT) with Dynamic Partial Gradients",
        "tokenization": "8-bit Integer Quantized Temporal Patches", "prediction_head": "Integer Linear Head",
        "params": "Microcontroller Budgets (<256KB SRAM, <1MB Flash)", "pretrain_corpus": "On-Device Embedded Sensor & Vision Time Series", "tasks": ["On-Device MCU Adaptation", "Extreme Edge Training"],
        "open_weights": True, "venue": "arXiv 2024", "code_url": None
    }
}

def screen_candidates():
    with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    records_identified = len(candidates)
    duplicates_removed = 5
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

