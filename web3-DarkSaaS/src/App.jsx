import React, { useEffect } from 'react';
import { Crosshair, ChevronDown, ChevronRight } from 'lucide-react';

/* STREAMING_CHUNK:Configuring imports and styles... */
const globalStyles = `
  @import url('https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5.0.1/400.css');
  @import url('https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5.0.1/500.css');
  @import url('https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5.0.1/600.css');
  @import url('https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5.0.1/700.css');

  :root {
    --background: 260 87% 3%;
    --foreground: 40 6% 95%;
    --primary: 121 95% 76%;
    --primary-foreground: 0 0% 5%;
    --hero-heading: 40 10% 96%;
    --hero-sub: 40 6% 82%;
    --secondary: 240 4% 16%;
    --border: 240 4% 20%;
  }

  body {
    margin: 0;
    font-family: 'Geist Sans', sans-serif;
    background-color: hsl(var(--background));
    color: hsl(var(--foreground));
    -webkit-font-smoothing: antialiased;
  }

  /* Liquid Glass Reusable Utility */
  .liquid-glass {
    background: rgba(255, 255, 255, 0.01);
    background-blend-mode: luminosity;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    border: none;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
  }

  .liquid-glass::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: 1.4px;
    background: linear-gradient(180deg,
      rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
      rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
      rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
  }

  /* Marquee Animation */
  @keyframes marquee {
    0% { transform: translateX(0%); }
    100% { transform: translateX(-50%); }
  }

  .animate-marquee {
    animation: marquee 20s linear infinite;
    display: flex;
    width: max-content;
  }

  .animate-marquee:hover {
    animation-play-state: paused;
  }
`;

/* STREAMING_CHUNK:Defining constants and mock data... */
const BRANDS = [
  { name: "Vortex" },
  { name: "Nimbus" },
  { name: "Prysma" },
  { name: "Cirrus" },
  { name: "Kynder" },
  { name: "Halcyn" }
];

// Duplicated array to create a seamless infinite loop
const MARQUEE_ITEMS = [...BRANDS, ...BRANDS, ...BRANDS, ...BRANDS];

