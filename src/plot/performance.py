import matplotlib.pyplot as plt


def plot(metrics=[], scores=[], colors=[]):

    plt.figure(figsize=(8, 5))
    plt.bar(metrics, scores, color=colors)
    plt.ylim(0, 1)
    plt.title("Model Performance Metrics")
    plt.xlabel("Metric")
    plt.ylabel("Score")
    plt.savefig("data/visualizations/performance.png", dpi=300, bbox_inches="tight")
    plt.close()
