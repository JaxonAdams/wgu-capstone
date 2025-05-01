import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot(pipeline):

    # Extract classifier from pipeline
    rf_model = pipeline.named_steps["classifier"]
    preprocessor = pipeline.named_steps["preprocessor"]

    # Get feature names from preprocessing
    ohe = preprocessor.named_transformers_["cat"].named_steps["encoder"]
    cat_feature_names = ohe.get_feature_names_out(preprocessor.transformers_[1][2])
    num_feature_names = preprocessor.transformers_[0][2]

    # Combine all feature names
    all_feature_names = np.concatenate([num_feature_names, cat_feature_names])

    # Get feature importances
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]

    # Plot
    plt.figure(figsize=(12, 8))
    sns.barplot(x=importances[indices][:20], y=all_feature_names[indices][:20])
    plt.title("Top 20 Feature Importances in Loan Default Prediction")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig("data/visualizations/feature_importance.png", dpi=300)
    plt.close()
