# UI Wireframe & Component Specification
**E-commerce Recommendation System - Frontend Architecture**

---

## 📐 Design System

### Color Palette
- **Primary**: `#00ADB5` (Teal) - CTAs, highlights, recommendations badge
- **Background**: `#FAFAFA` (Light) / `#1A1A2E` (Dark)
- **Text**: `#2C3E50` (Dark) / `#E8E8E8` (Light mode)
- **Accent**: `#FF6B6B` (Sale tags, wishlist hearts)
- **Muted**: `#95A5A6` (Secondary text, borders)

### Typography
- **Font Family**: Inter (primary), system-ui fallback
- **Headings**: Bold, 32px–48px (H1), 24px–32px (H2)
- **Body**: Regular, 16px (desktop), 14px (mobile)
- **Labels**: Medium, 12px–14px

### Spacing
- Container max-width: 1280px
- Grid gap: 24px (desktop), 16px (mobile)
- Section padding: 80px vertical, 40px mobile

---

## 🎨 Page Layouts & Wireframes

### 1. Home Page (`/`)

```
┌─────────────────────────────────────────────────────────────┐
│  Navbar: [Logo] [Search Bar] [Account] [Cart] [Theme]      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Hero Section (Full-width gradient background)             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ✨ AI-Powered Recommendations                       │   │
│  │                                                       │   │
│  │  Discover Products Tailored Just for You             │   │
│  │  [Large heading, centered, max-width 800px]          │   │
│  │                                                       │   │
│  │  Experience shopping with advanced AI...             │   │
│  │  [Subheading, 18px, muted color]                     │   │
│  │                                                       │   │
│  │  [Explore Products →] [View Recommendations]         │   │
│  │                                                       │   │
│  │  Stats:  100+ Products | 95% Accuracy | 50+ Users    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✨ Recommended for You                                    │
│  [Section heading with sparkle icon]                       │
│                                                             │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              │
│  │ Image  │ │ Image  │ │ Image  │ │ Image  │              │
│  │        │ │        │ │        │ │        │              │
│  │Category│ │Category│ │Category│ │Category│              │
│  │ Name   │ │ Name   │ │ Name   │ │ Name   │              │
│  │$49.99  │ │$79.99  │ │$29.99  │ │$99.99  │              │
│  │[+ Cart]│ │[+ Cart]│ │[+ Cart]│ │[+ Cart]│              │
│  └────────┘ └────────┘ └────────┘ └────────┘              │
│  [Horizontal scroll on mobile, grid on desktop]            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  All Products                                              │
│  [Filters: Category dropdown | Sort by | Price range]      │
│                                                             │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                       │
│  │Prod│ │Prod│ │Prod│ │Prod│ │Prod│                       │
│  │uct │ │uct │ │uct │ │uct │ │uct │                       │
│  └────┘ └────┘ └────┘ └────┘ └────┘                       │
│  [Responsive grid: 4 cols desktop, 2 mobile]               │
│  [Pagination or infinite scroll]                           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Footer: [About | Links | Social] © 2025 RecommendAI       │
└─────────────────────────────────────────────────────────────┘
```

**Interactions:**
- Hero CTA buttons: Smooth scroll to sections (Framer Motion)
- Product cards: Hover scale + shadow increase
- Lazy image loading with skeleton loaders
- Navbar sticky on scroll with backdrop blur

---

### 2. Product Detail Page (`/product/[id]`)

