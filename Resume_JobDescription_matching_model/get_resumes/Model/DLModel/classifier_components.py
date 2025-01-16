import torch
import numpy
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from transformers import AdamW
from tqdm import tqdm



def transfrom_data_from_database(data_from_database, label):
    data = []
    labels: torch.tensor
    for entry in data_from_database:
        cv, overview = entry
        data.append(cv+overview)
    # labels = torch.tensor(label, (len(data), ))
    # labels = numpy.array([int(label)] * len(data))
    labels = [int(label)] * len(data)
    # print(labels)

    return data, labels


class TextDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)