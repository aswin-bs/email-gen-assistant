# Email Generation Assistant

A lightweight LLM-powered assistant that generates professional emails from structured inputs — intent, key facts, and tone. Built as part of an AI Engineer assessment, this project also includes a custom evaluation framework and a side-by-side comparison of two local models.

---

## What This Does

You give it three things:
- **Intent** — what the email is trying to accomplish
- **Key Facts** — bullet points that must appear in the email
- **Tone** — how the email should feel (formal, urgent, casual, etc.)

It generates a well-structured email and then scores it across three custom metrics against a human-written reference.

---

## Project Structure

```
email-gen-assistant/
├── main.py                        # Run this to generate + evaluate everything
├── requirements.txt
├── README.md
│
├── data/
│   ├── test_scenarios.json        # 10 input scenarios (intent, facts, tone)
│   └── reference_emails.json     # Manually written ideal emails for each scenario
│
├── src/
│   ├── generator.py               # Calls Ollama, applies the prompt template
│   ├── evaluator.py               # The 3 custom metrics
│   └── comparator.py              # Runs both models and collects results
│
├── prompts/
│   └── email_prompt_template.txt  # Documents the prompting strategy
│
├── outputs/
│   ├── model_a_results.json
│   ├── model_b_results.json
│   └── evaluation_report.csv      # Final scores for all 10 scenarios x 2 models
│
└── report/
    └── analysis.md                # Comparative analysis write-up
```

---

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed and running locally
- macOS (tested on MacBook Air M4)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/email-gen-assistant.git
cd email-gen-assistant
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Install and start Ollama

If you haven't already:

```bash
brew install ollama
ollama serve
```

Open a new terminal tab and pull the two models used in this project:

```bash
ollama pull llama3.2
ollama pull mistral
```

You can verify they're available with:

```bash
ollama list
```

### 4. Run the project

```bash
python3 main.py
```

This will generate emails for all 10 scenarios using both models, score them, and write the results to `outputs/evaluation_report.csv`.

---

## Prompting Strategy

The assistant uses a combination of **Role-Playing** and **Few-Shot Prompting**.

The model is first given a persona — an experienced business communication specialist — to anchor its output style. It then sees two fully worked examples before being asked to generate a new email. This approach consistently produces emails that are better structured and more tone-accurate than a bare zero-shot prompt.

The full template is documented in `prompts/email_prompt_template.txt`.

---

## Evaluation Metrics

Three custom metrics were designed specifically for this task. Generic NLP metrics like BLEU weren't a good fit here since email quality is partly subjective, so the evaluation combines rule-based, statistical, and LLM-based approaches.

### Metric 1 — Fact Recall Score
Checks what percentage of the provided key facts actually made it into the generated email. Uses keyword matching on meaningful words (length > 4 chars) from each fact bullet. Score range: 0 to 1.

### Metric 2 — Tone Accuracy Score
Uses the model itself as a judge (LLM-as-a-Judge). The model is asked to rate on a scale of 0–10 how well the generated email matches the requested tone. The score is normalized to 0–1. This handles tones like "empathetic" or "urgent" that are hard to measure with rules alone.

### Metric 3 — ROUGE-L Fluency Score
Compares the generated email against the human-written reference using ROUGE-L (longest common subsequence). This captures how closely the structure and flow of the output matches a well-written email, without requiring exact word matches. Score range: 0 to 1.

The final `avg_score` in the CSV is the mean of all three metrics per scenario.

---

## Models Compared

| Model | Type | Notes |
|-------|------|-------|
| `llama3.2` | Meta LLaMA 3.2 3B | Faster, lighter |
| `mistral` | Mistral 7B | Slower, generally better reasoning |

Results and analysis are in `report/analysis.md`.

---

## Output

After running `main.py`, the `outputs/` folder will contain:

- `evaluation_report.csv` — raw scores for all 10 scenarios across both models, with columns: `id`, `model`, `fact_recall`, `tone_accuracy`, `rouge_l`, `avg_score`, `generated`
- `model_a_results.json` and `model_b_results.json` — full generated emails per model

---

## Notes

- The `urllib3` SSL warning on macOS (LibreSSL) is harmless and doesn't affect functionality
- All inference runs locally via Ollama — no API keys or internet connection required after the models are pulled
- Reference emails in `data/reference_emails.json` were written manually to serve as ground truth`