```
┌─────────────────────────────────────────────────────────────┐
│  Navbar (sticky)                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐  ┌──────────────────────────────┐    │
│  │                  │  │  Category > Subcategory       │    │
│  │  Product Image   │  │                               │    │
│  │  (Large, 600px)  │  │  Product Name                 │    │
│  │                  │  │  [H1, bold, 32px]             │    │
│  │  [Thumbnails]    │  │                               │    │
│  │   ⬜⬜⬜⬜        │  │  ⭐⭐⭐⭐⭐ (4.5) 120 reviews │    │
│  │                  │  │                               │    │
│  │                  │  │  $79.99  [Sale badge -20%]    │    │
│  │                  │  │                               │    │
│  └──────────────────┘  │  Description paragraph...     │    │
│                        │                               │    │
│                        │  [- 1 +] [Add to Cart]        │    │
│                        │  [❤ Add to Wishlist]          │    │
│                        └──────────────────────────────┘    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  You May Also Like (Similar Products)                      │
│  [Horizontal carousel with 5 cards]                        │
│  ← ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ →                   │
│    │Sim │ │Sim │ │Sim │ │Sim │ │Sim │                     │
│    └────┘ └────┘ └────┘ └────┘ └────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Interactions:**
- Image gallery with zoom on hover
- Quantity selector with +/− buttons
- Similar products API call on mount, cached
- "Add to Cart" toast notification

---

### 3. User Dashboard (`/dashboard`)

```
┌─────────────────────────────────────────────────────────────┐
│  Navbar                                                     │
├─────────────────────────────────────────────────────────────┤
│  Sidebar (Desktop) / Tabs (Mobile)                          │
│  ┌─────────────┐  ┌───────────────────────────────────┐    │
│  │ Dashboard   │  │  Welcome back, John! 👋            │    │
│  │ ▸ For You   │  │                                    │    │
│  │   History   │  │  Personalized Recommendations      │    │
│  │   Wishlist  │  │  [Grid of recommended products]    │    │
│  │   Settings  │  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐      │    │
│  └─────────────┘  │  │Rec │ │Rec │ │Rec │ │Rec │      │    │
│                   │  └────┘ └────┘ └────┘ └────┘      │    │
│                   │                                    │    │
│                   │  Recently Viewed                   │    │
│                   │  [Horizontal scroll]               │    │
│                   │                                    │    │
│                   │  Saved Items (Wishlist)            │    │
│                   │  [Grid with remove option]         │    │
│                   └───────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**Interactions:**
- Fetch recommendations from `/api/v1/recommend/{user_id}`
- Track clicks to refine future recommendations
- Skeleton loaders during data fetch
- Smooth transitions between tabs

---

### 4. Admin Dashboard (`/admin`)

```
┌─────────────────────────────────────────────────────────────┐
│  Navbar (Admin mode indicator)                             │
├─────────────────────────────────────────────────────────────┤
│  Admin Dashboard                                            │
│                                                             │
│  ┌─────────────┬──────────────────────────────────────┐    │
│  │ Metrics     │  A/B Test Results                     │    │
│  │             │                                        │    │
│  │ Products    │  Variant A vs B Comparison            │    │
│  │ • Total: 100│  ┌─────────────────────────────────┐  │    │
│  │ • Active: 95│  │ [Bar chart: CTR comparison]     │  │    │
│  │             │  │  Variant A: 5.2%                │  │    │
│  │ Users       │  │  Variant B: 6.8% ✅ Winner      │  │    │
│  │ • Total: 50 │  └─────────────────────────────────┘  │    │
│  │ • Cohort A  │                                        │    │
│  │ • Cohort B  │  ┌─────────────────────────────────┐  │    │
│  │             │  │ [Line chart: CTR over time]     │  │    │
│  │ Performance │  │                                  │  │    │
│  │ • Avg API   │  └─────────────────────────────────┘  │    │
│  │   Latency:  │                                        │    │
│  │   245ms ✅  │  Conversion Rates                     │    │
│  │             │  [Pie chart or table]                 │    │
│  └─────────────┴──────────────────────────────────────┘    │
│                                                             │
│  Recent Activity Feed                                      │
│  • User X clicked Product Y (Variant A)                    │
│  • User Z purchased Product W (Variant B)                  │
│  [Real-time updates via polling or WebSocket]              │
└─────────────────────────────────────────────────────────────┘
```

**Interactions:**
- Fetch A/B test data from `/api/v1/ab-test/results`
- Chart.js or Recharts for visualizations
- Filter by date range (dropdown)
- Export CSV button

---

## 🧩 Component Tree

