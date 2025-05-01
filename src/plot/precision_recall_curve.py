import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score


def plot(y_true, y_proba):

    # Compute precision-recall curve and average precision
    precision, recall, thresholds = precision_recall_curve(y_true, y_proba)
    avg_precision = average_precision_score(y_true, y_proba)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    plt.plot(recall, precision, color="navy", lw=2, label=f"AP = {avg_precision:.4f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.legend(loc="lower left")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.tight_layout()
    plt.savefig("data/visualizations/precision_recall_curve.png", dpi=300, bbox_inches="tight")
    plt.close()