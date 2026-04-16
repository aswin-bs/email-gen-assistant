import json, pandas as pd
from src.generator import generate_email
from src.evaluator import fact_recall, tone_accuracy, rouge_l_score

scenarios = json.load(open("data/test_scenarios.json"))
references = json.load(open("data/reference_emails.json"))

results = []
for s, ref in zip(scenarios, references):
    for model in ["llama3.2", "mistral"]:
        email = generate_email(s["intent"], s["facts"], s["tone"], model)
        results.append({
            "id": s["id"], "model": model,
            "fact_recall": fact_recall(email, s["facts"]),
            "tone_accuracy": tone_accuracy(email, s["tone"], model),
            "rouge_l": rouge_l_score(email, ref["email"]),
            "generated": email
        })

df = pd.DataFrame(results)
df["avg_score"] = df[["fact_recall","tone_accuracy","rouge_l"]].mean(axis=1)
df.to_csv("outputs/evaluation_report.csv", index=False)
print(df.groupby("model")[["fact_recall","tone_accuracy","rouge_l","avg_score"]].mean())