# -*- coding: utf-8 -*-
import json
import os
import re
import time

import requests

import config
import questions


def clean_response(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()


def generate(model, prompt, params):
    url = config.OLLAMA_URL + "/api/generate"
    payload = dict(params)
    payload["model"] = model
    payload["prompt"] = prompt
    payload["stream"] = False
    if "r1" in model:
        payload["think"] = False
    t0 = time.time()
    resp = requests.post(url, json=payload, timeout=config.TIMEOUT)
    if resp.status_code >= 400 and "r1" in model:
        payload.pop("think", None)
        resp = requests.post(url, json=payload, timeout=config.TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    elapsed = time.time() - t0
    return clean_response(data.get("response", "")), elapsed


def discover_models():
    resp = requests.get(config.OLLAMA_URL + "/api/tags", timeout=30)
    resp.raise_for_status()
    names = [m["name"] for m in resp.json().get("models", [])]
    return [n for n in names if not any(k in n.lower() for k in config.EXCLUDE_KEYWORDS)]


def get_candidate_models():
    if config.AUTO_DISCOVER_MODELS:
        return discover_models()
    return list(config.CANDIDATE_MODELS)


def load_raw():
    raw_path = os.path.join(config.RESULTS_DIR, config.RAW_FILE)
    if not os.path.exists(raw_path):
        return {}
    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {(r["model"], r["qid"]): r for r in data}


def save_raw(entries):
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    raw_path = os.path.join(config.RESULTS_DIR, config.RAW_FILE)
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(list(entries.values()), f, ensure_ascii=False, indent=2)


def run_all():
    entries = load_raw()
    models = get_candidate_models()
    print("Candidate models:", models)
    for model in models:
        for q in questions.QUESTIONS:
            key = (model, q["id"])
            if key in entries and not entries[key].get("error"):
                continue
            print(f"[RUN] {model} :: {q['id']}", flush=True)
            try:
                text, elapsed = generate(model, q["prompt"], config.GEN_PARAMS)
                entries[key] = {
                    "model": model,
                    "qid": q["id"],
                    "answer": text,
                    "elapsed": round(elapsed, 2),
                }
            except Exception as e:
                entries[key] = {
                    "model": model,
                    "qid": q["id"],
                    "answer": "",
                    "elapsed": 0,
                    "error": str(e),
                }
            save_raw(entries)
    print("RUN finished, total:", len(entries))
    return entries
