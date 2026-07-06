This is a pseudo-replication for Labor LLM. Paper can be found here: https://arxiv.org/abs/2406.17972.

The goal here is not to replicate the entire paper, but rather build a very lightweight version of it using synthetic data. I do this replication using GPT-2 as it is a more light-weight model that can be trained on a local machine. 

**Note**: This assumes that you have an understanding of Python, virtual environments, etc. 

Before getting started it will be helpful to create a [HuggingFace](https://huggingface.co/) account to log in. When you activate the virtual environment make sure to run in terminal:

`hf auth login`

This will then prompt either a web login or ask you to paste your access code. 
## Getting Started 

I first start with [llm_practice.py](llm_practice.py). This file is helpful for understanding the general workflow with initializing models and working with them. 

A couple of notes: 

```python
device = "mps" if torch.backends.mps.is_available() else "cpu"
```

This line is useful for Mac to train the model using the GPU when available. This may not be needed if running on a server or Windows. 

The example that [llm_practice.py](llm_practice.py) goes through is a simple one. I give the model the sentence "The capital of Turkey is" and then look at the probabilities of the next word. After all, the LaborLLM looks at the career history and then predicts the next job. 

The tokenizer turns each of the words into tokens (integer IDs that represent each word). When you run the code you will see each word and its token number. 

`with torch.no_grad()` is a commonly used syntax in LLM work. All this command does is help us do things with the model, without allowing for the model to update its gradient. For example, if we need to evaluate a model we call this so we get only the model's answer without letting the model update itself. 

In this type of work, log probabilities are preferred. The reasoning is very simple. Let's say we have a sequence of career transitions (A, B, C). And assume that the probability of starting your job at A is 0.5, transition to B has a probability of 0.4 and transitioning to C has a probability of 0.5. The likelihood someone is at career C is then 0.5 * 0.4 * 0.5 which is 0.1. In this three job example it works fine, but imagine a much longer sequence. The probability would convert to 0 and not be human readable. As a result we do log() so we can sum the probabilities and avoid this problem. 

We then look at the next 10 words with the highest probability. In this example, you may be surprised (or not surprised) to see that the first 9 words are stopwords such as "the", "is", or "a". Istanbul is mentioned at rank 10, and Istanbul is not even the correct answer! This is because this is the base model so it is outputting probabilities based on words that appear close to the other words in the sentence from the training corpus. 

This is to get a sense of how to tokenize words and how the LLM scores predictions. In practice, leaving the prediction to be the full set of potential words is not really useful. First, there is the obvious problem of having too large a set to choose from. Second, some job titles are multiple words i.e. Software Engineer. Predicting only the next word is not useful in this context. 

The next part of this file then goes into how to score phrases and how the model will evaluate what we give it, rather than it generating something on its own. This is actually the crux of how we use the model to make predictions. 

In this simple example, we want to see what probability the model gives to "located in Asia" after the context of "The capital of Turkey is". The score phrase function takes in context and phrase as arguments and does the following: 

1. Tokenize only the context ("The capital of Turkey is" )
2. Tokenize the full sentence ("The capital of Turkey is located in Asia")
3. Store the number of tokens in the context (In this case 5)
4. Store the number of tokens in the phrase (In 3)
5. Without optimizing the gradients get the probabilities of each word in the full sentence appearing in that order
6. While iterating through only the phrase tokens ("located in Asia") get the probability of each word coming and sum them. Return the total. 

Super reduced example, imagine ["The", "capital", "of", "Turkey", "is", "located", "in", "Asia"] all have probabilities of 0.5 of being in that order. The iterating step 6 sums the log-probabilities: ln(0.5) is about -0.69 for located, then -0.69 for in and -0.69 for Asia, so the log-probability of the entire phrase "located in Asia" appearing after the context is about -2.08, which e^-2.08 is about 0.125. So we can then evaluate the phrase as having roughly a 12.5% chance of appearing. 

This simple idea is what the rest of the training is done through. 

## Generating Synthetic Data

This section goes over how the synthetic data was generated. This step can be skipped if the focus is only LLM fine tuning. 

[generate_data.py](generate_data.py) creates fake work histories for 5000 workers (the number can be increased if needed). The sectors and jobs in each sector were generated using Claude Opus 4.8. Following the article I also define the special states for education, unemployment and not in labor force. 

I use the distribution of demographics used in their paper. The transition probabilities (staying vs moving within sector vs moving to other sector vs non employment) I had Claude Opus 4.8 create. These numbers are actually not super important, and actually serve more as an answer key of the true transition probabilities where we can compare the calibrated model and the true model. The rest of the code is straightforward, nothing fancy just generating the .json files. 

## Fine Tuning

[finetune.py](finetune.py) starts with the same basic structure. I initialize the models, and then load the training and validation sets. The validation set makes up 10% of the data. It acts like a practice exam before the testing set and allows us to determine how many epochs we train the data for. When there is no improvement in the validation set, we know we can stop the training. 

I also initialize the optimizer which is AdamW in this case. It is a widely used deep learning optimizer. For each epoch we begin training the model. We tokenize the texts and pass them through the model. We then keep track of the loss, and optimize accordingly. We reset the gradient after each resume. We do this until there is no improvement on the validation set. (Patience sets the number of epochs we are willing to go over even if there is no improvement). 

## Evaluation 

I use perplexity to evaluate the model (similar to the paper). Perplexity simply defined is how many words on average the model is choosing from when predicting the next word. A lower perplexity means the model is choosing between fewer words and therefore more confident. 
For example, base GPT-2 has a perplexity of about 6700 words it could be choosing from. Whereas the fine-tuned version has 10.46. A significant improvement. 

### True Value Analysis 

Since the data was synthetically generated, I have access to the true transition probabilities for the work histories (unlike the real PSID data where we do not know the true probabilities) so I can check how my fine tuned model compares. The true model perplexity is about 9, meaning even with knowing the true transition probabilities, the true model can only get as good as picking between 9 words. 
