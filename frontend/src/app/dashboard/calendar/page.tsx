"use client";

import React from "react";

export default function CalendarPlaceholderPage() {
  return (
    <div className="flex flex-col items-center justify-center p-12 min-h-[480px]">
      <div className="max-w-[480px] bg-white border border-line rounded-2xl p-10 text-center space-y-4 shadow-sm animate-fade-up">
        <span className="w-14 h-14 rounded-full bg-mustard/12 text-mustard-deep flex items-center justify-center mx-auto">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
        </span>
        <p className="font-mono text-[10px] tracking-widest uppercase text-mustard-deep font-semibold m-0">Módulo Programador</p>
        <h3 className="font-display font-semibold text-lg text-ink m-0">Calendario Editorial</h3>
        <p className="text-xs text-slate leading-relaxed m-0">
          Visualiza todas tus publicaciones en una cuadrícula semanal o mensual.
          Programa posts con arrastrar y soltar, y analiza tus horarios de mayor impacto.
        </p>
      </div>
    </div>
  );
}
