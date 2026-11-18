# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

OLLAMA_URL = "http://localhost:11434"
TIMEOUT = 900

AUTO_DISCOVER_MODELS = True

EXCLUDE_KEYWORDS = ["embedding", "embed"]

CANDIDATE_MODELS = [
    "qwen2.5:1.5b",
    "qwen2.5:3b",
    "deepseek-r1:1.5b",
    "qwen2.5:7b",
    "llama3.2:3b",
    "gemma2:2b",
]

JUDGE_MODEL = "qwen2.5:7b"

GEN_PARAMS = {
    "temperature": 0.2,
    "top_p": 0.9,
    "num_predict": 384,
}

JUDGE_PARAMS = {
    "temperature": 0.0,
    "num_predict": 128,
}

RAW_FILE = "raw_results.json"
SCORE_FILE = "scores.json"
REPORT_FILE = "report.md"
CSV_FILE = "report.csv"
