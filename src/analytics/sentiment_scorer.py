import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from pathlib import Path


def score_sentiment():
    """
    Applies NLTK SentimentIntensityAnalyzer to score the polarity
    of generated pros (positive) and cons (negative).
    """
    print(" Starting NLP : Sentiment Scorer...")

    # Download NLTK VADER lexicon if not already downloaded
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        print(" Downloading NLTK VADER lexicon for the first time...")
        nltk.download("vader_lexicon", quiet=True)

    # File paths
    root_path = Path(__file__).resolve().parents[2]
    file_path = os.path.join(root_path, "pros_cons_generated.csv")

    if not os.path.exists(file_path):
        print(f" Error: {file_path} not found.")
        return

    try:
        # Load the generated pros and cons
        df = pd.read_csv(file_path)
        print(f" Successfully loaded {len(df)} Pros/Cons entries.")
    except Exception as e:
        print(f" Error reading file: {e}")
        return

    # Initialize the Sentiment Analyzer
    sia = SentimentIntensityAnalyzer()
    print(" Analyzing text sentiment using NLTK VADER...")

    # Apply sentiment scoring
    # 'compound' score ranges from -1 (most negative) to +1 (most positive)
    df["sentiment_score"] = df["text"].apply(
        lambda text: sia.polarity_scores(str(text))["compound"]
    )

    # Save the updated dataframe (Overwriting the same file as per sprint requirements)
    df.to_csv(file_path, index=False)

    print(" Sentiment Scoring Complete!")
    print(f" Updated report saved to: {file_path}\n")

    # Display a sample of the scored data
    if not df.empty:
        print(" SAMPLE SENTIMENT SCORES:")
        # Show a mix of both Pros and Cons to see the difference in scores
        sample_df = pd.concat(
            [df[df["type"] == "Pro"].head(3), df[df["type"] == "Con"].head(3)]
        )
        print(
            sample_df[["company_id", "type", "sentiment_score", "text"]].to_string(
                index=False
            )
        )


if __name__ == "__main__":
    score_sentiment()
