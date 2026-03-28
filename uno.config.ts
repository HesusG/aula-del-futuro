import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    // Mac OS 7 design system
    'neo-card': 'border-2 border-black p-0 bg-white shadow-[2px_2px_0px_#000]',
    'neo-border': 'border-2 border-black',
    'neo-shadow': 'shadow-[2px_2px_0px_#000]',
    'neo-shadow-sm': 'shadow-[1px_1px_0px_#000]',
    'neo-tag': 'border-2 border-black px-2 py-1 text-sm font-bold shadow-[1px_1px_0px_#000]',
    'neo-btn': 'border-2 border-black px-4 py-2 font-bold hover:bg-black hover:text-white transition-all shadow-[2px_2px_0px_#000]',
    'term-card': 'border-2 border-black p-6 bg-white shadow-[2px_2px_0px_#000]',
    'term-code': 'bg-[#282A36] text-[#2DD4BF] font-mono p-4 rounded-sm',
    'term-highlight': 'bg-[#2DD4BF]/20 px-1',
    'term-accent': 'text-[#2DD4BF] font-bold',
    'term-section-bg': 'bg-[#282A36] text-white',
    // Color shortcuts
    'bg-banana': 'bg-[#2DD4BF]',
    'bg-coral': 'bg-[#FF6B6B]',
    'bg-sky': 'bg-[#2DD4BF]',
    'bg-grape': 'bg-[#6C5CE7]',
    'bg-ink': 'bg-[#2D3436]',
    'bg-paper': 'bg-[#FAFAFA]',
    'bg-cream': 'bg-[#F0F0F0]',
    'text-banana': 'text-[#2DD4BF]',
    'text-coral': 'text-[#FF6B6B]',
    'text-sky': 'text-[#2DD4BF]',
    'text-grape': 'text-[#6C5CE7]',
    'text-ink': 'text-[#2D3436]',
  },
  theme: {
    fontFamily: {
      heading: 'Space Grotesk, sans-serif',
      body: 'Inter, sans-serif',
      mono: 'JetBrains Mono, monospace',
    },
  },
})
