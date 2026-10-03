# 20 — Math and Number Theory

## Useful built-ins
```python
import math
math.gcd(12, 18)        # 6
math.lcm(4, 6)          # 12
math.isqrt(50)          # 7  (whole-number square root)
math.comb(5, 2)         # 10 (n choose k)
pow(2, 100, 10**9 + 7)  # fast power with modulus
```

## Primes
**Is one prime?** Try dividing by numbers up to √n.
```python
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
```

**All primes up to N** (sieve): cross out multiples of each prime.
```python
def primes_upto(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return [i for i in range(n + 1) if is_p[i]]
```

## Modulo (keeps numbers small)
Big contest answers use `MOD = 10**9 + 7`. Take `% MOD` after each multiply or add.
Division becomes multiplying by the inverse: `pow(a, MOD - 2, MOD)` (MOD is prime).

## Counting
- Arrangements of n items: `n!`
- Choose k from n: `math.comb(n, k)`
- Put n identical balls into k boxes: `comb(n + k - 1, k - 1)`

## Handy formulas
- Sum 1..n = `n * (n + 1) // 2`
- Digit sum: `sum(map(int, str(n)))`
- Divisors: loop i up to √n; both `i` and `n // i` are divisors.

## Mistakes
- `int(n ** 0.5)` can be off by one for big n. Use `math.isqrt`.
- Floats lose precision for big numbers. Keep integers.
- Modulo of negatives in Python is non-negative for positive MOD — convenient, but double check.

## Classic problems
Count Primes, Happy Number, Pow(x, n), Unique Paths (combinations), Fraction to Recurring Decimal, Excel Sheet Column Number.
