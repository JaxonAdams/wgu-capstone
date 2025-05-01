import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def plot(y_true, y_proba):

    df = pd.DataFrame({
        'y_true': y_true,
        'y_proba': y_proba,
    })

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df[df['y_true'] == 0], x='y_proba', color='green', label='Paid in Full (0)', bins=50, stat='density', alpha=0.6)
    sns.histplot(data=df[df['y_true'] == 1], x='y_proba', color='red', label='Defaulted (1)', bins=50, stat='density', alpha=0.6)

    plt.title('Distribution of Predicted Probabilities')
    plt.xlabel('Predicted Probability of Default')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("data/visualizations/probability_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()