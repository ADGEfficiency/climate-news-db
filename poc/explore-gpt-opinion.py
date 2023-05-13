import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scrapy.settings import Settings

from climatedb import database

settings = Settings()
settings.setmodule("climatedb.settings")


def bootstrap_ci(
    group: pd.DataFrame, column: str, n_bootstrap: int = 1000
) -> pd.Series:
    series = group[column]
    bootstrap_means = np.zeros(n_bootstrap)
    for i in range(n_bootstrap):
        bootstrap_sample = np.random.choice(series, size=len(series), replace=True)
        bootstrap_means[i] = bootstrap_sample.mean()
    ci_lower = np.percentile(bootstrap_means, 2.5)
    ci_upper = np.percentile(bootstrap_means, 97.5)
    return pd.Series(
        {
            f"{column}_mean": series.mean(),
            f"{column}_lb": ci_lower,
            f"{column}_ub": ci_upper,
        }
    )


articles = database.get_all_articles_with_opinions(settings["DB_URI"], n=100000)
print(len(articles))

data = pd.DataFrame(articles)
data = data[~data["topics"].isnull()]

cols = [c for c in data.columns if "_score" in c]
data[cols] = data[cols].astype(float)
for col in cols:
    data = data[data[col] >= 0]

# Calculate confidence intervals before grouping
bootstrapped_scientific = data.groupby("newspaper_name").apply(
    bootstrap_ci, column="scientific_accuracy_score"
)
bootstrapped_tone = data.groupby("newspaper_name").apply(
    bootstrap_ci, column="article_tone_score"
)

# Merge back to the original dataframe
grp = pd.concat([bootstrapped_scientific, bootstrapped_tone], axis=1)

grp = grp.sort_values("article_tone_score_mean", ascending=False)
print(grp)

# data ends

# First figure (Bar plots)
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 10))
grp.index.name = "newspaper_name"
grp = grp.reset_index()

grp = grp.sort_values("scientific_accuracy_score_mean", ascending=True)
axes[0].barh(
    grp["newspaper_name"],
    grp["scientific_accuracy_score_mean"],
    xerr=(
        grp["scientific_accuracy_score_mean"] - grp["scientific_accuracy_score_lb"],
        grp["scientific_accuracy_score_ub"] - grp["scientific_accuracy_score_mean"],
    ),
    ecolor="gray",
    capsize=3,
)

grp = grp.sort_values("article_tone_score_mean", ascending=True)
axes[1].barh(
    grp["newspaper_name"],
    grp["article_tone_score_mean"],
    xerr=(
        grp["article_tone_score_mean"] - grp["article_tone_score_lb"],
        grp["article_tone_score_ub"] - grp["article_tone_score_mean"],
    ),
    ecolor="gray",
    capsize=3,
)


axes[0].set_title("Scientific Accuracy Scores")
axes[1].set_title("Article Tone Scores")

# Second figure (Scatter plot)
fig2, ax2 = plt.subplots(figsize=(10, 10))
grp.plot(
    kind="scatter",
    x="scientific_accuracy_score_mean",
    y="article_tone_score_mean",
    ax=ax2,
)
ax2.set_xlabel("Scientific Accuracy Score")
ax2.set_ylabel("Article Tone Score")

# Formatting
plt.tight_layout()
# for ax in axes:
#     ax.get_legend().remove()

# Save figures
fig.savefig("gpt-opinion-bars.png")
fig2.savefig("gpt-opinion-scatter.png")


# Create a new dataframe where each topic gets its own row
topics_df = data.explode("topics")

# Group by newspaper_name and topics, then count
topic_counts = (
    topics_df.groupby(["newspaper_name", "topics"]).size().reset_index(name="counts")
)

# Sort the dataframe by counts, for each newspaper
topic_counts = topic_counts.sort_values(
    ["newspaper_name", "counts"], ascending=[True, False]
)

# Display the top 5 topics for each newspaper
top_topics = topic_counts.groupby("newspaper_name").head(5)

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))

for name, group in top_topics.groupby("newspaper_name"):
    ax.barh(group["topics"], group["counts"], label=name)

