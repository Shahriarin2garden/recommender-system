"""
Data preprocessing pipeline for the recommender system.
Loads raw data, cleans, transforms, and stores in PostgreSQL.
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os
import random

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://recommender_user:recommender_pass@localhost:5432/recommender_db"
)

def generate_sample_data():
    """Generate sample e-commerce data for MVP testing."""
    
    print("Generating sample data...")
    
    # Sample product categories
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
    
    # Generate products
    products = []
    for i in range(1, 101):
        category = random.choice(categories)
        products.append({
            "id": i,
            "name": f"Product {i} - {category}",
            "description": f"High-quality {category.lower()} item with great features",
            "category": category,
            "price": round(random.uniform(9.99, 499.99), 2),
            "image_url": f"https://picsum.photos/400/400?random={i}",
            "tags": ",".join(random.sample(["popular", "new", "sale", "trending"], k=2)),
            "stock_quantity": random.randint(0, 100),
            "is_active": True,
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365))
        })
    
    # Generate users
    users = []
    for i in range(1, 51):
        users.append({
            "id": i,
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            "full_name": f"User {i}",
            "cohort": random.choice(["A", "B"]),
            "is_active": True,
            "created_at": datetime.now() - timedelta(days=random.randint(1, 180))
        })
    
    # Generate interactions (views, clicks, ratings)
    interactions = []
    interaction_id = 1
    for user in users:
        # Each user interacts with 5-20 random products
        num_interactions = random.randint(5, 20)
        user_products = random.sample(products, num_interactions)
        
        for product in user_products:
            interaction_type = random.choice(["view", "click", "click", "rating"])
            interactions.append({
                "id": interaction_id,
                "user_id": user["id"],
                "product_id": product["id"],
                "interaction_type": interaction_type,
                "rating": random.uniform(3.0, 5.0) if interaction_type == "rating" else None,
                "timestamp": datetime.now() - timedelta(days=random.randint(0, 30)),
                "session_id": f"session_{user['id']}_{random.randint(1000, 9999)}"
            })
            interaction_id += 1
    
    return pd.DataFrame(products), pd.DataFrame(users), pd.DataFrame(interactions)

def create_user_item_matrix(interactions_df):
    """
    Create user-item interaction matrix for collaborative filtering.
    Returns a sparse matrix where rows=users, cols=products, values=ratings/counts.
    """
    # For ratings, use actual rating values
    # For other interactions, count occurrences
    matrix = interactions_df.pivot_table(
        index='user_id',
        columns='product_id',
        values='rating',
        aggfunc='mean',
        fill_value=0
    )
    
    print(f"User-item matrix shape: {matrix.shape}")
    print(f"Sparsity: {(matrix == 0).sum().sum() / (matrix.shape[0] * matrix.shape[1]) * 100:.2f}%")
    
    return matrix

def compute_product_features(products_df):
    """
    Extract features from products for content-based filtering.
    Uses TF-IDF on product descriptions and category encoding.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import OneHotEncoder
    
    # TF-IDF on descriptions
    tfidf = TfidfVectorizer(max_features=100, stop_words='english')
    text_features = tfidf.fit_transform(products_df['description'].fillna(''))
    
    # One-hot encode categories
    encoder = OneHotEncoder(sparse=True)
    category_features = encoder.fit_transform(products_df[['category']])
    
    print(f"Text features shape: {text_features.shape}")
    print(f"Category features shape: {category_features.shape}")
    
    return text_features, category_features, tfidf, encoder

def load_to_database(products_df, users_df, interactions_df):
    """Load dataframes into PostgreSQL database."""
    
    print("Connecting to database...")
    engine = create_engine(DATABASE_URL)
    
    try:
        print("Loading products...")
        products_df.to_sql('products', engine, if_exists='replace', index=False)
        
        print("Loading users...")
        users_df.to_sql('users', engine, if_exists='replace', index=False)
        
        print("Loading interactions...")
        interactions_df.to_sql('interactions', engine, if_exists='replace', index=False)
        
        print("Data loaded successfully!")
        
        # Print summary statistics
        print("\n=== Data Summary ===")
        print(f"Products: {len(products_df)}")
        print(f"Users: {len(users_df)}")
        print(f"Interactions: {len(interactions_df)}")
        print(f"Categories: {products_df['category'].nunique()}")
        print(f"Avg interactions per user: {len(interactions_df) / len(users_df):.1f}")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        raise
    finally:
        engine.dispose()

def main():
    """Main preprocessing pipeline."""
    
    print("=" * 50)
    print("E-commerce Recommender - Data Preprocessing")
    print("=" * 50)
    
    # Generate sample data
    products_df, users_df, interactions_df = generate_sample_data()
    
    # Create user-item matrix
    user_item_matrix = create_user_item_matrix(interactions_df)
    
    # Compute product features
    text_features, category_features, tfidf, encoder = compute_product_features(products_df)
    
    # Load to database
    load_to_database(products_df, users_df, interactions_df)
    
    # Save preprocessed artifacts for model training
    print("\nSaving preprocessing artifacts...")
    np.save('ml/user_item_matrix.npy', user_item_matrix.values)
    np.save('ml/text_features.npy', text_features.toarray())
    
    import joblib
    joblib.dump(tfidf, 'ml/tfidf_vectorizer.pkl')
    joblib.dump(encoder, 'ml/category_encoder.pkl')
    
    print("\n✅ Preprocessing complete!")
    print("Next step: Train the recommendation model using train_model.ipynb")

if __name__ == "__main__":
    main()
