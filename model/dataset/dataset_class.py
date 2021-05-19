import torch


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        if type(labels) != list:
            labels = labels['emotion'].tolist()
        self.examples = []
        for inputs, att_mask, label in zip(encodings['input_ids'], encodings['attention_mask'], labels):
            self.examples.append({
                'input_ids': torch.tensor(inputs),
                'attention_mask': torch.tensor(att_mask),
                'labels': torch.tensor(label),
            })

    def __getitem__(self, idx):
        return self.examples[idx]

    def __len__(self):
        return len(self.examples)
