
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "mps" if torch.backends.mps.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("gpt2")

model = AutoModelForCausalLM.from_pretrained("gpt2").to(device)

model.train()

train_text = []



def load_texts(path):
    loaded = []
    for line in open(path):
        loaded.append(json.loads(line)["text"])
    return loaded

train_texts = load_texts("data/train.jsonl")
val_texts = load_texts("data/val.jsonl")


optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)


def average_loss(texts):
    model.eval()
    total = 0.0
    with torch.no_grad():
        for text in texts:
            input_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)
            total += model(input_ids, labels=input_ids).loss.item()
    return total / len(texts)

EPOCHS = 6
PATIENCE = 2


best_value = float("inf")
epochs_without_improvement = 0

for epoch in range(EPOCHS):

    model.train()

    for text in train_texts:
        input_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)
        loss = model(input_ids, labels=input_ids).loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()


    value_loss = average_loss(val_texts)
    print(f"epoch {epoch}: validation loss {value_loss}")

    if value_loss < best_value:
        best_value = value_loss
        model.save_pretrained("model/gpt2-labor-finetuned")
        epochs_without_improvement = 0
    else:
        epochs_without_improvement += 1
        if epochs_without_improvement >= PATIENCE:
            print("Cannot improve further")
            break

print("Training complete.")

