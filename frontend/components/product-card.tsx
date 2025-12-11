'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ShoppingCart, Heart } from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardFooter } from './ui/card'

interface Product {
  id: number
  name: string
  price: number
  category: string
  image_url: string
}

export function ProductCard({ product }: { product: Product }) {
  return (
    <Link href={`/product/${product.id}`}>
      <Card className="product-card overflow-hidden group cursor-pointer">
        <div className="relative aspect-square overflow-hidden bg-muted">
          <Image
            src={product.image_url}
            alt={product.name}
            fill
            className="object-cover transition-transform group-hover:scale-105"
          />
          <Button
            size="icon"
            variant="secondary"
            className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
            onClick={(e) => {
              e.preventDefault()
              // Add to wishlist
            }}
          >
            <Heart className="h-4 w-4" />
          </Button>
        </div>
        
        <CardContent className="p-4">
          <div className="text-xs text-muted-foreground mb-1">{product.category}</div>
          <h3 className="font-semibold line-clamp-2 mb-2">{product.name}</h3>
          <div className="text-xl font-bold text-primary">${product.price.toFixed(2)}</div>
        </CardContent>

        <CardFooter className="p-4 pt-0">
          <Button className="w-full" size="sm">
            <ShoppingCart className="mr-2 h-4 w-4" />
            Add to Cart
          </Button>
        </CardFooter>
      </Card>
    </Link>
  )
}
