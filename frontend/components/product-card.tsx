'use client'

import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { ShoppingBag, Heart } from 'lucide-react'
import { Button } from './ui/button'
import { addToCart } from '@/lib/cart'

interface Product {
  id: number
  name: string
  price?: number
  category: string
  image_url?: string | null
}

export function ProductCard({ product }: { product: Product }) {
  const [isAdded, setIsAdded]     = useState(false)
  const [isWishlisted, setWished] = useState(false)

  const handleAddToCart = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    e.stopPropagation()
    addToCart(product)
    setIsAdded(true)
    setTimeout(() => setIsAdded(false), 1400)
  }

  const handleWishlist = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setWished((v) => !v)
  }

  return (
    <Link href={`/product/${product.id}`} className="group block outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-2xl">

      {/* Image container */}
      <div className="relative aspect-square overflow-hidden rounded-2xl bg-muted/40 mb-4">

        {product.image_url ? (
          <Image
            src={product.image_url}
            alt={product.name}
            fill
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
            className="object-cover transition-transform duration-700 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:scale-[1.04]"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <ShoppingBag className="h-14 w-14 text-muted-foreground/20" />
          </div>
        )}

        {/* Dark overlay on hover */}
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/8 transition-colors duration-300" />

        {/* Wishlist */}
        <button
          onClick={handleWishlist}
          aria-label={isWishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
          className={`absolute top-3 right-3 h-8 w-8 rounded-full flex items-center justify-center
            bg-white/90 backdrop-blur-sm shadow-sm cursor-pointer
            opacity-0 group-hover:opacity-100
            transition-all duration-300 hover:scale-110 active:scale-95
            ${isWishlisted ? 'text-rose-500' : 'text-foreground/60'}`}
        >
          <Heart className={`h-3.5 w-3.5 transition-all ${isWishlisted ? 'fill-current' : ''}`} />
        </button>

        {/* Add to cart */}
        <div className="absolute bottom-3 left-3 right-3 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0">
          <button
            onClick={handleAddToCart}
            className={`w-full h-9 rounded-full text-xs font-medium cursor-pointer
              flex items-center justify-center gap-1.5
              transition-all duration-200
              ${isAdded
                ? 'bg-foreground text-background'
                : 'bg-white/90 backdrop-blur-sm text-foreground hover:bg-white shadow-sm'
              }`}
          >
            {isAdded ? (
              <span className="animate-fade-in">✓ Added</span>
            ) : (
              <>
                <ShoppingBag className="h-3.5 w-3.5" />
                Add to Cart
              </>
            )}
          </button>
        </div>
      </div>

      {/* Product info */}
      <div className="space-y-0.5 px-0.5">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-medium leading-snug line-clamp-2 group-hover:text-foreground/70 transition-colors duration-200">
              {product.name}
            </h3>
            <p className="text-xs text-muted-foreground mt-0.5 capitalize">{product.category}</p>
          </div>
          <span className="text-sm font-semibold tabular-nums shrink-0">
            ${product.price?.toFixed(2) ?? '0.00'}
          </span>
        </div>
      </div>

    </Link>
  )
}
