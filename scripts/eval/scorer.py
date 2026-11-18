# -*- coding: utf-8 -*-
import json
import os
import re

import config
import questions
from runner import generate, load_raw

JUDGE_TEMPLATE = """你是一名严格的评测裁判。请根据题目要求和参考答案要点，评估下面模型回答的质量。

【题目】
{prompt}

【参考答案要点】
{hints}

【模型回答】
{answer}

请给出 1 到 5 的整数评分（5=完全正确且优质，4=基本正确，3=部分正确，2=大部分错误，1=完全错误），并附一句简短理由。
请严格按以下格式输出：
分数：<1-5>
理由：<一句话>
"""


def rule_score(q, answer):
    hints = q.get("hints", [])
    if not hints:
        return None
    a = answer.lower()
    hit = sum(1 for h in hints if h.lower() in a)
    return round(hit / len(hints) * 100, 1)


def judge_score(q, answer):
    prompt = JUDGE_TEMPLATE.format(
        prompt=q["prompt"],
        hints="、".join(q.get("hints", [])),
        answer=answer[:1500],
    )
    try:
        text, _ = generate(config.JUDGE_MODEL, prompt, config.JUDGE_PARAMS)
    except Exception as e:
        return 3, f"judge error: {e}"
    m = re.search(r"分数\s*[:：]\s*([1-5])", text)
    if not m:
        m = re.search(r"([1-5])", text)
    score = int(m.group(1)) if m else 3
    return score, text.strip()


def load_scores():
    path = os.path.join(config.RESULTS_DIR, config.SCORE_FILE)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {(s["model"], s["qid"]): s for s in data}


def save_scores(entries):
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    path = os.path.join(config.RESULTS_DIR, config.SCORE_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(list(entries.values()), f, ensure_ascii=False, indent=2)


def score_all():
    raw = load_raw()
    qmap = {q["id"]: q for q in questions.QUESTIONS}
    entries = load_scores()
    for (model, qid), r in raw.items():
        if (model, qid) in entries:
            continue
        q = qmap[qid]
        rule = rule_score(q, r.get("answer", ""))
        judge, reason = judge_score(q, r.get("answer", ""))
        print(f"[SCORE] {model} :: {qid} rule={rule} judge={judge}", flush=True)
        entries[(model, qid)] = {
            "model": model,
            "qid": qid,
            "rule": rule,
            "judge": judge,
            "judge_reason": reason,
        }
        save_scores(entries)
    print("SCORE finished, total:", len(entries))
    return entries
