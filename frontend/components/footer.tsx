'use client'

import Link from 'next/link'
import { Github, Twitter, Mail } from 'lucide-react'

const SHOP_LINKS    = ['All Products', 'New Arrivals', 'Collections']
const SUPPORT_LINKS = ['Help Center', 'Contact', 'Privacy']

export function Footer() {
  return (
    <footer className="border-t border-border/40 bg-background">
      <div className="container mx-auto px-6 lg:px-8">

        {/* Top section */}
        <div className="py-16 grid grid-cols-1 md:grid-cols-[1fr_auto_auto_auto] gap-12 md:gap-16">

          {/* Brand column */}
          <div className="space-y-4 max-w-xs">
            <Link href="/" className="text-lg font-bold tracking-tight hover:opacity-70 transition-opacity">
              Recommend
            </Link>
            <p className="text-sm text-muted-foreground leading-relaxed">
              AI-powered shopping experience.
              <br />
              Products curated just for you.
            </p>
            {/* Social icons */}
            <div className="flex items-center gap-4 pt-2">
              {[
                { icon: Github,  href: '#', label: 'GitHub'  },
                { icon: Twitter, href: '#', label: 'Twitter' },
                { icon: Mail,    href: '#', label: 'Email'   },
              ].map(({ icon: Icon, href, label }) => (
                <a
                  key={label}
                  href={href}
                  aria-label={label}
                  className="text-muted-foreground hover:text-foreground transition-colors duration-200"
                >
                  <Icon className="h-4 w-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Shop column */}
          <div>
            <h4 className="text-xs font-semibold tracking-widest uppercase text-foreground mb-5">Shop</h4>
            <ul className="space-y-3">
              {SHOP_LINKS.map((label) => (
                <li key={label}>
                  <Link
                    href="/"
                    className="hover-line text-sm text-muted-foreground hover:text-foreground transition-colors duration-200"
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support column */}
          <div>
            <h4 className="text-xs font-semibold tracking-widest uppercase text-foreground mb-5">Support</h4>
            <ul className="space-y-3">
              {SUPPORT_LINKS.map((label) => (
                <li key={label}>
                  <a
                    href="#"
                    className="hover-line text-sm text-muted-foreground hover:text-foreground transition-colors duration-200"
                  >
                    {label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Newsletter column */}
          <div className="min-w-[200px]">
            <h4 className="text-xs font-semibold tracking-widest uppercase text-foreground mb-5">Stay updated</h4>
            <p className="text-xs text-muted-foreground mb-4 leading-relaxed">
              Get personalized picks in your inbox.
            </p>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="you@email.com"
                aria-label="Email for newsletter"
                className="flex-1 min-w-0 h-9 px-3 text-xs bg-muted/40 border border-border/60 rounded-lg outline-none focus:border-foreground/30 transition-colors placeholder:text-muted-foreground/50"
              />
              <button className="h-9 px-3 text-xs font-medium bg-foreground text-background rounded-lg hover:bg-foreground/85 transition-colors cursor-pointer">
                Join
              </button>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="py-6 border-t border-border/40 flex flex-col sm:flex-row justify-between items-center gap-3 text-[11px] text-muted-foreground">
          <p>© {new Date().getFullYear()} Recommend. All rights reserved.</p>
          <div className="flex gap-5">
            {['Terms', 'Privacy', 'Cookies'].map((label) => (
              <Link
                key={label}
                href="#"
                className="hover:text-foreground transition-colors duration-200"
              >
                {label}
              </Link>
            ))}
          </div>
        </div>

      </div>
    </footer>
  )
}
