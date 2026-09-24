# Template Analysis: Structural and Methodological Foundations

## 1. Overview of Template Documents

This project builds upon the structural rigor, categorization methodology, and analytical depth of two foundational works by Ming Jin and collaborators:
1. **Primary Template**: Ming Jin et al., *"Large Models for Time Series and Spatio-Temporal Data: A Survey and Outlook"*, arXiv:2310.10196 (ACM Computing Surveys / arXiv v3, 2024–2026).
2. **Secondary Reference**: Ming Jin et al., *"Position: What Can Large Language Models Tell Us about Time Series Analysis"*, ICML 2024 (arXiv:2402.02713).

Both papers were downloaded and analyzed in `template/2310.10196.pdf` and `template/2402.02713.pdf`.

---

## 2. Structural Breakdown of the Primary Template (arXiv:2310.10196)

### 2.1 Section Organization
1. **Introduction**
   - *Motivation*: The shift from narrow, task-specific deep neural networks (e.g., LSTMs, N-BEATS, domain CNNs) to foundation models in temporal data analysis.
   - *Paradigm Shift*: Foundation models trained on diverse time series corpora vs. language models repurposed as cross-modal time series backbones.
   - *Contributions*: Systematic four-dimensional taxonomy, comprehensive coverage of pre-training paradigms and adaptation strategies, empirical critique, and curated repository.
   - *Comparison Table*: Explicit comparison matrix against prior surveys (e.g., distinguishing general deep learning surveys, forecasting-only surveys, and foundation-model surveys).
2. **Background and Preliminaries**
   - *Formal Definitions*: Mathematical formulation of univariate time series $\mathbf{x} \in \mathbb{R}^T$, multivariate time series $\mathbf{X} \in \mathbb{R}^{T \times C}$, patching operators $\mathcal{P}$, masking schemes, and forecasting horizons $H$.
   - *Core Paradigms*: Clear theoretical distinction between Pre-trained Foundation Models (PFMs) trained ab initio and Large Language Models (LLMs) adapted via parameter-efficient fine-tuning (PEFT), reprogramming, or prompting.
3. **Overview and Categorization**
   - Multi-dimensional taxonomy structured across:
     - **Data Modality & Form**: Univariate, multivariate, multi-rate, irregular, spatio-temporal.
     - **Model Architecture & Pretraining**: Autoregressive decoder-only, masked autoencoding encoder, encoder-decoder, mixture-of-experts (MoE), diffusion/flow matching.
     - **Adaptation Methodology**: Direct prompting, token reprogramming, LoRA/PEFT, full fine-tuning, cross-modal alignment.
     - **Scope**: General-purpose foundation models vs. domain-specialized temporal models.
4. **Large Models for Time Series Data (LM4TS)**
   - In-depth bifurcation into:
     - *PFM4TS (Native Time Series Foundation Models)*: Architectures trained from scratch on massive temporal corpora (e.g., Chronos, TimesFM, MOIRAI, MOMENT, Lag-Llama, Timer, Sundial).
     - *LLM4TS (LLM Repurposing / Cross-Modal)*: Reprogramming and cross-attention frameworks leveraging frozen or adapted language weights (e.g., Time-LLM, GPT4TS/OFA, LLMTime, TEMPO, TEST).
5. **Evaluation, Benchmarks, and Resources**
   - Pre-training data repositories (LOTSA, Monash, UCR/UEA, synthetic data generators).
   - Zero-shot vs. fine-tuned evaluation benchmarks (GIFT-Eval, fev-bench).
   - Reproducibility and open-source availability.
6. **Critical Perspectives and Open Challenges**
   - The central question: *"Are LLM backbones truly beneficial for time series, or do native compact models achieve superior accuracy and efficiency?"*
   - Tokenization mismatch, out-of-distribution generalization, data leakage/contamination in benchmark evaluations, computational efficiency, and calibration of uncertainty estimates.
7. **Conclusion and Future Outlook**

---

## 3. Key Methodological Lessons from Position Paper (ICML 2024, arXiv:2402.02713)

Jin et al.'s ICML 2024 position paper highlights critical theoretical and practical considerations:
1. **Modality Incongruity**: Natural language tokens possess discrete semantic and syntactic structures, whereas continuous time series signals are dominated by continuous dynamics, high-frequency noise, and phase shifts.
2. **Reprogramming vs. Native Modeling**: Reprogramming maps continuous temporal patches into the word embedding space of an LLM. While parameter-efficient, freezing 7B+ language parameters to predict scalar sequences incurs massive computational overhead ($10\times$ to $100\times$ slower inference) compared to native TSFMs.
3. **Multimodal Reasoning Opportunities**: Where LLMs excel is not raw numeric autoregression alone, but multimodal context integration: combining scalar metrics with textual reports, external calendars, news, and domain metadata.

---

## 4. Adaptation Strategy for this Survey Project

We adapt the template's structure to our focused scope: **"Large Language Models and Foundation Models for Time Series: A Survey and Outlook"**:

| Template Element | Original Template (arXiv:2310.10196) | Our Adapted Survey Design |
| :--- | :--- | :--- |
| **Scope** | Broad time series + spatio-temporal data | LLMs & Time Series Foundation Models (2021–2026) |
| **Core Distinction** | PFM vs. LLM across TS and Spatio-temporal | Native TSFMs (Chronos, TimesFM, Moirai, Timer, MOMENT) vs. LLM4TS (Time-LLM, GPT4TS, TEMPO) |
| **Taxonomy Dimensions** | Data, Architecture, Scope, Task | Pretraining Data, Tokenization/Embedding, Backbone Architecture, Prediction Head (Point/Probabilistic), Adaptation |
| **Special Focus** | Wide industry review | THUML group (Mingsheng Long), Ming Jin's group, Amazon Chronos family, Salesforce, Google TimesFM |
| **Critical Debate** | Brief mention of LLM utility | Dedicated section on inductive bias, scaling laws, zero-shot transfer, benchmark leakage, and efficiency |
| **Summary Table** | Consolidated landscape table | High-density comparison table with verified parameter counts, tokenizers, corpora, and code links |
| **Figures** | Taxonomy tree, domain distribution | Taxonomy hierarchy, PRISMA flow chart, model timeline/genealogy, parameters vs. corpus size scatter |

---

## 5. Summary Table Design Standards
Following the template:
1. **Model Name & Citation**: Direct formal citation (`\cite{key}`).
2. **Release Date & Venue**: Verified peer-reviewed venue (NeurIPS, ICML, ICLR, KDD) or arXiv preprint date.
3. **Model Paradigm**: Native TSFM vs. LLM-reprogrammed / Adapted.
4. **Base Architecture**: Transformer encoder, decoder-only, encoder-decoder, MoE, SSM/Mamba.
5. **Tokenization / Patching**: Patching length, stride, scalar binning/quantization, lag vectors.
6. **Probabilistic vs. Deterministic**: Quantile loss, GMM/Gaussian head, categorical token distribution, flow/diffusion.
7. **Pretraining Corpus**: Named dataset (LOTSA, Monash, Synthetics, etc.) with explicit sample/token count if stated in paper.
8. **Parameter Count**: Exact parameter counts (e.g., 8M to 1B+), with non-reported values explicitly labeled.
9. **Code & Weights**: Verified GitHub repository URL.
