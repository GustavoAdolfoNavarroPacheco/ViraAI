"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";

interface ScheduledItem {
  id: number;
  time: string;
  platform: string;
  topic: string;
  status: string;
  statusColor: string;
}

export default function DashboardPage() {
  const [greeting, setGreeting] = useState("Buenos días");
  const [dateStr, setDateStr] = useState("");

  useEffect(() => {
    const hours = new Date().getHours();
    if (hours < 12) setGreeting("Buenos días");
    else if (hours < 18) setGreeting("Buenas tardes");
    else setGreeting("Buenas noches");

    const days = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
    const months = [
      "enero", "febrero", "marzo", "abril", "mayo", "junio",
      "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ];
    const now = new Date();
    setDateStr(`${days[now.getDay()]}, ${now.getDate()} de ${months[now.getMonth()]} ${now.getFullYear()}`);
  }, []);

  const kpiItems = [
    { label: "Posts Publicados", value: "142", sub: "+12% este mes", color: "border-l-4 border-forest", iconBg: "bg-forest/10 text-forest", icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
      </svg>
    )},
    { label: "Canales Activos", value: "3", sub: "LinkedIn, Twitter, Insta", color: "border-l-4 border-mustard", iconBg: "bg-mustard/10 text-mustard-deep", icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
      </svg>
    )},
    { label: "Tasa de Engagement", value: "4.8%", sub: "+0.6% vs mes ant.", color: "border-l-4 border-ink", iconBg: "bg-ink/10 text-ink", icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
        <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
        <path d="M22 12A10 10 0 0 0 12 2v10z" />
      </svg>
    )},
    { label: "Tasa de IA Activa", value: "88.4%", sub: "Takeovers controlados", color: "border-l-4 border-red-500", iconBg: "bg-red-500/10 text-red-500", icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
      </svg>
    )}
  ];

  const scheduledPosts: ScheduledItem[] = [
    { id: 1, time: "10:30 AM", platform: "LinkedIn", topic: "Arquitectura Hexagonal en APIs modernas", status: "Aprobado", statusColor: "text-forest bg-forest/8 border border-forest/15" },
    { id: 2, time: "02:15 PM", platform: "Twitter/X", topic: "Por qué usar Celery + Redis para colas asíncronas", status: "En Revisión", statusColor: "text-mustard-deep bg-mustard/10 border border-mustard/15" },
    { id: 3, time: "Mañana", platform: "Instagram", topic: "Carrusel de consejos sobre UX Glassmorphism", status: "Borrador", statusColor: "text-slate bg-pearl border border-line" }
  ];

  const funnelItems = [
    { label: "Borradores", count: 18, pct: "90%", color: "bg-gradient-to-r from-ink to-ink-soft" },
    { label: "En Revisión", count: 8, pct: "50%", color: "bg-gradient-to-r from-ink-soft to-slate" },
    { label: "Aprobados", count: 12, pct: "75%", color: "bg-gradient-to-r from-forest to-forest-soft" },
    { label: "Programados", count: 6, pct: "40%", color: "bg-gradient-to-r from-mustard-deep to-mustard" },
    { label: "Publicados", count: 142, pct: "100%", color: "bg-gradient-to-r from-forest to-mustard" }
  ];

  return (
    <div className="space-y-8 animate-fade-up">
      {/* Welcome Banner */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-line shadow-sm">
        <div>
          <h2 className="font-display font-semibold text-xl text-ink">
            {greeting}, <span>Administrador</span>
          </h2>
          <p className="text-sm text-slate capitalize mt-1">{dateStr}</p>
        </div>
        <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-forest/6 border border-forest/15 rounded-full text-xs font-semibold text-forest relative">
          <span className="w-2 h-2 bg-forest rounded-full relative pulse-dot-glow" />
          <span>VIRA IA operando normalmente</span>
        </div>
      </div>

      {/* KPIs Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {kpiItems.map((item, idx) => (
          <div
            key={idx}
            className={`bg-white p-6 rounded-2xl shadow-sm border border-line flex flex-col justify-between transition-all hover:-translate-y-1 hover:shadow-md ${item.color}`}
          >
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-medium text-slate mb-1">{item.label}</p>
                <p className="font-display font-bold text-2xl text-ink leading-tight">{item.value}</p>
              </div>
              <span className={`w-9 h-9 rounded-xl flex items-center justify-center ${item.iconBg}`}>
                {item.icon}
              </span>
            </div>
            <p className="text-[10px] text-slate-light font-semibold mt-4">{item.sub}</p>
          </div>
        ))}
      </div>

      {/* Main Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-[1.6fr_1fr] gap-6">
        {/* Funnel Box */}
        <div className="bg-white p-8 rounded-2xl border border-line shadow-sm space-y-6">
          <div className="flex justify-between items-center pb-4 border-b border-line">
            <h3 className="font-display font-semibold text-base text-ink m-0">Embudo de Publicaciones</h3>
            <span className="text-[10px] font-mono tracking-wider uppercase text-forest bg-forest/8 px-2 py-0.5 rounded">VIRA Pipeline</span>
          </div>

          <div className="space-y-4">
            {funnelItems.map((item, idx) => (
              <div key={idx} className="grid grid-cols-[100px_1fr_40px] items-center gap-4">
                <span className="text-xs font-medium text-ink-soft">{item.label}</span>
                <div className="h-7 bg-pearl rounded-lg overflow-hidden relative">
                  <div
                    className={`h-full rounded-lg flex items-center justify-end pr-3 transition-all duration-1000 ${item.color}`}
                    style={{ width: item.pct }}
                  >
                    <span className="font-mono text-[10px] font-semibold text-white/90">{item.pct}</span>
                  </div>
                </div>
                <span className="font-mono text-right text-xs font-bold text-ink">{item.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Agenda Box */}
        <div className="bg-white p-8 rounded-2xl border border-line shadow-sm space-y-6">
          <div className="flex justify-between items-center pb-4 border-b border-line">
            <h3 className="font-display font-semibold text-base text-ink m-0">Agenda del Día</h3>
            <span className="text-[10px] font-mono tracking-wider uppercase text-mustard bg-mustard/10 px-2 py-0.5 rounded">Próximos Posts</span>
          </div>

          <div className="divide-y divide-line">
            {scheduledPosts.map((post) => (
              <div key={post.id} className="py-4.5 flex gap-4 first:pt-0 last:pb-0">
                <div className="font-mono text-xs font-semibold text-forest pt-0.5 whitespace-nowrap min-w-[64px]">
                  {post.time}
                </div>
                <div className="flex-1 space-y-1">
                  <h4 className="text-sm font-semibold text-ink leading-snug">{post.topic}</h4>
                  <p className="text-xs text-slate-light flex items-center gap-1.5">
                    <span>{post.platform}</span>
                    <span className="w-1 h-1 rounded-full bg-slate-light" />
                    <span className={`px-1.5 py-0.2 rounded-full text-[9px] font-bold uppercase ${post.statusColor}`}>{post.status}</span>
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-line shadow-sm text-center flex flex-col items-center justify-center gap-3">
          <span className="logo-mark w-12 h-12 rounded-xl bg-forest/8 text-forest flex items-center justify-center">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
              <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
              <path d="M22 12A10 10 0 0 0 12 2v10z" />
            </svg>
          </span>
          <div>
            <h4 className="text-sm font-bold text-ink mb-1">Métricas de Cuentas</h4>
            <p className="text-xs text-slate">Visualiza analíticas por red social conectada</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-line shadow-sm text-center flex flex-col items-center justify-center gap-3">
          <span className="logo-mark w-12 h-12 rounded-xl bg-mustard/12 text-mustard-deep flex items-center justify-center">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
              <path d="M12 20h9M3 20h9M3 4h18M3 8h18M3 12h18M3 16h18" />
            </svg>
          </span>
          <div>
            <h4 className="text-sm font-bold text-ink mb-1">Voces de Marca</h4>
            <p className="text-xs text-slate">Configura las personalidades de tu agente</p>
          </div>
        </div>

        <Link href="/dashboard/campaigns" className="bg-ink text-bone hover:bg-ink-soft p-6 rounded-2xl border-none shadow-sm text-center flex flex-col items-center justify-center gap-3 transition-colors cursor-pointer group">
          <span className="logo-mark w-12 h-12 rounded-xl bg-white/10 text-mustard flex items-center justify-center group-hover:scale-110 transition-transform">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
          </span>
          <div>
            <h4 className="text-sm font-bold text-white mb-1">Crear Publicación</h4>
            <p className="text-xs text-bone/60">Redacta una nueva publicación con IA</p>
          </div>
        </Link>
      </div>
    </div>
  );
}
