'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ShoppingBag, User, Search } from 'lucide-react'
import { ThemeToggle } from './theme-toggle'
import { Button } from './ui/button'
import { CART_UPDATED_EVENT, getCartCount } from '@/lib/cart'

export function Navbar() {
  const [cartCount, setCartCount] = useState(0)
  const [scrolled, setScrolled] = useState(false)

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

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled
          ? 'bg-background/90 backdrop-blur-2xl border-b border-border/50 shadow-[0_1px_0_0_hsl(var(--border)/0.4)]'
          : 'bg-transparent border-b border-transparent'
      }`}
    >
      <div className="container mx-auto flex h-14 items-center justify-between px-6 lg:px-8">

        {/* Logo */}
        <Link
          href="/"
          className="text-lg font-bold tracking-tight hover:opacity-70 transition-opacity duration-200"
          aria-label="Recommend home"
        >
          Recommend
        </Link>

        {/* Center nav links */}
        <div className="hidden md:flex items-center gap-8">
          {[
            { href: '#all-products',          label: 'Shop' },
            { href: '#all-products',          label: 'New Arrivals' },
            { href: '#recommended-products',  label: 'For You' },
          ].map((link) => (
            <Link
              key={link.label}
              href={link.href}
              className="hover-line text-sm font-medium text-muted-foreground hover:text-foreground transition-colors duration-200"
            >
              {link.label}
            </Link>
          ))}
        </div>

        {/* Right actions */}
        <div className="flex items-center gap-0.5">
          <Button
            variant="ghost"
            size="icon"
            asChild
            className="h-9 w-9 rounded-full hover:bg-muted/60"
            aria-label="Browse products"
          >
            <Link href="#all-products">
              <Search className="h-4 w-4" />
            </Link>
          </Button>

          <ThemeToggle />

          <Button
            variant="ghost"
            size="icon"
            asChild
            className="h-9 w-9 rounded-full hover:bg-muted/60"
            aria-label="Account"
          >
            <Link href="/login">
              <User className="h-4 w-4" />
            </Link>
          </Button>

          <Button
            variant="ghost"
            size="icon"
            asChild
            className="h-9 w-9 rounded-full hover:bg-muted/60 relative"
            aria-label={`Cart${cartCount > 0 ? `, ${cartCount} items` : ''}`}
          >
            <Link href="/cart">
              <ShoppingBag className="h-4 w-4" />
              {cartCount > 0 && (
                <span className="absolute -top-0.5 -right-0.5 min-w-[16px] h-4 px-0.5 rounded-full bg-foreground text-background text-[9px] font-semibold leading-4 text-center tabular-nums">
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