ax.set_xlabel("Count")
ax.set_ylabel("Topics")
ax.set_title("Top 5 Topics for Each Newspaper")
ax.legend()
fig.savefig("gpt-topics.png")

import matplotlib.cm as cm
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Create a new dataframe where each topic gets its own row
topics_df = data.explode("topics")

# Group by topics and calculate mean article_tone_score and counts
grouped_topics = (
    topics_df.groupby("topics")
    .agg({"article_tone_score": "mean", "id": "count"})
    .reset_index()
)
grouped_topics.columns = ["topics", "mean_tone_score", "counts"]

# Sort the dataframe by counts
grouped_topics = grouped_topics.sort_values("counts", ascending=False)

# Display the top 10 topics
top_topics = grouped_topics.head(32)

# Create a colormap based on the mean_tone_score
cmap = cm.get_cmap("RdYlBu")  # Choose colormap here
normalize = plt.Normalize(
    vmin=top_topics["mean_tone_score"].min(), vmax=top_topics["mean_tone_score"].max()
)
colors = [cmap(normalize(value)) for value in top_topics["mean_tone_score"]]

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(top_topics["topics"], top_topics["counts"], color=colors)

ax.set_xlabel("Count")
ax.set_ylabel("Topics")
ax.set_title("Top 10 Topics Across All Newspapers")

# Create colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = plt.colorbar(
    cm.ScalarMappable(norm=normalize, cmap=cmap), cax=cax, orientation="vertical"
)
cbar.ax.set_xlabel("Mean Tone Score")

# Save as PNG
plt.tight_layout()
plt.savefig("top-topics.png", format="png", dpi=300)

import matplotlib.cm as cm
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Create a new dataframe where each topic gets its own row
topics_df = data.explode("topics")

# Group by topics and calculate mean article_tone_score and counts
grouped_topics = (
    topics_df.groupby("topics")
    .agg({"article_tone_score": "mean", "id": "count"})
    .reset_index()
)
grouped_topics.columns = ["topics", "mean_tone_score", "counts"]

grouped_topics = grouped_topics[grouped_topics["counts"] >= 5]

# Sort the dataframe by mean_tone_score
highest_tone_topics = grouped_topics.sort_values(
    "mean_tone_score", ascending=False
).head(10)
lowest_tone_topics = grouped_topics.sort_values("mean_tone_score", ascending=True).head(
    10
)

# Create a colormap based on the mean_tone_score
cmap = cm.get_cmap("RdYlBu")  # Choose colormap here
normalize = plt.Normalize(
    vmin=grouped_topics["mean_tone_score"].min(),
    vmax=grouped_topics["mean_tone_score"].max(),
)

# Plotting
fig, axes = plt.subplots(3, 1, figsize=(10, 24))

# Most common topics
axes[0].barh(
    top_topics["topics"],
    top_topics["counts"],
    color=[cmap(normalize(value)) for value in top_topics["mean_tone_score"]],
)
axes[0].set_title("Top 10 Topics Across All Newspapers")

# Topics with highest mean tone score
axes[1].barh(
    highest_tone_topics["topics"],
    highest_tone_topics["counts"],
    color=[cmap(normalize(value)) for value in highest_tone_topics["mean_tone_score"]],
)
axes[1].set_title("Top 10 Topics with Highest Mean Tone Score")

# Topics with lowest mean tone score
axes[2].barh(
    lowest_tone_topics["topics"],
    lowest_tone_topics["counts"],
    color=[cmap(normalize(value)) for value in lowest_tone_topics["mean_tone_score"]],
)
axes[2].set_title("Top 10 Topics with Lowest Mean Tone Score")

for ax in axes:
    ax.set_xlabel("Count")
    ax.set_ylabel("Topics")

# Create colorbar
divider = make_axes_locatable(axes[2])
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = plt.colorbar(
    cm.ScalarMappable(norm=normalize, cmap=cmap), cax=cax, orientation="vertical"
)
cbar.ax.set_xlabel("Mean Tone Score")

# Save as PNG
plt.savefig("topics-analysis.png", format="png", dpi=300)
