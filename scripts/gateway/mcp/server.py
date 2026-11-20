# -*- coding: utf-8 -*-
import json
import subprocess
import sys

from mcp.server.mcpserver import MCPServer
from openai import OpenAI

LITELLM_BASE = "http://localhost:4000/v1"
LITELLM_KEY = "sk-local-eval"

client = OpenAI(base_url=LITELLM_BASE, api_key=LITELLM_KEY)

server = MCPServer("llm-gateway")


def chat(prompt: str, model: str = "qwen2.5:7b") -> str:
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return r.choices[0].message.content


def list_models() -> str:
    models = [m.id for m in client.models.list().data]
    return json.dumps(models, ensure_ascii=False, indent=2)


def run_eval() -> str:
    result = subprocess.run(
        [sys.executable, "main.py"],
        cwd="../eval",
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout[-2000:] if result.stdout else result.stderr[-2000:]


server.add_tool(chat, name="chat", description="调用模型进行对话生成")
server.add_tool(list_models, name="list_models", description="列出 LiteLLM 网关中可用的模型")
server.add_tool(run_eval, name="run_eval", description="触发脚本评测（scripts/eval）并返回结果摘要")


if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    if transport == "http":
        server.run(transport="streamable-http", host="0.0.0.0", port=8000)
    else:
        server.run(transport="stdio")
