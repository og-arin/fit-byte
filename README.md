<div align="center">

# 🏋️ FitByte
### Personalized AI Fitness Coach

*Your goals. Your food. Your plan.*

[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-00A67E?style=flat-square&logo=groq)](https://console.groq.com)
[![Gradio](https://img.shields.io/badge/Gradio-4.x-FF7C00?style=flat-square)](https://gradio.app)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/og-arin/Fit-Byte)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)

**[▶ Live Demo](https://huggingface.co/spaces/og-arin/Fit-Byte)** · **[📓 Colab Notebook](https://colab.research.google.com/drive/1YhrXE1EH7baCCjFFzDOUPWhPmlsXhZ4h?usp=sharing)**

</div>

---

## What it does

FitByte takes your personal details — weight, height, goal, cuisine, daily schedule — and generates a fully personalized **workout + meal plan** in seconds. No generic advice. No "eat chicken and broccoli" nonsense.

---

## Features

```
🧮  BMI Calculator         WHO classification built-in
🤖  4 Coaching Modes       Motivational · Scientific · Buddy · Drill Sergeant
🍽️  Cuisine-aware meals    Indian, South Indian, Mediterranean, and more
💪  Body condition input   Skinny / Skinny-Fat / Average / Overweight / Muscular
⏱️  Time-aware plans       Set your workout days + daily duration
💾  Download your plan     Export as .txt in one click
🔒  Secure API handling    Colab Secrets + HF Secrets — never hardcoded
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Groq API — LLaMA 3.3 70B Versatile |
| UI | Gradio `gr.Blocks` |
| Deployment | Hugging Face Spaces |
| Dev Environment | Google Colab |

---

## Run locally

```bash
git clone https://github.com/og-arin/fitbyte
cd fitbyte
pip install gradio groq
export GROQ_API_KEY=your_key_here
python app.py
```

## Run on Colab

1. Open the [Colab notebook](https://colab.research.google.com/drive/1YhrXE1EH7baCCjFFzDOUPWhPmlsXhZ4h?usp=sharing)
2. Add `GROQ_API_KEY` to Colab Secrets (🔑 icon in left panel)
3. Run all cells

---

## How it works

```
User Input → Validate → Calculate BMI
                              ↓
                    build_system_prompt()   ← coaching mode
                              ↓
                    build_user_prompt()     ← all user data
                              ↓
                       Groq API call
                              ↓
                    Gradio Output + Download
```

---

<div align="center">
<sub>Built for ADYPU LLM Practicals · Powered by Groq · Deployed on HuggingFace</sub>
</div>
