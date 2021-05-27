import torch


class Metrics:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def get_accuracy(self, y_pred, y_true, sigmoid=True):
        y_pred = torch.from_numpy(y_pred)
        y_true = torch.from_numpy(y_true)
        if sigmoid:
            y_pred = y_pred.sigmoid()
        return ((y_pred > self.threshold) == y_true.bool()).float().mean().item()

    def compute_metrics(self, eval_pred):
        predictions, labels = eval_pred
        return {'accuracy': self.get_accuracy(predictions, labels)}
