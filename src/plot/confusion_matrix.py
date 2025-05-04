import seaborn as sns
import matplotlib.pyplot as plt


def plot(confusion_matrix):

    plt.figure(figsize=(6, 5))
    sns.heatmap(
        confusion_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Pred: 0", "Pred: 1"],
        yticklabels=["True: 0", "True: 1"],
    )
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.savefig("data/visualizations/confusion_matrix.png", dpi=300, bbox_inches="tight")
    plt.close()