```
App
├── Layout
│   ├── Navbar
│   │   ├── Logo
│   │   ├── SearchBar
│   │   ├── AccountDropdown
│   │   ├── CartIcon
│   │   └── ThemeToggle
│   ├── Main (children)
│   └── Footer
│       ├── Links (About, Support, etc.)
│       └── SocialIcons
│
├── Pages
│   ├── Home
│   │   ├── Hero
│   │   │   ├── Heading
│   │   │   ├── CTAButtons
│   │   │   └── StatsGrid
│   │   ├── RecommendationSection
│   │   │   └── ProductCard[]
│   │   └── ProductGrid
│   │       ├── FilterBar
│   │       └── ProductCard[]
│   │
│   ├── ProductDetail
│   │   ├── ImageGallery
│   │   ├── ProductInfo
│   │   │   ├── Title, Price, Rating
│   │   │   ├── QuantitySelector
│   │   │   ├── AddToCartButton
│   │   │   └── WishlistButton
│   │   └── SimilarProductsCarousel
│   │
│   ├── Dashboard
│   │   ├── Sidebar (or Tabs)
│   │   ├── PersonalizedRecommendations
│   │   ├── RecentlyViewed
│   │   └── Wishlist
│   │
│   └── AdminDashboard
│       ├── MetricsCards
│       ├── ABTestCharts (Chart.js)
│       ├── ActivityFeed
│       └── ExportButton
│
└── Shared Components
    ├── ProductCard
    │   ├── Image (Next/Image)
    │   ├── Badge (Sale, New, etc.)
    │   ├── Title, Category, Price
    │   ├── AddToCartButton
    │   └── WishlistButton
    ├── Button (variants: primary, secondary, ghost, outline)
    ├── Card (shadcn/ui)
    ├── Skeleton (loading states)
    ├── Toast (notifications)
    ├── Modal/Dialog
    └── Badge
```

---

## 🎭 Animation & Transitions (Framer Motion)

### Page Transitions
```jsx
const pageVariants = {
  initial: { opacity: 0, y: 20 },
  enter: { opacity: 1, y: 0, transition: { duration: 0.4 } },
  exit: { opacity: 0, y: -20, transition: { duration: 0.3 } }
}
```

### Product Card Hover
```jsx
<motion.div
  whileHover={{ scale: 1.03, y: -4 }}
  transition={{ type: "spring", stiffness: 300 }}
>
  {/* Card content */}
</motion.div>
```

### Stagger Children (Grid)
```jsx
const containerVariants = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.05
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, scale: 0.9 },
  show: { opacity: 1, scale: 1 }
}
```

---

## 📱 Responsive Breakpoints

```css
/* Mobile: < 640px */
.product-grid { grid-template-columns: repeat(2, 1fr); }

/* Tablet: 640px - 1024px */
@media (min-width: 640px) {
  .product-grid { grid-template-columns: repeat(3, 1fr); }
}

/* Desktop: > 1024px */
@media (min-width: 1024px) {
  .product-grid { grid-template-columns: repeat(4, 1fr); }
}

/* Large: > 1280px */
@media (min-width: 1280px) {
  .product-grid { grid-template-columns: repeat(5, 1fr); }
}
```

---

## 🔄 State Management (Zustand)

```tsx
// stores/cart.ts
interface CartStore {
  items: CartItem[]
  addItem: (product: Product) => void
  removeItem: (id: number) => void
  clearCart: () => void
}

// stores/user.ts
interface UserStore {
  user: User | null
  token: string | null
  setUser: (user: User, token: string) => void
  logout: () => void
}
```

---

## ✅ Implementation Checklist

### Core Components (Priority 1)
- [x] Navbar with search, account, cart
- [x] Footer with links and social
- [x] Hero section with animations
- [x] ProductCard with hover effects
- [x] ProductGrid with filtering
- [x] RecommendationSection

### Pages (Priority 2)
- [x] Home page layout
- [ ] Product detail page
- [ ] User dashboard
- [ ] Admin dashboard
- [ ] Login/Register modal

### Features (Priority 3)
- [ ] Shopping cart functionality
- [ ] Wishlist/favorites
- [ ] Search with autocomplete
- [ ] Filter & sort products
- [ ] A/B test tracking
- [ ] Dark mode toggle

### Polish (Priority 4)
- [ ] Skeleton loaders everywhere
- [ ] Toast notifications
- [ ] Error boundaries
- [ ] 404 page
- [ ] Loading states
- [ ] Image optimization

---

## 🎨 Figma/Mockup Notes

If handing off to a designer:
1. Use the color palette and typography above
2. Focus on micro-interactions (hover, click feedback)
3. Ensure 8px grid system for spacing
4. Export assets as SVG or WebP
5. Provide component variants (default, hover, active, disabled)

---

**This wireframe is implementation-ready. All components are mapped to existing code in `frontend/components/`.**
