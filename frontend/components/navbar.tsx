'use client'

import Link from 'next/link'
import { ShoppingBag, User, Search } from 'lucide-react'
import { ThemeToggle } from './theme-toggle'
import { Button } from './ui/button'

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/40">
      <div className="container mx-auto flex h-14 items-center justify-between px-6 lg:px-8">
        {/* Logo - Minimal */}
        <Link href="/" className="flex items-center space-x-2 group">
          <span className="text-2xl font-semibold tracking-tight transition-colors group-hover:text-foreground/70">Recommend</span>
        </Link>

        {/* Center Navigation Links */}
        <div className="hidden md:flex items-center space-x-8">
          <Link href="/" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            Shop
          </Link>
          <Link href="/" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            New Arrivals
          </Link>
          <Link href="/" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            Collections
          </Link>
        </div>

        {/* Right Side Actions - Minimal Icons */}
        <div className="flex items-center space-x-1">
          <Button variant="ghost" size="icon" className="hover:bg-transparent">
            <Search className="h-5 w-5" />
          </Button>
          <ThemeToggle />
          <Button variant="ghost" size="icon" asChild className="hover:bg-transparent">
            <Link href="/dashboard">
              <User className="h-5 w-5" />
            </Link>
          </Button>
          <Button variant="ghost" size="icon" className="hover:bg-transparent">
            <ShoppingBag className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </nav>
  )
}
