"""真实模型实验的初稿，已人工审阅后保存，用于本地验证。"""


def find_primes(n: int) -> list[int]:
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
    return primes
