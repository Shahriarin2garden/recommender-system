'use client'

import { useEffect, useMemo, useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { ShoppingBag, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { CartItem, clearCart, getCartItems, removeFromCart, CART_UPDATED_EVENT } from '@/lib/cart'

export default function CartPage() {
  const [items, setItems] = useState<CartItem[]>([])

  useEffect(() => {
    const syncCart = () => setItems(getCartItems())

    syncCart()
    window.addEventListener('storage', syncCart)
    window.addEventListener(CART_UPDATED_EVENT, syncCart)

    return () => {
      window.removeEventListener('storage', syncCart)
      window.removeEventListener(CART_UPDATED_EVENT, syncCart)
    }
  }, [])

  const total = useMemo(
    () => items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    [items]
  )

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-6 lg:px-8 py-10">
        <h1 className="text-3xl font-bold mb-6">Your Cart</h1>
        <div className="rounded-2xl border p-8 text-center">
          <ShoppingBag className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground mb-4">Your cart is empty.</p>
          <Button asChild variant="glass">
            <Link href="/">Continue Shopping</Link>
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-6 lg:px-8 py-10">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Your Cart</h1>
        <Button variant="outline" onClick={clearCart}>Clear Cart</Button>
      </div>

      <div className="space-y-4">
        {items.map((item) => (
          <div key={item.id} className="rounded-2xl border p-4 flex items-center gap-4">
            <div className="relative h-20 w-20 rounded-lg overflow-hidden bg-muted/30">
              {item.image_url ? (
                <Image src={item.image_url} alt={item.name} fill className="object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <ShoppingBag className="h-8 w-8 text-muted-foreground/40" />
                </div>
              )}
            </div>

            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">{item.name}</p>
              <p className="text-sm text-muted-foreground">{item.category}</p>
              <p className="text-sm mt-1">Qty: {item.quantity}</p>
            </div>

            <div className="text-right">
              <p className="font-semibold">${(item.price * item.quantity).toFixed(2)}</p>
              <Button
                variant="ghost"
                size="icon"
                className="mt-1"
                onClick={() => removeFromCart(item.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 rounded-2xl border p-6 flex items-center justify-between">
        <p className="text-lg font-semibold">Total</p>
        <p className="text-xl font-bold">${total.toFixed(2)}</p>
      </div>
    </div>
  )
}
