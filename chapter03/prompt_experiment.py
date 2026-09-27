"""第 3 章练习 4：比较零样本、单样本、少样本提示。

先完成三个 TODO，并保持 TEST_TEXT 不变，才方便比较。
默认只预览提示词。确认内容后，将 RUN_API 改为 True 再调用模型。
配置沿用项目根目录的 .env：LLM_API_KEY、LLM_BASE_URL、LLM_MODEL_ID。
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


TEST_TEXT = "这款软件界面很漂亮，但是运行时经常卡顿。"
LABELS = "正面、负面、混合"
RUN_API = True

# 三次实验只改变示例数量。每个提示都要使用相同的标签和待分类文本。
PROMPTS = {
    "零样本": (
        f"请将文本分类。只能从以下标签中选择一个：{LABELS}。\n"
        "只输出标签，不要解释。\n\n"
        f"文本：{TEST_TEXT}\n"
        "标签："
    ),

    "单样本": (
        f"请将文本分类。只能从以下标签中选择一个：{LABELS}。\n"
        "只输出标签，不要解释。\n\n"
        "示例：\n"
        "文本：安装很顺利，操作也很流畅。\n"
        "标签：正面\n\n"
        f"文本：{TEST_TEXT}\n"
        "标签："
    ),

    "少样本": (
        f"请将文本分类。只能从以下标签中选择一个：{LABELS}。\n"
        "只输出标签，不要解释。\n\n"
        "示例：\n"
        "文本：安装很顺利，操作也很流畅。\n"
        "标签：正面\n\n"
        "文本：应用频繁闪退，功能无法使用。\n"
        "标签：负面\n\n"
        "文本：功能齐全，但加载速度很慢。\n"
        "标签：混合\n\n"
        f"文本：{TEST_TEXT}\n"
        "标签："
    ),
}


def call_model(prompt: str, temperature: float = 0) -> str:
    """沿用第一章的 OpenAI 兼容接口调用方式。"""
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(project_root / ".env")

    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model_id = os.getenv("LLM_MODEL_ID")
    if not all((api_key, base_url, model_id)):
        raise RuntimeError("请先在项目根目录的 .env 配置 LLM_API_KEY、LLM_BASE_URL、LLM_MODEL_ID")

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    for name, prompt in PROMPTS.items():
        if not prompt.strip():
            print(f"请先完成{name}提示词的 TODO")
            continue

        print(f"\n--- {name} ---")
        print(f"提示词：\n{prompt}")
        if RUN_API:
            try:
                print(f"模型回答：{call_model(prompt)}")
            except Exception as error:
                print(f"调用失败：{error}")
