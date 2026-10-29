
"""
Gradio-based Symptom Checker (Colab-friendly)
- Loads diseases.json that maps keywords to responses
- Two modes: rule-based matching (default) and simple ML (Naive Bayes trained on synthetic phrases)
"""
import json, random, re, os
from pathlib import Path

# If running in Colab, install dependencies: !pip install gradio scikit-learn
try:
    import gradio as gr
except Exception as e:
    raise RuntimeError("Please install gradio: pip install gradio") from e

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / "diseases.json"

with DATA_PATH.open('r', encoding='utf-8') as f:
    items = json.load(f)

# Build lookup for rule-based
lookup = []
for it in items:
    lookup.append((it["disease"], [k.lower() for k in it["keywords"]], it["response"]))

def rule_based_response(text):
    text = text.lower()
    matches = []
    for disease, keys, resp in lookup:
        for k in keys:
            # exact word match or phrase in text
            if re.search(r'\\b' + re.escape(k) + r'\\b', text):
                matches.append((disease, resp))
                break
    if matches:
        # return top match (first found) and list alternatives
        primary = matches[0][1]
        others = [m[0] for m in matches[1:]]
        note = ""
        if others:
            note = "\\nAlso consider: " + ", ".join(others)
        return primary + note
    return "I couldn't confidently match the symptoms. Consider consulting a doctor or providing more details."

# Create synthetic dataset for simple ML (one-liners using keywords)
X = []
y = []
for it in items:
    for kw in it["keywords"]:
        X.append(f"I have {kw}")
        y.append(it["disease"])
        X.append(f"{kw} and fever")
        y.append(it["disease"])
        X.append(f"{kw} since yesterday")
        y.append(it["disease"])
# Train a small Naive Bayes classifier
vectorizer = CountVectorizer()
try:
    clf = make_pipeline(vectorizer, MultinomialNB())
    clf.fit(X, y)
    ml_ready = True
except Exception:
    clf = None
    ml_ready = False

def get_response(text, mode="Rule-based"):
    text = text.strip()
    if not text:
        return "Please enter symptoms."
    if mode == "Rule-based":
        return rule_based_response(text)
    else:
        if ml_ready:
            pred = clf.predict([text])[0]
            # fetch response for predicted disease
            for d in items:
                if d["disease"] == pred:
                    return f"(ML) {d['response']} (predicted: {pred})"
            return "(ML) I predicted: " + pred
        else:
            return "ML model not available."

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🩺 Symptom Checker (Rule-based + Optional ML)")
    with gr.Row():
        inp = gr.Textbox(lines=2, placeholder="Enter symptoms (e.g. 'fever, sore throat')")
        mode = gr.Radio(["Rule-based", "ML"], value="Rule-based", label="Mode")
    out = gr.Textbox(label="Suggestion")
    btn = gr.Button("Check")
    btn.click(fn=lambda t,m: get_response(t,m), inputs=[inp, mode], outputs=out)

if __name__ == '__main__':
    demo.launch()
