export default function Loading() {
  return (
    <div className="flex flex-col">
      {/* Hero Skeleton */}
      <section className="relative overflow-hidden bg-background">
        <div className="relative min-h-[85vh] flex items-center justify-center">
          <div className="container mx-auto px-6 lg:px-8 flex flex-col items-center text-center z-10 animate-pulse">
            <div className="h-24 sm:h-32 md:h-40 lg:h-48 w-3/4 bg-muted/50 rounded-2xl mb-6" />
            <div className="h-6 sm:h-8 w-2/3 bg-muted/50 rounded-xl mb-4" />
            <div className="h-6 sm:h-8 w-1/2 bg-muted/50 rounded-xl mb-12" />
            <div className="flex gap-4 mb-16">
              <div className="h-12 w-32 bg-muted/50 rounded-full" />
              <div className="h-12 w-32 bg-muted/50 rounded-full" />
            </div>
          </div>
        </div>
      </section>

      {/* Recommendations Skeleton */}
      <section className="container mx-auto px-6 lg:px-8 py-16 sm:py-20">
        <div className="h-12 w-64 bg-muted/50 rounded-xl mb-10 animate-pulse" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="animate-pulse">
              <div className="aspect-square w-full rounded-2xl bg-muted/50 mb-4" />
              <div className="h-4 w-3/4 bg-muted/50 rounded mb-2" />
              <div className="h-4 w-1/2 bg-muted/50 rounded" />
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
