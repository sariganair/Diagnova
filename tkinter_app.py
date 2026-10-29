
"""
Tkinter desktop Symptom Checker (runs locally)
- Loads diseases.json and uses simple rule-based matching
"""
import json, re, tkinter as tk
from tkinter import scrolledtext, END, messagebox
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / "diseases.json"

with DATA_PATH.open('r', encoding='utf-8') as f:
    items = json.load(f)

def rule_based_response(text):
    text = text.lower()
    matches = []
    for it in items:
        for k in it["keywords"]:
            if re.search(r'\\b' + re.escape(k.lower()) + r'\\b', text):
                matches.append((it['disease'], it['response']))
                break
    if matches:
        primary = matches[0][1]
        others = [m[0] for m in matches[1:]]
        if others:
            primary += "\\nAlso consider: " + ", ".join(others)
        return primary
    return "No confident match. Please consult a doctor or provide more details."

def on_check():
    text = entry.get().strip()
    if not text:
        messagebox.showinfo("Input required", "Please enter symptoms.")
        return
    resp = rule_based_response(text)
    chat.config(state='normal')
    chat.insert(END, "You: " + text + "\\n")
    chat.insert(END, "Bot: " + resp + "\\n\\n")
    chat.config(state='disabled')
    entry.delete(0, END)

root = tk.Tk()
root.title("Symptom Checker")

chat = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20, wrap='word')
chat.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

entry = tk.Entry(root, width=45)
entry.grid(row=1, column=0, padx=10, pady=5)
btn = tk.Button(root, text="Check", command=on_check)
btn.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
