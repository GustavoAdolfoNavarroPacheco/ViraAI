"use client";

import React from "react";

export default function BrandVoicesPlaceholderPage() {
  return (
    <div className="flex flex-col items-center justify-center p-12 min-h-[480px]">
      <div className="max-w-[480px] bg-white border border-line rounded-2xl p-10 text-center space-y-4 shadow-sm animate-fade-up">
        <span className="w-14 h-14 rounded-full bg-ink/8 text-ink flex items-center justify-center mx-auto">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
            <circle cx="12" cy="8" r="4" />
            <path d="M18 21a6 6 0 0 0-12 0" />
          </svg>
        </span>
        <p className="font-mono text-[10px] tracking-widest uppercase text-ink font-semibold m-0">Personalidad del Agente</p>
        <h3 className="font-display font-semibold text-lg text-ink m-0">Voces de Marca</h3>
        <p className="text-xs text-slate leading-relaxed m-0">
          Configura y edita diferentes directrices estilísticas para tu agente.
          Asigna un tono formal para LinkedIn, divertido para Twitter, y define la batería
          de temas y palabras prohibidas.
        </p>
      </div>
    </div>
  );
}
