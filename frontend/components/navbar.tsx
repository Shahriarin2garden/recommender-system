'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ShoppingBag, User, Search } from 'lucide-react'
import { ThemeToggle } from './theme-toggle'
import { Button } from './ui/button'
import { CART_UPDATED_EVENT, getCartCount } from '@/lib/cart'

export function Navbar() {
  const [cartCount, setCartCount] = useState(0)

  useEffect(() => {
    const syncCartCount = () => setCartCount(getCartCount())

    syncCartCount()
    window.addEventListener('storage', syncCartCount)
    window.addEventListener(CART_UPDATED_EVENT, syncCartCount)

    return () => {
      window.removeEventListener('storage', syncCartCount)
      window.removeEventListener(CART_UPDATED_EVENT, syncCartCount)
    }
  }, [])

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/40">
      <div className="container mx-auto flex h-14 items-center justify-between px-6 lg:px-8">
        {/* Logo - Minimal */}
        <Link href="/" className="flex items-center space-x-2 group">
          <span className="text-2xl font-semibold tracking-tight transition-colors group-hover:text-foreground/70">Recommend</span>
        </Link>

        {/* Center Navigation Links */}
        <div className="hidden md:flex items-center space-x-8">
          <Link href="#all-products" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            Shop
          </Link>
          <Link href="#all-products" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            New Arrivals
          </Link>
          <Link href="#recommended-products" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            Collections
          </Link>
        </div>

        {/* Right Side Actions - Minimal Icons */}
        <div className="flex items-center space-x-1">
          <Button variant="ghost" size="icon" asChild className="hover:bg-transparent">
            <Link href="#all-products" aria-label="Browse products">
              <Search className="h-5 w-5" />
            </Link>
          </Button>
          <ThemeToggle />
          <Button variant="ghost" size="icon" asChild className="hover:bg-transparent">
            <Link href="/login">
              <User className="h-5 w-5" />
            </Link>
          </Button>
          <Button variant="ghost" size="icon" asChild className="hover:bg-transparent relative">
            <Link href="/cart" aria-label="Open cart">
              <ShoppingBag className="h-5 w-5" />
              {cartCount > 0 && (
                <span className="absolute -top-1 -right-1 min-w-4 h-4 px-1 rounded-full bg-foreground text-background text-[10px] leading-4 text-center">
                  {cartCount}
                </span>
              )}
            </Link>
          </Button>
        </div>
      </div>
    </nav>
  )
}
