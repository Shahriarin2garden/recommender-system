"""One-off utility to normalize product images to deterministic product-name placeholders."""

from urllib.parse import quote_plus

from app.database import SessionLocal
from app.models import Product


def build_product_image_url(product_name: str) -> str:
    return f"https://placehold.co/800x800/png?text={quote_plus(product_name)}"


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
