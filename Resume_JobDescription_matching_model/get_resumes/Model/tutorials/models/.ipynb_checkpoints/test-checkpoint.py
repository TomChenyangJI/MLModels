import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from transformers import AdamW
from tqdm import tqdm


# Example dataset (texts and their corresponding labels)
texts = ["I love this product", "Worst purchase ever", "Highly recommend it", "Not worth the money"]
labels = [1, 0, 1, 0]  # 1 for positive, 0 for negative sentiment

train_texts, val_texts, train_lables, val_labels = train_test_split(texts, labels, test_size=0.2)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
# print(tokenizer)
# print(tokenizer.__dict__)
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=1024)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=1024)
print(train_texts)
print(train_encodings)
