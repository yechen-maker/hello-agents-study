"""第 4 章练习：把模型调用整理成可复用的客户端。

先完成非流式调用，再完成流式调用。只运行此文件不会发起 API 请求。
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


class HelloAgentsLLM:
    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        load_dotenv(project_root / ".env")

        self.model = os.getenv("LLM_MODEL_ID")
        api_key = os.getenv("LLM_API_KEY")
        base_url = os.getenv("LLM_BASE_URL")
        if not all((self.model, api_key, base_url)):
            raise ValueError("请在项目根目录的 .env 配置 LLM_MODEL_ID、LLM_API_KEY 和 LLM_BASE_URL")

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def think(self, messages: list[dict[str, str]]) -> str:
        """非流式：一次收到完整响应，再取出回答文本。"""
        # TODO 1：参考 chapter03/prompt_experiment.py 的 call_model。
        # 调用 self.client.chat.completions.create，传入 self.model、messages，
        # 并设置 stream=False；返回第一条回答的 content（可能为空）。
        response = self.client.chat.completions.create(
            model= self.model,
            messages = messages,
            stream= False
        )
        return response.choices[0].message.content or ""
        # raise NotImplementedError("请先完成 TODO 1")

    def think_stream(self, messages: list[dict[str, str]]) -> str:
        """流式：逐段接收回答，最后拼成一个字符串。"""
        # TODO 2：调用同一接口，但设置 stream=True。
        response = self.client.chat.completions.create(
            model= self.model,
            messages = messages,
            stream= True
        )
        # TODO 3：创建空列表；遍历返回的 chunk，取出每段文字并 append。
        #         注意某些 chunk 没有 choices，或 delta.content 为 None。
        parts = []
        for chunk in response:
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content or ""
            parts.append(content)
        # TODO 4：用 "".join(...) 拼接列表并返回。
        return ''.join(parts)
        # raise NotImplementedError("请先完成 TODO 2～4")
