# -*- coding: utf-8 -*-
import os
import sys

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eval"))
from questions import QUESTIONS

LITELLM_BASE = "http://localhost:4000/v1"
LITELLM_KEY = "sk-local-eval"

MODELS = [
    "qwen2.5:1.5b",
    "qwen2.5:3b",
    "qwen2.5:7b",
    "deepseek-r1:1.5b",
    "llama3.2:3b",
    "gemma2:2b",
    "glm4:9b",
    "seed-coder-8b",
]

providers = [
    {
        "id": f"openai:chat:{m}",
        "config": {"apiBaseUrl": LITELLM_BASE, "apiKey": LITELLM_KEY, "temperature": 0.2},
    }
    for m in MODELS
]

tests = []
for q in QUESTIONS:
    tests.append({
        "vars": {
            "question": q["prompt"],
            "dimension": q["dimension"],
            "hints": "、".join(q.get("hints", [])),
        },
        "assert": [
            {
                "type": "llm-rubric",
                "value": "题目维度：{{dimension}}。参考答案要点：{{hints}}。请判断模型回答是否基本正确，回答基本正确则判为通过。",
            }
        ],
    })

config = {
    "description": "本地 8 模型 × 24 题评测（经 LiteLLM 网关）",
    "providers": providers,
    "prompts": ["{{question}}"],
    "tests": tests,
    "defaultTest": {
        "options": {
            "provider": {
                "id": "openai:chat:qwen2.5:7b",
                "config": {"apiBaseUrl": LITELLM_BASE, "apiKey": LITELLM_KEY},
            },
        }
    },
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "promptfooconfig.yaml")
with open(out, "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, sort_keys=False, width=1000)

print(f"generated {out}, tests={len(tests)}, providers={len(providers)}")
