from transformers import AutoTokenizer, AutoModelForSequenceClassification, logging
import torch
import torch.nn.functional as func

logging.set_verbosity_error()

class RobertaSentiment:
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest", labels: list[str] = ["negative", "neutral", "positive"]):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.labels = labels

    def predict(self, ticker: str, articles: list[str]):
        if not articles:
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "articles_analyzed": 0,
                "distribution": {},
                "most_positive": "",
                "most_negative": ""
            }

        sentiment_counts = {label: 0 for label in self.labels}
        sentiment_scores = {label: 0.0 for label in self.labels}

        most_positive = -1
        most_negative = -1
        most_positive_article = ""
        most_negative_article = ""

        for text in articles:
            inputs = self.tokenizer(text[0], return_tensors="pt", truncation=True, max_length=512)

            with torch.no_grad():
                logit = self.model(**inputs).logits
                probs = func.softmax(logit, dim=1).squeeze()

            predicted_idx = torch.argmax(probs).item()
            sentiment = self.labels[predicted_idx]
            confidence = probs[predicted_idx].item()

            neg_score = probs[0].item()
            pos_score = probs[2].item()

            if predicted_idx == 1 and probs[1].item() <= 0.7:
                if neg_score > pos_score:
                    sentiment = self.labels[0]
                    confidence = probs[0].item()
                else:
                    sentiment = self.labels[2]
                    confidence = probs[2].item()


            sentiment_counts[sentiment] += 1
            sentiment_scores[sentiment] += confidence
                
            if sentiment == self.labels[2] and pos_score > most_positive:
                most_positive = pos_score
                most_positive_article = text
            
            if sentiment == self.labels[0] and neg_score > most_negative:
                most_negative = neg_score
                most_negative_article = text

        total_articles = len(articles)
        avg_scores = {label: sentiment_scores[label] / sentiment_counts[label]  if sentiment_counts[label] > 0 else 0.0 for label in self.labels}
        
        major_sentiment = max(avg_scores.items(), key=lambda x: x[1])[0]
        major_confidence = round(avg_scores[major_sentiment], 4)

        most_positive_article_text = most_positive_article[0].split(" How might investors react?")[0].split(f"News about {ticker.upper()}: ")[1]
        most_negative_article_text = most_negative_article[0].split(" How might investors react?")[0].split(f"News about {ticker.upper()}: ")[1]

        most_positive_article_source = most_positive_article[1]
        most_negative_article_source = most_negative_article[1]

        most_positive_article_time = most_positive_article[2]
        most_negative_article_time = most_negative_article[2]

        return {
            "sentiment": major_sentiment,
            "confidence": major_confidence,
            "articles_analyzed": total_articles,
            "avg_scores": avg_scores,
            "distribution": sentiment_counts,
            "most_positive": most_positive_article_text,
            "most_negative": most_negative_article_text,
            "most_positive_score": most_positive,
            "most_negative_score": most_negative,
            "most_positive_source": most_positive_article_source,
            "most_negative_source": most_negative_article_source,
            "most_positive_time": most_positive_article_time,
            "most_negative_time": most_negative_article_time,
        }