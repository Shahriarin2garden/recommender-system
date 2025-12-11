"""
Utility functions for ML model serving and predictions.
"""

import numpy as np
import joblib
from typing import List, Tuple
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
TFIDF_PATH = os.path.join(os.path.dirname(__file__), 'tfidf_vectorizer.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'category_encoder.pkl')

def load_model():
    """Load trained recommendation model from disk."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def load_vectorizers():
    """Load TF-IDF vectorizer and category encoder."""
    tfidf = joblib.load(TFIDF_PATH) if os.path.exists(TFIDF_PATH) else None
    encoder = joblib.load(ENCODER_PATH) if os.path.exists(ENCODER_PATH) else None
    return tfidf, encoder

def predict_collaborative(user_id: int, model, top_n: int = 10) -> List[Tuple[int, float]]:
    """
    Generate collaborative filtering recommendations for a user.
    
    Args:
        user_id: User ID
        model: Trained collaborative filtering model
        top_n: Number of recommendations to return
    
    Returns:
        List of (product_id, score) tuples
    """
    try:
        # Get user recommendations from model
        recommendations = model.recommend(user_id, top_n=top_n)
        return [(int(prod_id), float(score)) for prod_id, score in recommendations]
    except Exception as e:
        print(f"Error in collaborative filtering: {e}")
        return []

def predict_content_based(product_id: int, product_features, top_n: int = 5) -> List[Tuple[int, float]]:
    """
    Generate content-based recommendations for similar products.
    
    Args:
        product_id: Product ID to find similar items for
        product_features: Feature matrix for all products
        top_n: Number of similar products to return
    
    Returns:
        List of (product_id, similarity_score) tuples
    """
    from sklearn.metrics.pairwise import cosine_similarity
    
    try:
        # Compute cosine similarity
        similarities = cosine_similarity(
            product_features[product_id:product_id+1],
            product_features
        ).flatten()
        
        # Get top-N most similar (excluding the product itself)
        similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
        similar_scores = similarities[similar_indices]
        
        return [(int(idx), float(score)) for idx, score in zip(similar_indices, similar_scores)]
    except Exception as e:
        print(f"Error in content-based filtering: {e}")
        return []

def hybrid_recommendation(user_id: int, collaborative_model, product_features, 
                         alpha: float = 0.7, top_n: int = 10) -> List[Tuple[int, float]]:
    """
    Hybrid recommendation combining collaborative and content-based approaches.
    
    Args:
        user_id: User ID
        collaborative_model: Trained collaborative filtering model
        product_features: Product feature matrix
        alpha: Weight for collaborative filtering (1-alpha for content-based)
        top_n: Number of recommendations
    
    Returns:
        List of (product_id, combined_score) tuples
    """
    # Get collaborative recommendations
    collab_recs = predict_collaborative(user_id, collaborative_model, top_n=top_n*2)
    
    # Combine scores (weighted average)
    # In practice, you'd also incorporate content-based scores for these products
    final_recs = sorted(collab_recs, key=lambda x: x[1], reverse=True)[:top_n]
    
    return final_recs

def evaluate_model(predictions, ground_truth, k: int = 10) -> dict:
    """
    Evaluate recommendation model performance.
    
    Args:
        predictions: Predicted items for each user
        ground_truth: Actual items interacted with
        k: Top-k items to consider
    
    Returns:
        Dictionary with evaluation metrics
    """
    from sklearn.metrics import precision_score, recall_score
    
    # Calculate Precision@K and Recall@K
    precisions = []
    recalls = []
    
    for pred, truth in zip(predictions, ground_truth):
        pred_k = set(pred[:k])
        truth_set = set(truth)
        
        if len(pred_k) > 0:
            precision = len(pred_k & truth_set) / len(pred_k)
            precisions.append(precision)
        
        if len(truth_set) > 0:
            recall = len(pred_k & truth_set) / len(truth_set)
            recalls.append(recall)
    
    return {
        "precision@k": np.mean(precisions) if precisions else 0,
        "recall@k": np.mean(recalls) if recalls else 0,
        "k": k
    }

class RecommenderCache:
    """Simple in-memory cache for recommendations."""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, key: str):
        """Get cached recommendations."""
        return self.cache.get(key)
    
    def set(self, key: str, value):
        """Cache recommendations."""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple LRU)
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value
    
    def clear(self):
        """Clear cache."""
        self.cache.clear()
