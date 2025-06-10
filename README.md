# GPT Place‑Value Study

This repository accompanies the AIED 2023 workshop paper **“[Does ChatGPT Comprehend Place Value in Numbers When Solving Math Word Problems?](https://www.scopus.com/record/display.uri?eid=2-s2.0-85174938474&origin=inward&txGid=c56fe2a845291e125240d7e2364f33fc)”**. It contains all code, data, and cached results needed to reproduce the experiments exploring how GPT‑class models handle place‑value information in numerals.

## 📑 Paper in a Nutshell

|                  | **Goal**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Problem**      | Even strong language models often stumble on arithmetic with large numbers. We investigate **whether this is due to incomplete understanding of *place value*** – the idea that the digit “5” means different amounts in 5, 50, 500…                                                                                                                                                                                                                                                  |
| **Approach**     | Two controlled experiments using *gpt‑3.5‑turbo*:  <br>1. **Multiplet Ordering (Experiment 1)** – order sets of digits and their permutations to test explicit vs. implicit place‑value reasoning.  <br>2. **English ↔ Numeric Expressions (Experiment 2)** – swap numerals for English words inside Chain‑of‑Thought (CoT) and Program‑of‑Thought (PoT) prompts when solving SVAMP math‑word problems. |
| **Key Findings** | • Ordering accuracy drops sharply from **96.8 %** on single‑token numbers to **60.5 %** when place value must be inferred across multiple tokens.  <br>• Re‑expressing numbers in English improves math problem solving (CoT +3.1 pp, PoT +2 pp).                                                                                                                                                                                                                                              |
| **Implication**  | Current tokenisation fragments place‑value structure. Better prompts or fine‑tuning that restore this information could boost LLM numeracy.                                                                                                                                                                                                                                                                                                                                               |

## 🗂️ Repository Layout

```
├── data/                 # ⭢ generated test sets & SVAMP subset
│   ├── SVAMP.json        #   • base dataset
│   └── SVAMP_scaled_*    #   • scaled numbers for stress tests
├── datasets/             # dataset loader module
├── results/              # cached model outputs and metrics
├── core.py               # prompt templates and evaluation logic
├── main.py               # example script to reproduce results
├── util.py               # helper functions
└── test_util.py          # unit tests for util
```

### Dataset Format

Each entry in `data/SVAMP.json` is a small math word problem with fields like:

```
{
    "ID": "chal-1",
    "Body": "Each pack of dvds costs 76 dollars. If there is a discount of 25 dollars on each pack",
    "Question": "How much do you have to pay to buy each pack?",
    "Equation": "( 76.0 - 25.0 )",
    "Answer": 51.0,
    "Type": "Subtraction"
}
```

Scaled versions (`SVAMP_scaled_*.json`) contain the same questions with larger numbers to stress‑test the models.

## 🚀 Quick Start

1. Install the dependencies (Python ≥ 3.9).
   ```bash
   pip install -r requirements.txt
   ```
2. Export your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=<your-key>
   ```
3. Run the example script to evaluate a model:
   ```bash
   python main.py
   ```
   Results appear in the `results/` directory.

## 📊 Main Results

| Setting           | Accuracy   | Accuracy (Self‑Consistency) |
| ----------------- | ---------- | --------------------------- |
| **CoT – Numeric** | 76.8 %     | 81.2 %                      |
| **CoT – English** | **79.9 %** | **82.5 %**                  |
| **PoT – Numeric** | 80.0 %     | 82.6 %                      |
| **PoT – English** | **82.0 %** | **83.7 %**                  |

*Multiplet Ordering (Exp 1)*: accuracy falls from **96.8 %** (source) → **60.5 %** (permutation) when place value must be inferred.

## 🛠️ Requirements

* Python ≥ 3.9
* `openai`, `tiktoken`, `sympy`, `pandas`, `numpy`, `matplotlib`, `tqdm`

See `requirements.txt` for exact versions. GPU is **not** required because the calls go to the OpenAI API.

## 🔄 Extending the Benchmark

* **Try a new model** – set `--model` in `main.py` to any endpoint such as `gpt-4o`.
* **Stress-test bigger numbers** – use one of the `SVAMP_scaled_*` files or create your own via `scale_up_dataset.py`.
* **Add your dataset** – drop a JSON file with the same format into `data/` and modify `datasets/dataset.py` accordingly.

Pull requests are welcome!

## 🖋️ License

This project is released under the MIT License. See `LICENSE` for details.

