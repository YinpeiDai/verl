import ray
import random
import time
import math
from fractions import Fraction

# Let's start Ray
ray.init()

@ray.remote
def pi4_sample(sample_count):
    """pi4_sample runs sample_count experiments, and returns the 
    fraction of time it was inside the circle. 
    """
    in_count = 0
    for i in range(sample_count):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            in_count += 1
    return Fraction(in_count, sample_count)

SAMPLE_COUNT = 1000 * 1000
start = time.time() 
future = pi4_sample.remote(sample_count = SAMPLE_COUNT)
pi4 = ray.get(future)
end = time.time()
dur = end - start
print(f'Running {SAMPLE_COUNT} tests took {dur} seconds')

pi = pi4 * 4
print(f'Pi is approximately {float(pi)}', abs(pi-math.pi)/pi)

FULL_SAMPLE_COUNT = 1000 * 1000 * 1000  # 100 billion samples! 
BATCHES = int(FULL_SAMPLE_COUNT / SAMPLE_COUNT)
print(f'Doing {BATCHES} batches')
results = []
start = time.time() 
for _ in range(BATCHES):
    results.append(pi4_sample.remote(sample_count = SAMPLE_COUNT))
output = ray.get(results)
end = time.time()
dur = end - start
print(f'Running {FULL_SAMPLE_COUNT} tests took {dur} seconds')

total_in = sum([r.numerator for r in output])
total = sum([r.denominator for r in output])
pi4 = Fraction(total_in, total)
pi = pi4 * 4

print(f'Pi is approximately {float(pi)}', abs(pi-math.pi)/pi)
