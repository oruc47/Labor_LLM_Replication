import json
import math
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "mps" if torch.backends.mps.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("gpt2")

N_EVAL = 400

test_workers = []

with open("data/test.jsonl") as f:
    for line in f:
        test_workers.append(json.loads(line)["worker"])

test_workers = test_workers[:N_EVAL]


def transitions(worker):

    header = "\n".join([
        "<A synthetic worker>",
        f"The following information is available about the work history of a "
        f"{worker['gender']} {worker['ethnicity']} worker residing in the {worker['region']} region.",
        f"The worker was born in {worker['birth_year']}.",
        "The worker has the following records of work experience, one entry per line, including year and the job title:",
    ])

    prior = []
    results = []

    for year, job in worker["career"]:
        context = "\n".join([header] + prior + [f"{year} :"])
        results.append((context, f" {job}"))
        prior.append(f"{year} : {job}")

    return results


def occupation_logp(model, context, title):

    context_ids = tokenizer(context, return_tensors="pt").input_ids.to(device)
    full_ids = tokenizer(context + title, return_tensors="pt").input_ids.to(device)
    n_context = context_ids.shape[1]

    with torch.no_grad():
        logp = F.log_softmax(model(full_ids).logits[0], dim=-1)

    total = 0.0

    for i in range(n_context, full_ids.shape[1]):
        token_id = full_ids[0, i]
        total += logp[i - 1, token_id].item()

    return total


def perplexity(model):

    model.eval()
    total_logp, n = 0.0, 0

    for worker in test_workers:
        for context, title in transitions(worker):
            total_logp += occupation_logp(model, context, title)
            n += 1

    return math.exp(-total_logp / n), n


base_model = AutoModelForCausalLM.from_pretrained("gpt2").to(device)

base_model_perplexity, n = perplexity(base_model)

labor_llm = AutoModelForCausalLM.from_pretrained(
    "model/gpt2-labor-finetuned"
).to(device)

labor_llm_perplexity, _ = perplexity(labor_llm)

n_occ = len(json.load(open("data/meta.json"))["all_jobs"])
print(f"transitions scored          : {n}")
print(f"uniform-guess baseline      : {n_occ:.2f}   ({n_occ} possible occupations)")
print(f"off-the-shelf GPT-2         : {base_model_perplexity:.2f}")
print(f"fine-tuned GPT-2 (yours)    : {labor_llm_perplexity:.2f}")
print(f"\nfine-tuning cut perplexity by {base_model_perplexity / labor_llm_perplexity:.1f}x")
