"use client";

import React from "react";

export default function ChannelsPlaceholderPage() {
  return (
    <div className="flex flex-col items-center justify-center p-12 min-h-[480px]">
      <div className="max-w-[480px] bg-white border border-line rounded-2xl p-10 text-center space-y-4 shadow-sm animate-fade-up">
        <span className="w-14 h-14 rounded-full bg-forest/8 text-forest flex items-center justify-center mx-auto">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
          </svg>
        </span>
        <p className="font-mono text-[10px] tracking-widest uppercase text-forest font-semibold m-0">Canales e Integraciones</p>
        <h3 className="font-display font-semibold text-lg text-ink m-0">Canales Conectados</h3>
        <p className="text-xs text-slate leading-relaxed m-0">
          Vincular perfiles empresariales de LinkedIn, Twitter/X, Instagram y Facebook.
          Administra tokens de acceso OAuth y mantén activas tus integraciones seguras.
        </p>
      </div>
    </div>
  );
}