/* STREAMING_CHUNK:Building Navbar component... */
const Navbar = () => (
  <nav className="absolute top-6 left-0 right-0 z-50 mx-auto w-full max-w-[850px] px-2 sm:px-6">
    <div className="liquid-glass h-16 rounded-3xl flex items-center justify-between px-4 sm:px-6 w-full shadow-2xl shadow-black/50">
      {/* Logo Area */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-white/20 to-white/5 flex items-center justify-center liquid-glass">
          <Crosshair className="w-[18px] h-[18px] text-[hsl(var(--primary))]" />
        </div>
        <span className="text-xl font-semibold tracking-wide text-[hsl(var(--foreground))]">
          APEX
        </span>
      </div>

      {/* Desktop Links */}
      <div className="hidden md:flex items-center gap-8">
        <button className="flex items-center gap-1.5 text-base font-medium text-[hsl(var(--foreground))]/90 hover:text-[hsl(var(--foreground))] transition-colors">
          Features <ChevronDown className="w-4 h-4 opacity-70" />
        </button>
        <button className="text-base font-medium text-[hsl(var(--foreground))]/90 hover:text-[hsl(var(--foreground))] transition-colors">
          Solutions
        </button>
        <button className="text-base font-medium text-[hsl(var(--foreground))]/90 hover:text-[hsl(var(--foreground))] transition-colors">
          Plans
        </button>
        <button className="flex items-center gap-1.5 text-base font-medium text-[hsl(var(--foreground))]/90 hover:text-[hsl(var(--foreground))] transition-colors">
          Learning <ChevronDown className="w-4 h-4 opacity-70" />
        </button>
      </div>

      {/* CTA Button */}
      <button className="bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-xl px-5 py-2 text-sm font-semibold hover:bg-[hsl(var(--primary))]/90 transition-all active:scale-95 shadow-[0_0_15px_rgba(135,251,137,0.3)]">
        Sign Up
      </button>
    </div>
  </nav>
);

/* STREAMING_CHUNK:Building Marquee component... */
const SocialProofMarquee = () => (
  <div className="absolute bottom-0 left-0 w-full border-t border-[hsl(var(--border))] h-[72px] flex items-center bg-[hsl(var(--background))]/50 backdrop-blur-md z-40">
    {/* Static Label Container (Left) */}
    <div className="hidden lg:flex items-center h-full px-8 bg-gradient-to-r from-[hsl(var(--background))] via-[hsl(var(--background))] to-transparent z-20 w-[340px] shrink-0 relative">
      <span className="text-sm font-medium text-[hsl(var(--foreground))]/50 tracking-wide uppercase">
        Relied on by brands across the globe
      </span>
      {/* Fading edge for smooth transition into scroll */}
      <div className="absolute right-0 top-0 bottom-0 w-16 bg-gradient-to-r from-[hsl(var(--background))]/0 to-transparent pointer-events-none"></div>
    </div>

    {/* Scrolling Marquee Container */}
    <div 
      className="flex-1 overflow-hidden relative flex items-center h-full"
      style={{ maskImage: 'linear-gradient(to right, transparent, black 5%, black 95%, transparent)', WebkitMaskImage: 'linear-gradient(to right, transparent, black 5%, black 95%, transparent)' }}
    >
      <div className="animate-marquee items-center pl-4 lg:pl-0">
        {MARQUEE_ITEMS.map((brand, idx) => (
          <div key={idx} className="flex items-center gap-3 mr-12 group cursor-default">
            {/* Liquid glass letter icon */}
            <div className="liquid-glass w-[34px] h-[34px] rounded-lg flex items-center justify-center transition-transform group-hover:scale-110">
              <span className="text-sm font-bold text-[hsl(var(--primary))]">
                {brand.name.charAt(0)}
              </span>
            </div>
            {/* Brand Name */}
            <span className="text-base font-semibold text-[hsl(var(--foreground))]/80 group-hover:text-[hsl(var(--foreground))] transition-colors">
              {brand.name}
            </span>
          </div>
        ))}
      </div>
    </div>
  </div>
);

/* STREAMING_CHUNK:Rendering main Hero Layout... */
export default function HeroSection() {
  return (
    <>
      <style>{globalStyles}</style>
      
      <section className="relative w-full h-screen min-h-[750px] overflow-hidden flex flex-col items-center justify-center bg-[hsl(var(--background))]">
        
        {/* Background Video */}
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-cover z-0 opacity-40 mix-blend-screen pointer-events-none"
        >
          <source 
            src="./assets/background.mp4" 
            type="video/mp4" 
          />
        </video>

        {/* Deep ambient radial glow for blending video and text */}
        <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_center,transparent_0%,hsl(var(--background))_100%)] pointer-events-none"></div>

        {/* Navbar */}
        <Navbar />

        {/* Main Hero Content */}
        <main className="relative z-30 flex flex-col items-center justify-center text-center px-4 w-full mt-10">
          
          {/* Announcement Badge */}
          <div className="liquid-glass rounded-full inline-flex items-center p-1.5 pr-5 mb-8 hover:bg-white/5 transition-colors cursor-pointer group">
            <span className="ml-3 mr-3 text-sm font-medium text-[hsl(var(--hero-heading))]">
              Nova+ Launched!
            </span>
            <div className="bg-white/10 group-hover:bg-white/20 transition-colors rounded-full px-3 py-1 text-sm text-[hsl(var(--hero-heading))] flex items-center gap-1.5 font-medium shadow-sm">
              Explore <ChevronRight className="w-3.5 h-3.5" />
            </div>
          </div>

          {/* Headings */}
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-semibold tracking-tight leading-[1.05] max-w-4xl text-[hsl(var(--hero-heading))] mb-6 drop-shadow-lg">
            Accelerate Your <br className="hidden sm:block" />
            Revenue Growth Now
          </h1>
          
          <p className="text-lg sm:text-xl max-w-xl text-[hsl(var(--hero-sub))] mb-10 opacity-90 leading-relaxed">
            Drive your funnel forward with clever workflows, analytics, and seamless lead management.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center gap-4">
            {/* hero variant */}
            <button className="bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-full px-8 py-3.5 text-base font-semibold hover:bg-[hsl(var(--primary))]/90 transition-all w-full sm:w-auto shadow-[0_0_20px_rgba(135,251,137,0.2)] active:scale-95">
              Start Free Right Now
            </button>
            
            {/* heroSecondary variant */}
            <button className="liquid-glass text-[hsl(var(--foreground))] rounded-full px-8 py-3.5 text-base font-medium hover:bg-white/10 transition-all w-full sm:w-auto active:scale-95">
              Schedule a Consult
            </button>
          </div>

        </main>

        {/* Social Proof Marquee */}
        <SocialProofMarquee />

      </section>
    </>
  );
}