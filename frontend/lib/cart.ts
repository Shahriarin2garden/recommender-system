export interface CartItem {
  id: number
  name: string
  price: number
  category: string
  image_url?: string | null
  quantity: number
}

export const CART_UPDATED_EVENT = 'cart-updated'

export function getCartItems(): CartItem[] {
  if (typeof window === 'undefined') return []
  try {
    const items = localStorage.getItem('cart')
    return items ? JSON.parse(items) : []
  } catch (e) {
    console.error('Failed to parse cart items:', e)
    return []
  }
}

export function saveCartItems(items: CartItem[]) {
  if (typeof window === 'undefined') return
  localStorage.setItem('cart', JSON.stringify(items))
  window.dispatchEvent(new Event(CART_UPDATED_EVENT))
}

export function addToCart(product: { id: number; name: string; price?: number; category: string; image_url?: string | null }) {
  const items = getCartItems()
  const existing = items.find((item) => item.id === product.id)
  
  if (existing) {
    existing.quantity += 1
  } else {
    items.push({
      id: product.id,
      name: product.name,
      price: product.price ?? 0,
      category: product.category,
      image_url: product.image_url,
      quantity: 1,
    })
  }
  
  saveCartItems(items)
}

export function removeFromCart(id: number) {
  const items = getCartItems()
  const updated = items.filter((item) => item.id !== id)
  saveCartItems(updated)
}

export function clearCart() {
  saveCartItems([])
}

export function getCartCount(): number {
  const items = getCartItems()
  return items.reduce((sum, item) => sum + item.quantity, 0)
}
