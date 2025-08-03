# 🧪 Project: Lightweight Fine-Tuning of a Foundation Model

---

## 📘 Overview

This project demonstrates how to fine-tune a pre-trained Transformer model for sentiment analysis using **Parameter-Efficient Fine-Tuning (PEFT)**, specifically **LoRA (Low-Rank Adaptation)**. The main goal is to adapt a foundation model to a downstream task with minimal trainable parameters, reducing resource usage while maintaining strong performance.

---

## 🧠 Key Components

* **PEFT Technique:** LoRA
* **Base Model:** `DistilBERT` (from Hugging Face)
* **Task:** Binary sentiment classification
* **Dataset:** IMDb Movie Reviews
* **Metrics:**

  * Accuracy (primary)
  * Loss (for overfitting tracking)
  * Evaluation speed (samples/sec, steps/sec)

---

## 📦 Dataset

**IMDb Reviews**
A classic NLP benchmark containing 50k movie reviews split evenly into positive and negative classes.

* Source: Hugging Face `datasets` library
* Pre-split into `train` and `test`
* Preprocessed using Hugging Face tokenizers

---

## 🔧 Workflow Steps

1. **Set Up Environment**

   * Use Python 3.10
   * Create and activate a virtual environment

2. **Install Dependencies**

   * Core libraries: `transformers`, `datasets`, `peft`, `accelerate`, `evaluate`, `scikit-learn`, `torch`

3. **Load Base Model**

   * Use `DistilBertForSequenceClassification` and its tokenizer

4. **Tokenize and Prepare Dataset**

   * Truncate and pad sequences
   * Use DataLoader-compatible datasets

5. **Evaluate Base Model**

   * Run inference to collect baseline metrics

6. **Apply LoRA (via PEFT)**

   * Freeze most layers and inject LoRA adapters

7. **Train and Evaluate**

   * Use Hugging Face's `Trainer` API
   * Monitor metrics like accuracy, loss, and training speed

8. **Compare Results**

   * Highlight performance gains vs. resource savings

---

## ⚙️ Installation

### ✅ Virtual Environment (Recommended)

```bash
python -m venv genai
source genai/bin/activate      # For MacOS/Linux
.\genai\Scripts\activate       # For Windows
```

### ✅ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, you can install directly:

```bash
pip install transformers datasets peft accelerate evaluate scikit-learn torch
```

---

## 🚀 Running the Notebook

1. Open the notebook in Jupyter or Colab.
2. Execute each cell sequentially.
3. Observe and record baseline and fine-tuned performance metrics.

---

## 📊 Example Results

| Metric           | Base Model | Fine-Tuned (LoRA) |
| ---------------- | ---------- | ----------------- |
| Accuracy (Dev)   | \~         | \~                |
| Trainable Params | 100%       | \~0.2%            |
| Training Time    | Moderate   | Faster            |

> 📌 You’ll need to run the notebook to populate the actual numbers.

---

## 💡 Why LoRA?

Traditional fine-tuning updates **all** parameters of a model, which is expensive. LoRA inserts small, trainable matrices into the model's architecture, enabling efficient adaptation by updating **only a small fraction** of the parameters.

---

## 📁 Files

* `LightweightFineTuning.ipynb`: Main notebook with code and explanations
* `requirements.txt`: Package dependencies 




