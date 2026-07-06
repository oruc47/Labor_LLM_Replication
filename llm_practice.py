import math

import torch
import torch.nn.functional as F

from transformers import AutoTokenizer as autotk
from transformers import AutoModelForCausalLM as autolm


#set the model name

model_name = "gpt2"

#setting to use gpu if available
device = "mps" if torch.backends.mps.is_available() else "cpu"

#tokenizing is done through the pretrained model that is already set
tokenizer = autotk.from_pretrained(model_name)

model = autolm.from_pretrained(model_name).to(device).eval()


sentence = "The capital of Turkey is"

encoded = tokenizer(sentence, return_tensors="pt").to(device)

token_ids = encoded.input_ids

print("Original sentence vs token ID")
print("Sentence:", sentence)
print("Token IDs:", token_ids.tolist())

#not super important here for now
print("Attention mask:", encoded.attention_mask.tolist())

with torch.no_grad():
    result = model(**encoded)

#note the scores here are logit odds ratio not probabilities
scores = result.logits

print(scores.shape)

print(scores)

#in this sentence, take the score of the last word
last_word_scores = scores[0,-1]

#convert to probability, exp() function
prob = F.softmax(last_word_scores, dim = -1)


#store top 10 results
top10 = torch.topk(prob, 10)

#for each probability and token print out the probability
for p, token in zip(top10.values, top10.indices):
    word = tokenizer.decode(int(token))
    print(f" {word} {p.item():.1%}")


def score_phrase(context, phrase, show=False):

        #tokenize both context and then context with the phrase
        context_ids = tokenizer(context, return_tensors="pt").input_ids.to(device)

        full_ids = tokenizer(context + phrase, return_tensors="pt").input_ids.to(device)


        #number of tokens in the context, number of tokens in the phrase
        n_context = context_ids.shape[1]
        phrase_ids = full_ids[0, n_context:]


        with torch.no_grad():
            logits = model(full_ids).logits[0]

        log_probs = F.log_softmax(logits, dim = -1)

        total = 0.0

        for k, token_id in enumerate(phrase_ids):
            index = n_context + k
            lp = log_probs[index - 1, token_id].item()

            total += lp

            if show:
                print(f" token {tokenizer.decode(int(token_id))}")
                print(f" log-prob {lp}, prob {math.exp(lp)}")

        return total


context = "The capital of Turkey is"
phrase = " located in Asia"

print(f"Scoring {phrase} after {context}")

total_lp = score_phrase(context, phrase, show=True)

print(f" Total log probability {total_lp}, phrase prob. {math.exp(total_lp)}")

candidates = [" Paris", " London", " Hanoi", " Ankara", " Istanbul", " Izmir", " Mardin"]

for c in candidates:
    lp = score_phrase(context, c)
    print(f" {c} prob. {math.exp(lp):.4f}")


#now suppose we have an example worker

example_worker = {

        "gender" : "female",
        "region" : "south",
        "birth_year" : 1985,
        "career" : [
            (2003, "Cashier"),
            (2004, "Cashier"),
            (2005, "Waiter"),
            (2007, "Administrative Assistant"),
            (2009, "Resturant Manager")
            ],
        }


def make_resume(worker):

    lines = []

    lines.append("<A synthetic worker>")

    lines.append(
            f"The following information is available about the work history of a {worker['gender']} worker residing in the {worker['region']} region."
            )

    lines.append(f"The worker was born in {worker['birth_year']}.")

    lines.append("The worker has the following records of work experience, one entry per line, including year and the job title:")

    for year, job_title in worker["career"]:
        lines.append(f"{year} : {job_title}")


    lines.append("<END OF DATA")

    return "\n".join(lines)


print(make_resume(example_worker))
