'use client'

import Image from 'next/image'
import Link from 'next/link'
import { ShoppingBag, Heart } from 'lucide-react'
import { Button } from './ui/button'

interface Product {
  id: number
  name: string
  price?: number
  category: string
  image_url?: string | null
}

export function ProductCard({ product }: { product: Product }) {
  return (
    <Link href={`/product/${product.id}`}>
      <div className="group cursor-pointer">
        {/* Image Container - Clean, borderless */}
        <div className="relative aspect-square overflow-hidden rounded-2xl bg-muted/30 mb-4">
          {product.image_url ? (
            <Image
              src={product.image_url}
              alt={product.name}
              fill
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
              className="object-cover transition-all duration-500 group-hover:scale-105"
              loading="lazy"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-muted/30">
              <ShoppingBag className="h-16 w-16 text-muted-foreground/30" />
            </div>
          )}
          
          {/* Hover overlay with actions */}
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-all duration-300" />
          
          {/* Wishlist button */}
          <Button
            size="icon"
            variant="secondary"
            className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-all duration-300 rounded-full bg-white hover:bg-white shadow-lg"
          >
            <Heart className="h-4 w-4 text-foreground" />
          </Button>

          {/* Quick add to cart button */}
          <Button
            className="absolute bottom-3 left-3 right-3 opacity-0 group-hover:opacity-100 transition-all duration-300 rounded-full bg-foreground text-background hover:bg-foreground/90"
          >
            <ShoppingBag className="mr-2 h-4 w-4" />
            Add to Bag
          </Button>
        </div>
        
        {/* Product Info - Minimal, clean layout */}
        <div className="space-y-1">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <h3 className="font-medium text-sm line-clamp-2 leading-tight group-hover:text-foreground/70 transition-colors">
                {product.name}
              </h3>
              <p className="text-xs text-muted-foreground mt-0.5">{product.category}</p>
            </div>
          </div>
          <div className="text-base font-semibold">${product.price?.toFixed(2) || '0.00'}</div>
        </div>
      </div>
    </Link>
  )
}
