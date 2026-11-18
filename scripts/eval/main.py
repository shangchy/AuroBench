# -*- coding: utf-8 -*-
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import runner
import scorer
import report


def main():
    print("=== Step 1/3: 生成模型回答 ===")
    runner.run_all()
    print("=== Step 2/3: 规则 + LLM 裁判打分 ===")
    scorer.score_all()
    print("=== Step 3/3: 生成报告 ===")
    report.generate()
    print("ALL DONE")


if __name__ == "__main__":
    main()
