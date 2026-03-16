"""One-off utility to update existing product images to real photo URLs."""

from app.database import SessionLocal
from app.models import Product


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


def run() -> None:
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        for product in products:
            product.image_url = build_product_image_url(product.name)
        db.commit()
        print(f"Updated {len(products)} product images")
    finally:
        db.close()


if __name__ == "__main__":
    run()
