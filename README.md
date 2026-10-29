
# Symptom Checker Project - delivered files

Files generated here:
- diseases.json : JSON file mapping ~55 conditions to keywords and response texts
- gradio_app.py : Colab-friendly Gradio app (web interface)
- tkinter_app.py: Desktop Tkinter GUI (for local execution)
- README.md : this file

## How to run in Google Colab (recommended)
1. Upload the `diseases.json` and `gradio_app.py` to your Colab session, or run in this environment.
2. Install dependencies:
   ```bash
   !pip install gradio scikit-learn
   ```
3. Run the Gradio app in a cell:
   ```python
   !python gradio_app.py
   ```
   Gradio will provide a public URL and an in-notebook iframe to interact with the chatbot.

## How to run locally (desktop)
- Tkinter GUI (Windows/Mac/Linux with Python and tkinter available):
  ```bash
  python tkinter_app.py
  ```
- Or run `gradio_app.py` locally after `pip install gradio scikit-learn` and open the local web link.

## Notes
- The system is rule-based by default (fast, interpretable). The Gradio app contains a simple optional ML model (Naive Bayes) trained on synthetic examples created from the keywords — this is for demonstration and not a substitute for clinical diagnosis.
- You can expand `diseases.json` with more keywords or more nuanced responses.
- For production or clinical use you must involve medical professionals and implement robust testing, privacy, and safety checks.
