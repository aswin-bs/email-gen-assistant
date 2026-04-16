from rouge_score import rouge_scorer
import requests, json

def fact_recall(generated_email, facts):
    hits = sum(1 for f in facts if any(word.lower() in generated_email.lower() 
               for word in f.split() if len(word) > 4))
    return round(hits / len(facts), 2)

def tone_accuracy(generated_email, tone, model="llama3.2"):
    judge_prompt = f"""Rate how well this email matches the tone '{tone}' on a scale of 0 to 10.
    Reply with ONLY a number between 0 and 10.
    Email: {generated_email}"""
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": model, "prompt": judge_prompt, "stream": False
    })
    try:
        return float(r.json()["response"].strip().split()[0]) / 10
    except:
        return 0.5

def rouge_l_score(generated_email, reference_email):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(reference_email, generated_email)
    return round(scores['rougeL'].fmeasure, 2)