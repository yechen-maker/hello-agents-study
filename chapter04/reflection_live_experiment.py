"""真实模型实验：生成初稿、反思反馈、修订稿；不执行生成的代码。

使用 --resume 可从已成功生成的初稿继续，避免临时 503 后重复生成。
"""

import sys

from openai import APIStatusError

from llm_client import HelloAgentsLLM


RESUME_INITIAL = """def find_primes(n: int) -> list[int]:
    if n < 2:
        return []
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for d in range(2, int(num**0.5) + 1):
            if num % d == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes"""


def ask(llm: HelloAgentsLLM, prompt: str) -> str:
    return llm.think([{"role": "user", "content": prompt}])


def main() -> None:
    llm = HelloAgentsLLM()
    llm.client = llm.client.with_options(timeout=40, max_retries=0)
    task = (
        "实现 find_primes(n: int) -> list[int]：返回 2 到 n（含）的所有素数；"
        "n < 2 时返回空列表。"
    )

    if "--resume" in sys.argv:
        initial = RESUME_INITIAL
    else:
        initial = ask(
            llm,
            f"{task}\n先写一个清晰、正确的基础版本，使用逐个候选数试除。"
            "只输出 Python 函数代码，不要解释，不要 Markdown 代码围栏。",
        )
    print("\n=== 初稿代码 ===\n", initial, flush=True)

    feedback = ask(
        llm,
        f"原始任务：{task}\n初稿代码：\n{initial}\n"
        "请作为代码评审员检查边界条件和算法效率；如果有更快的算法，"
        "给出具体建议。不要编写修订代码。",
    )
    print("\n=== 反思反馈 ===\n", feedback, flush=True)

    refined = ask(
        llm,
        f"原始任务：{task}\n初稿代码：\n{initial}\n评审反馈：\n{feedback}\n"
        "请按反馈给出修订后的完整 Python 函数，保持函数签名和输出约定。"
        "只输出代码，不要解释，不要 Markdown 代码围栏。",
    )
    print("\n=== 修订稿代码 ===\n", refined, flush=True)


if __name__ == "__main__":
    try:
        main()
    except APIStatusError as error:
        if error.status_code == 503:
            raise SystemExit("模型服务暂时繁忙（503）；可稍后使用 --resume 从初稿继续。") from None
        raise
