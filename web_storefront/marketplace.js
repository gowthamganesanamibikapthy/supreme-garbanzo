import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Mock Product Database matching our Core Desktop Skins
const PREMIUM_SKINS = [
  {
    id: "CYBER_HUD",
    name: "CYBER HUD: OPERATOR EDITION",
    tagline: "Futuristic neon data grid for hardcore developers & nocturnal coders.",
    price: "$4.99",
    color: "from-cyan-900 to-teal-400",
    badge: "Cyberpunk v1.2",
    features: ["Neon Radial Glow Shader", "Precision Tech Crosshairs", "Asynchronous Sonar Audio"]
  },
  {
    id: "KAWAII_PET",
    name: "KAWAII DESK TAMAGOTCHI",
    tagline: "A soft, expressive pastel friend to keep you company during crunch hours.",
    price: "$5.99",
    color: "from-pink-400 to-rose-300",
    badge: "Y2K Nostalgia",
    features: ["Interactive Eye-Blinking", "Mood Shifting Expressions", "Purr Sound Synthesis"]
  },
  {
    id: "ZEN_OASIS",
    name: "ZEN GEOMETRIC WHEEL",
    tagline: "Quiet luxury vector mechanics designed to eliminate cognitive fatigue.",
    price: "$3.99",
    color: "from-emerald-800 to-amber-600",
    badge: "Quiet Luxury",
    features: ["Golden-Ratio Kaleidoscope", "Harmonic Sound Healing Chimes", "Slower Refresh Math"]
  }
];

export default function AuraMarketplace() {
  const [selectedSkin, setSelectedSkin] = useState(null);
  const [purchaseSuccess, setPurchaseSuccess] = useState(false);
  const [username, setUsername] = useState("");

  const handlePurchase = (skinId) => {
    if (!username.trim()) {
      alert("Please link your AURA Account Username to authorize deployment.");
      return;
    }
    
    // Simulating Secure API Callback and Stripe Metadata Routing Pipeline
    setPurchaseSuccess(true);
    setTimeout(() => {
      setPurchaseSuccess(false);
      setSelectedSkin(null);
    }, 4000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-8 selection:bg-cyan-500 selection:text-slate-950">
      {/* Header section with Premium typography */}
      <header className="max-w-6xl mx-auto text-center my-12">
        <motion.h1 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl md:text-7xl font-extrabold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-pink-400 to-amber-400"
        >
          AURA MARKETPLACE
        </motion.h1>
        <p className="mt-4 text-slate-400 text-lg font-medium tracking-tight">
          Level up your workspace. High-fidelity kinetic desktop companions for your ecosystem.
        </p>
      </header>

      {/* Account Verification Floating Console */}
      <div className="max-w-md mx-auto mb-16 bg-slate-900/60 border border-slate-800 p-4 rounded-xl flex items-center gap-3 backdrop-blur-md">
        <span className="text-xl">🧿</span>
        <input 
          type="text" 
          placeholder="Enter Desktop Client Username..." 
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 w-full text-cyan-400 focus:outline-none focus:border-cyan-400 font-mono text-sm transition-all"
        />
      </div>

      {/* Liquid-Smooth Scrolling Modular Product Grid Grid */}
      <main className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        {PREMIUM_SKINS.map((skin) => (
          <motion.div
            key={skin.id}
            whileHover={{ y: -8, scale: 1.02 }}
            className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col justify-between"
          >
            {/* Animated Dynamic Vector Preview Box */}
            <div className={`h-48 bg-gradient-to-br ${skin.color} flex items-center justify-center p-6 relative`}>
              <span className="absolute top-3 right-3 bg-slate-950/80 text-xs px-2.5 py-1 rounded-full text-slate-200 font-bold border border-slate-800/40">
                {skin.badge}
              </span>
              <motion.div 
                animate={{ rotate: 360 }}
                transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
                className="w-24 h-24 rounded-full border-4 border-dashed border-white/40 flex items-center justify-center shadow-inner"
              >
                <div className="w-12 h-12 bg-slate-950 rounded-full border-2 border-white/60 shadow-lg" />
              </motion.div>
            </div>

            {/* Product Meta Core Information */}
            <div className="p-6 flex-grow flex flex-col justify-between">
              <div>
                <h3 className="text-xl font-bold tracking-tight mb-2 text-slate-100">{skin.name}</h3>
                <p className="text-sm text-slate-400 mb-4 font-light leading-relaxed">{skin.tagline}</p>
                
                <ul className="space-y-1.5 mb-6 text-xs font-medium text-slate-300">
                  {skin.features.map((f, idx) => (
                    <li key={idx} className="flex items-center gap-2">
                      <span className="text-cyan-400">⚡</span> {f}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Secure Checkout Interactive Action Layer */}
              <div className="flex items-center justify-between mt-auto">
                <span className="text-2xl font-black text-slate-50 tracking-tight">{skin.price}</span>
                <button
                  onClick={() => setSelectedSkin(skin)}
                  className="bg-slate-100 text-slate-950 hover:bg-cyan-400 hover:text-slate-950 transition-all px-4 py-2 rounded-xl text-sm font-bold tracking-tight shadow-lg"
                >
                  Deploy Shell
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </main>

      {/* Commercial Stripe Checkout Transactional Modal Overlay Overlay */}
      <AnimatePresence>
        {selectedSkin && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-4 z-50"
          >
            <motion.div 
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="bg-slate-900 border border-slate-800 max-w-md w-full rounded-2xl p-6 shadow-2xl relative"
            >
              {!purchaseSuccess ? (
                <>
                  <h4 className="text-2xl font-black mb-1 tracking-tight">SECURE SECURE CHECKOUT</h4>
                  <p className="text-xs font-mono text-slate-500 mb-6">GATEWAY IDENTIFIER: STRIPE_API_LIVE_v1</p>
                  
                  <div className="bg-slate-950 p-4 rounded-xl mb-6 border border-slate-800">
                    <div className="flex justify-between items-center text-sm mb-2">
                      <span className="text-slate-400">Target User Profile:</span>
                      <span className="font-mono text-cyan-400 font-bold">{username}</span>
                    </div>
                    <div className="flex justify-between items-center text-sm font-bold border-t border-slate-800 pt-2">
                      <span>Total Allocation:</span>
                      <span className="text-emerald-400">{selectedSkin.price}</span>
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <button 
                      onClick={() => setSelectedSkin(null)}
                      className="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-2.5 rounded-xl text-sm tracking-tight transition-all"
                    >
                      Abort Core
                    </button>
                    <button 
                      onClick={() => handlePurchase(selectedSkin.id)}
                      className="w-full bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black py-2.5 rounded-xl text-sm tracking-tight transition-all shadow-md shadow-emerald-950/40"
                    >
                      Authorize Payment
                    </button>
                  </div>
                </>
              ) : (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="text-center py-8"
                >
                  <div className="w-16 h-16 bg-emerald-500/20 border border-emerald-500 rounded-full flex items-center justify-center mx-auto text-2xl mb-4 text-emerald-400 shadow-lg animate-bounce">
                    ✓
                  </div>
                  <h4 className="text-2xl font-black text-emerald-400 tracking-tight">TRANSACTION SUCCESS</h4>
                  <p className="text-sm text-slate-300 mt-2 font-medium">
                    Skin vector manifest unlocked for user: <span className="text-cyan-400 font-mono font-bold">{username}</span>
                  </p>
                  <p className="text-xs text-slate-500 mt-4 font-light italic">
                    Jarvis is currently injecting the styling profile into your desktop client loop...
                  </p>
                </motion.div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
