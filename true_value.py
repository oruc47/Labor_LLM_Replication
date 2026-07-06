

import json
import math
from collections import Counter

meta = json.load(open("data/meta.json"))

T = meta["transitions"]


#what are the odds someone starts their career at job x?
first_counts = Counter()

for line in open("data/train.jsonl"):
    career = json.loads(line)["worker"]["career"]
    first_counts[career[0][1]] += 1

n_first = sum(first_counts.values())


def first_prob(job):
    return first_counts[job] / n_first

def true_prob(prev_job, next_job):
    row = T[prev_job]
    return row.get(next_job, 0.0) / sum(row.values())


total_logp, n = 0.0, 0

for line in open("data/test.jsonl"):
    career = json.loads(line)["worker"]["career"]
    prev = None
    for year, job in career:
        if prev is None:
            p = first_prob(job)
        else:
            p = true_prob(prev, job)

        total_logp += math.log(p)
        n += 1
        prev = job


floor = math.exp(-total_logp / n)

print(f"True model perplexity: {floor}")
