# -*- coding: utf-8 -*-
import asyncio

from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI

LITELLM_BASE = "http://localhost:4000/v1"
LITELLM_KEY = "sk-local-eval"


def make_llm(model: str = "qwen2.5:7b") -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        api_key=LITELLM_KEY,
        base_url=LITELLM_BASE,
        temperature=0.2,
    )


async def main():
    agent = Agent(
        task="打开 https://example.com 并告诉我页面标题",
        llm=make_llm("qwen2.5:1.5b"),
        browser=Browser("chromium", headless=True),
    )
    result = await agent.run(max_steps=5)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
