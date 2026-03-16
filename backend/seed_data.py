"""
Quick data seeder to populate the database with sample products and users.
Run this to get started with test data.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal, engine
from app.models import Base, User, Product, Interaction
from passlib.context import CryptContext
import random
from datetime import datetime, timedelta

# Create all tables
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def build_product_image_url(product_name: str) -> str:
       image_map = {
           "Wireless Headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=800&fit=crop&auto=format&q=80",
           "Smart Watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&h=800&fit=crop&auto=format&q=80",
           "Laptop Stand": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&h=800&fit=crop&auto=format&q=80",
           "USB-C Hub": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=800&h=800&fit=crop&auto=format&q=80",
           "Mechanical Keyboard": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=800&h=800&fit=crop&auto=format&q=80",
           "Cotton T-Shirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=800&fit=crop&auto=format&q=80",
           "Denim Jeans": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=800&fit=crop&auto=format&q=80",
           "Running Shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=800&fit=crop&auto=format&q=80",
           "Winter Jacket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&h=800&fit=crop&auto=format&q=80",
           "Baseball Cap": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=800&h=800&fit=crop&auto=format&q=80",
           "Coffee Maker": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&h=800&fit=crop&auto=format&q=80",
           "Blender": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=800&h=800&fit=crop&auto=format&q=80",
           "Throw Pillow": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=800&fit=crop&auto=format&q=80",
           "Desk Lamp": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=800&fit=crop&auto=format&q=80",
           "Storage Bins": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=800&fit=crop&auto=format&q=80",
           "Python Programming Book": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&h=800&fit=crop&auto=format&q=80",
           "Sci-Fi Novel": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=800&fit=crop&auto=format&q=80",
           "Cookbook": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&h=800&fit=crop&auto=format&q=80",
           "Yoga Mat": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=800&fit=crop&auto=format&q=80",
           "Dumbbells Set": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=800&fit=crop&auto=format&q=80",
           "Resistance Bands": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=800&h=800&fit=crop&auto=format&q=80",
           "Water Bottle": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=800&h=800&fit=crop&auto=format&q=80",
       }
       return image_map.get(product_name, "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&h=800&fit=crop&auto=format&q=80")

def hash_password(password: str) -> str:
       """Hash password using the same algorithm as auth."""
       return pwd_context.hash(password)

def seed_data():
    """Seed the database with sample data."""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create sample users
        users = [
            User(
                email="alice@example.com",
                username="alice",
                hashed_password=hash_password("password123"),
                full_name="Alice Johnson",
                cohort="A",
                is_active=True
            ),
            User(
                email="bob@example.com",
                username="bob",
                hashed_password=hash_password("password123"),
                full_name="Bob Smith",
                cohort="B",
                is_active=True
            ),
            User(
                email="charlie@example.com",
                username="charlie",
                hashed_password=hash_password("password123"),
                full_name="Charlie Brown",
                cohort="A",
                is_active=True
            ),
            User(
                email="admin@example.com",
                username="admin",
                hashed_password=hash_password("admin123"),
                full_name="Admin User",
                cohort="A",
                is_active=True
            )
        ]
        
        db.add_all(users)
        db.commit()
        print(f"Created {len(users)} users")
        
        # Sample products
        products = [
            # Electronics
            Product(name="Wireless Headphones", description="High-quality Bluetooth headphones with noise cancellation", 
                   category="Electronics", price=149.99, stock_quantity=50, tags="audio,wireless,bluetooth",
                   image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"),
            Product(name="Smart Watch", description="Fitness tracking smartwatch with heart rate monitor", 
                   category="Electronics", price=299.99, stock_quantity=30, tags="fitness,wearable,smart",
                   image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"),
            Product(name="Laptop Stand", description="Ergonomic aluminum laptop stand", 
                   category="Electronics", price=49.99, stock_quantity=100, tags="desk,ergonomic,aluminum",
                   image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400"),
            Product(name="USB-C Hub", description="7-in-1 USB-C hub with multiple ports", 
                   category="Electronics", price=39.99, stock_quantity=75, tags="usb,adapter,hub",
                   image_url="https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400"),
            Product(name="Mechanical Keyboard", description="RGB mechanical keyboard with blue switches", 
                   category="Electronics", price=129.99, stock_quantity=40, tags="keyboard,gaming,rgb",
                   image_url="https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400"),
            
            # Clothing
            Product(name="Cotton T-Shirt", description="Comfortable 100% cotton t-shirt", 
                   category="Clothing", price=24.99, stock_quantity=200, tags="cotton,casual,basic",
                   image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"),
            Product(name="Denim Jeans", description="Classic blue denim jeans", 
                   category="Clothing", price=59.99, stock_quantity=150, tags="denim,pants,casual",
                   image_url="https://images.unsplash.com/photo-1542272604-787c3835535d?w=400"),
            Product(name="Running Shoes", description="Lightweight running shoes with cushioning", 
                   category="Clothing", price=89.99, stock_quantity=80, tags="shoes,running,sports",
                   image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"),
            Product(name="Winter Jacket", description="Warm winter jacket with hood", 
                   category="Clothing", price=149.99, stock_quantity=60, tags="jacket,winter,warm",
                   image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"),
            Product(name="Baseball Cap", description="Adjustable baseball cap", 
                   category="Clothing", price=19.99, stock_quantity=120, tags="hat,cap,casual",
                   image_url="https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400"),
            
            # Home & Kitchen
            Product(name="Coffee Maker", description="Programmable coffee maker with thermal carafe", 
                   category="Home", price=79.99, stock_quantity=45, tags="coffee,kitchen,appliance",
                   image_url="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400"),
            Product(name="Blender", description="High-speed blender for smoothies", 
                   category="Home", price=69.99, stock_quantity=55, tags="blender,kitchen,smoothie",
                   image_url="https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400"),
            Product(name="Throw Pillow", description="Decorative throw pillow", 
                   category="Home", price=29.99, stock_quantity=90, tags="pillow,decor,home",
                   image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400"),
            Product(name="Desk Lamp", description="LED desk lamp with adjustable brightness", 
                   category="Home", price=44.99, stock_quantity=70, tags="lamp,desk,led",
                   image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
            Product(name="Storage Bins", description="Set of 3 storage bins", 
                   category="Home", price=34.99, stock_quantity=100, tags="storage,organizer,home",
                   image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"),
            
            # Books
            Product(name="Python Programming Book", description="Comprehensive guide to Python", 
                   category="Books", price=39.99, stock_quantity=35, tags="book,programming,python",
                   image_url="https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400"),
            Product(name="Sci-Fi Novel", description="Best-selling science fiction novel", 
                   category="Books", price=14.99, stock_quantity=80, tags="book,scifi,novel",
                   image_url="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400"),
            Product(name="Cookbook", description="Healthy recipes cookbook", 
                   category="Books", price=24.99, stock_quantity=50, tags="book,cooking,recipes",
                   image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"),
            
            # Sports
            Product(name="Yoga Mat", description="Non-slip yoga mat with carrying strap", 
                   category="Sports", price=29.99, stock_quantity=95, tags="yoga,fitness,mat",
                   image_url="https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400"),
            Product(name="Dumbbells Set", description="Adjustable dumbbells set (5-25 lbs)", 
                   category="Sports", price=199.99, stock_quantity=25, tags="weights,fitness,dumbbells",
                   image_url="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400"),
            Product(name="Resistance Bands", description="Set of 5 resistance bands", 
                   category="Sports", price=24.99, stock_quantity=110, tags="bands,fitness,resistance",
                   image_url="https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400"),
            Product(name="Water Bottle", description="Insulated stainless steel water bottle", 
                   category="Sports", price=19.99, stock_quantity=150, tags="bottle,hydration,insulated",
                   image_url="https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400"),
        ]

              for product in products:
                     product.image_url = build_product_image_url(product.name)
        
        db.add_all(products)
        db.commit()
        print(f"Created {len(products)} products")
        
        # Create some sample interactions
        interactions = []
        for user in users[:3]:  # First 3 users
            # Each user interacts with 5-10 random products
            num_interactions = random.randint(5, 10)
            product_sample = random.sample(products, num_interactions)
            
            for product in product_sample:
                # Random interaction type
                interaction_type = random.choice(["view", "view", "click", "click", "purchase"])
                rating = random.uniform(3.5, 5.0) if interaction_type == "purchase" else None
                
                interaction = Interaction(
                    user_id=user.id,
                    product_id=product.id,
                    interaction_type=interaction_type,
                    rating=rating,
                    timestamp=datetime.now() - timedelta(days=random.randint(0, 30))
                )
                interactions.append(interaction)
        
        db.add_all(interactions)
        db.commit()
        print(f"Created {len(interactions)} interactions")
        
        print("\n" + "="*60)
        print("Database seeded successfully!")
        print("="*60)
        print("\nTest Accounts:")
        print("   Email: alice@example.com | Password: password123 (Cohort A)")
        print("   Email: bob@example.com   | Password: password123 (Cohort B)")
        print("   Email: admin@example.com | Password: admin123")
        print("\nProducts: 22 sample products across 5 categories")
        print("Interactions: Sample user activity generated")
        print("\nNext steps:")
        print("   1. Visit http://localhost:3000 to see the frontend")
        print("   2. Login with test accounts")
        print("   3. Browse products and recommendations")
        print("   4. Visit http://localhost:8000/docs for API documentation")
        print("="*60)
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
