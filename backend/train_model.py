#!/usr/bin/env python
"""
Quick ML training script to generate recommendation model from database data.
"""
import sys
import os
sys.path.insert(0, '/app')

import numpy as np
import pandas as pd
import joblib
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Try to import implicit ALS, fall back to sklearn if not available
try:
    from implicit.als import AlternatingLeastSquares
    USE_IMPLICIT = True
except ImportError:
    from sklearn.decomposition import NMF
    USE_IMPLICIT = False

from app.database import SessionLocal
from app.models import User, Product, Interaction

def train_ml_model():
    """Train the recommendation model using database data."""
    print("🚀 Starting ML model training...")
    
    # Connect to database
    db = SessionLocal()
    
    try:
        # Fetch data
        users = db.query(User).all()
        products = db.query(Product).all()
        interactions = db.query(Interaction).all()
        
        print(f"✓ Loaded {len(users)} users")
        print(f"✓ Loaded {len(products)} products")
        print(f"✓ Loaded {len(interactions)} interactions")
        
        if not users or not products or not interactions:
            print("⚠ Insufficient data. Please run seed_data.py first.")
            return False
        
        # Create user-item matrix for collaborative filtering
        user_idx = {u.id: i for i, u in enumerate(users)}
        product_idx = {p.id: i for i, p in enumerate(products)}
        
        user_item_matrix = np.zeros((len(users), len(products)), dtype=np.float32)
        for interaction in interactions:
            if interaction.user_id in user_idx and interaction.product_id in product_idx:
                user_id_idx = user_idx[interaction.user_id]
                prod_id_idx = product_idx[interaction.product_id]
                # Weight: 1 for view, 2 for click, 3 for purchase
                weight = 1 + int(interaction.interaction_type in ['click', 'purchase'])
                if interaction.interaction_type == 'purchase':
                    weight = 3
                user_item_matrix[user_id_idx, prod_id_idx] += weight
        
        print(f"✓ User-item matrix: {user_item_matrix.shape}")
        
        # Train collaborative filtering model
        print("\n📊 Training collaborative filtering model...")
        sparse_matrix = csr_matrix(user_item_matrix)
        
        if USE_IMPLICIT:
            print("  Using Implicit ALS...")
            model = AlternatingLeastSquares(
                factors=50,
                regularization=0.01,
                iterations=20,
                random_state=42,
                calculate_training_loss=False
            )
            model.fit(sparse_matrix)
        else:
            print("  Using sklearn NMF (Implicit not available)...")
            model = NMF(n_components=50, init='random', random_state=42)
            model.fit(user_item_matrix)
        
        # Train content-based model using TF-IDF
        print("\n📝 Training content-based similarity model...")
        product_names = [p.name for p in products]
        product_descriptions = [f"{p.name} {p.category}" for p in products]
        
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(product_descriptions)
        product_similarity = cosine_similarity(tfidf_matrix)
        
        print(f"✓ Product similarity matrix: {product_similarity.shape}")
        
        # Save models
        print("\n💾 Saving models...")
        os.makedirs('/app/ml', exist_ok=True)
        
        joblib.dump(model, '/app/ml/model.pkl')
        joblib.dump(vectorizer, '/app/ml/vectorizer.pkl')
        np.save('/app/ml/product_similarity.npy', product_similarity)
        np.save('/app/ml/user_item_matrix.npy', user_item_matrix)
        
        print("✓ Model saved: /app/ml/model.pkl")
        print("✓ Vectorizer saved: /app/ml/vectorizer.pkl")
        print("✓ Product similarity saved: /app/ml/product_similarity.npy")
        print("✓ User-item matrix saved: /app/ml/user_item_matrix.npy")
        
        # Test recommendations
        print("\n🧪 Testing recommendations...")
        if len(users) > 0:
            test_user_idx = 0
            if USE_IMPLICIT:
                recs = model.recommend(test_user_idx, sparse_matrix[test_user_idx], N=5)
                print(f"\nTop 5 recommendations for User {users[test_user_idx].id}:")
                for prod_idx, score in recs:
                    print(f"  • {products[prod_idx].name}: score {score:.3f}")
            else:
                scores = model.transform(sparse_matrix[[test_user_idx]])[0]
                top_indices = np.argsort(-scores)[:5]
                top_indices = top_indices[top_indices < len(products)]  # Filter valid indices
                print(f"\nTop 5 recommendations for User {users[test_user_idx].id}:")
                for i, prod_idx in enumerate(top_indices[:5], 1):
                    if prod_idx < len(products):
                        print(f"  • {products[prod_idx].name}: score {scores[prod_idx]:.3f}")
        
        print("\n✅ ML Model training complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == '__main__':
    success = train_ml_model()
    sys.exit(0 if success else 1)
