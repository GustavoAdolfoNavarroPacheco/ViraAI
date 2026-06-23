"use client";

import React from "react";

export default function SettingsPlaceholderPage() {
  return (
    <div className="flex flex-col items-center justify-center p-12 min-h-[480px]">
      <div className="max-w-[480px] bg-white border border-line rounded-2xl p-10 text-center space-y-4 shadow-sm animate-fade-up">
        <span className="w-14 h-14 rounded-full bg-red-500/10 text-red-500 flex items-center justify-center mx-auto">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 13a8 8 0 0 0 0-2l2-1.5-2-3.4-2.4.6a8 8 0 0 0-1.7-1l-.3-2.5h-4l-.3 2.5a8 8 0 0 0-1.7 1l-2.4-.6-2 3.4 2 1.5a8 8 0 0 0 0 2l-2 1.5 2 3.4 2.4-.6a8 8 0 0 0 1.7 1l.3 2.5h4l.3-2.5a8 8 0 0 0 1.7-1l2.4.6 2-3.4z" />
          </svg>
        </span>
        <p className="font-mono text-[10px] tracking-widest uppercase text-red-500 font-semibold m-0">Ajustes Generales</p>
        <h3 className="font-display font-semibold text-lg text-ink m-0">Configuración</h3>
        <p className="text-xs text-slate leading-relaxed m-0">
          Ajustes de la organización, roles y permisos de usuarios, y configuración
          avanzada de latencia y autonomía del agente de Inteligencia Artificial.
        </p>
      </div>
    </div>
  );
}
