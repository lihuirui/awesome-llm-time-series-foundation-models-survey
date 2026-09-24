# Project brief: Survey of LLMs and Time Series Foundation Models

- Local folder: `/workspace/survey-llm-tsfm` · GitHub repo: `lihuirui/awesome-llm-time-series-foundation-models-survey`
- Working title: "Large Language Models and Foundation Models for Time Series: A Survey and Outlook"
- Scope, 2021–present: (1) time series foundation models pretrained on large time-series corpora (e.g. Chronos, Chronos-2,
  Chronos-Bolt as repository release, TimesFM, Moirai family, MOMENT, Lag-Llama, TTM, Timer, Timer-XL, Sundial, Timer-S1,
  Time-MoE, Toto, TabPFN-TS, Kairos, YingLong, FlowState and newer); (2) LLM-based time series methods (reprogramming,
  prompting, fine-tuning, tokenisation, LLM-as-reasoner/agent), e.g. Time-LLM, GPT4TS/OFA, LLMTime, TEMPO, TEST, S2IP-LLM;
  (3) evaluations, scaling laws, benchmarks (e.g. GIFT-Eval, fev-bench) and critiques such as "are LLMs actually useful for
  time series". Give special attention to the THUML group (Mingsheng Long, Tsinghua) and Ming Jin's group, and the Chronos family.
- Suggested RQs: pretraining corpora and data curation; architectures (encoder/decoder/enc-dec, MoE, diffusion/flow);
  tokenisation (patching, quantisation, lags); probabilistic outputs; scaling behaviour; zero-shot vs. fine-tuned
  performance; efficiency; when LLM backbones help vs. native TSFMs; evaluation pitfalls (leakage, benchmark overlap).
- Extra figures: model-family genealogy/timeline; reported parameter count vs. release date; pretraining corpus size vs.
  date (only stated values); open-weight share; comparison table of design choices.
