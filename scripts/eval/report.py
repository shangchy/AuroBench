# -*- coding: utf-8 -*-
import csv
import os

import config
import questions
from scorer import load_scores

JUDGE_SCALE = 20


def total_score(rule, judge):
    if rule is None:
        return judge * JUDGE_SCALE
    return round(0.5 * rule + 0.5 * judge * JUDGE_SCALE, 1)


def build_report():
    scores = load_scores()
    qmap = {q["id"]: q for q in questions.QUESTIONS}

    rows = []
    for (model, qid), s in scores.items():
        q = qmap[qid]
        total = total_score(s["rule"], s["judge"])
        rows.append({
            "model": model,
            "dimension": q["dimension"],
            "qid": qid,
            "rule": s["rule"],
            "judge": s["judge"],
            "total": total,
            "elapsed": None,
        })

    elapsed_map = {}
    raw = os.path.join(config.RESULTS_DIR, config.RAW_FILE)
    if os.path.exists(raw):
        import json
        with open(raw, "r", encoding="utf-8") as f:
            for r in json.load(f):
                elapsed_map[(r["model"], r["qid"])] = r.get("elapsed")
    for row in rows:
        row["elapsed"] = elapsed_map.get((row["model"], row["qid"]))

    return rows


def agg_by_dimension(rows):
    dims = {}
    for r in rows:
        dims.setdefault(r["dimension"], []).append(r["total"])
    return {d: round(sum(v) / len(v), 1) for d, v in dims.items()}


def agg_by_model(rows):
    models = {}
    for r in rows:
        models.setdefault(r["model"], []).append(r["total"])
    ranked = sorted(models.items(), key=lambda kv: -sum(kv[1]) / len(kv[1]))
    return [(m, round(sum(v) / len(v), 1)) for m, v in ranked]


def write_markdown(rows, path):
    dim_avg = agg_by_dimension(rows)
    model_rank = agg_by_model(rows)
    lines = []
    lines.append("# 中国制 LLM 初步功能验证报告")
    lines.append("")
    lines.append("## 一、总体排名（平均综合分）")
    lines.append("")
    lines.append("| 排名 | 模型 | 平均综合分 |")
    lines.append("|------|------|-----------|")
    for i, (m, s) in enumerate(model_rank, 1):
        lines.append(f"| {i} | {m} | {s} |")
    lines.append("")
    lines.append("## 二、分维度平均分")
    lines.append("")
    lines.append("| 维度 | 平均综合分 |")
    lines.append("|------|-----------|")
    for d in questions.DIMENSIONS:
        lines.append(f"| {questions.DIMENSION_NAMES[d]} | {dim_avg.get(d, '-')} |")
    lines.append("")
    lines.append("## 三、分维度 × 模型 综合分")
    lines.append("")
    header = "| 模型 | " + " | ".join(questions.DIMENSION_NAMES[d] for d in questions.DIMENSIONS) + " | 平均 |"
    lines.append(header)
    lines.append("|" + "------|" * (len(questions.DIMENSIONS) + 2))
    for m, _ in model_rank:
        cells = [m]
        for d in questions.DIMENSIONS:
            vals = [r["total"] for r in rows if r["model"] == m and r["dimension"] == d]
            cells.append(str(round(sum(vals) / len(vals), 1)) if vals else "-")
        avg = round(sum(r["total"] for r in rows if r["model"] == m) / len([r for r in rows if r["model"] == m]), 1)
        cells.append(str(avg))
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## 四、逐题明细")
    lines.append("")
    lines.append("| 维度 | 题号 | 模型 | 规则分 | 裁判分(1-5) | 综合分 | 耗时(s) |")
    lines.append("|------|------|------|--------|------------|--------|---------|")
    for r in rows:
        lines.append(
            f"| {questions.DIMENSION_NAMES[r['dimension']]} | {r['qid']} | {r['model']} "
            f"| {r['rule']} | {r['judge']} | {r['total']} | {r['elapsed']} |"
        )
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def write_csv(rows, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "dimension", "qid", "rule", "judge", "total", "elapsed"])
        for r in rows:
            w.writerow([r["model"], r["dimension"], r["qid"], r["rule"], r["judge"], r["total"], r["elapsed"]])
    return path


def generate():
    rows = build_report()
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    md = write_markdown(rows, os.path.join(config.RESULTS_DIR, config.REPORT_FILE))
    csv_path = write_csv(rows, os.path.join(config.RESULTS_DIR, config.CSV_FILE))
    print("report written:", md)
    print("csv written:", csv_path)
