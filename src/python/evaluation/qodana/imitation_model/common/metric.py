import torch
from sklearn.metrics import multilabel_confusion_matrix
from src.python.evaluation.qodana.imitation_model.common.util import MeasurerArgument


class Measurer:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def get_f1_score(self, predictions: torch.tensor, targets: torch.tensor) -> float:
        confusion_matrix = multilabel_confusion_matrix(targets, predictions)
        false_positives = sum(score[0][1] for score in confusion_matrix)
        false_negatives = sum(score[1][0] for score in confusion_matrix)
        true_positives = sum(score[1][1] for score in confusion_matrix)
        f1_score = true_positives / (true_positives + 1 / 2 * (false_positives + false_negatives))
        return f1_score

    def compute_metric(self, evaluation_predictions: torch.tensor) -> dict:
        logits, targets = evaluation_predictions
        prediction_probabilities = torch.from_numpy(logits).sigmoid()
        predictions = torch.where(prediction_probabilities > self.threshold, 1, 0)
        return {MeasurerArgument.F1_SCORE.value: self.get_f1_score(predictions, torch.tensor(targets))}
