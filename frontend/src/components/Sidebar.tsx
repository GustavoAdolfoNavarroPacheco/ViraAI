"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface NavItem {
  id: string;
  label: string;
  href: string;
  icon: React.ReactNode;
}

export default function Sidebar() {
  const pathname = usePathname();
  const [isExpanded, setIsExpanded] = useState(false);

  const navItems: NavItem[] = [
    {
      id: "dashboard",
      label: "Dashboard",
      href: "/dashboard",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
          <rect x="3" y="3" width="7" height="7" rx="1.4" />
          <rect x="14" y="3" width="7" height="7" rx="1.4" />
          <rect x="3" y="14" width="7" height="7" rx="1.4" />
          <rect x="14" y="14" width="7" height="7" rx="1.4" />
        </svg>
      ),
    },
    {
      id: "campaigns",
      label: "Campañas",
      href: "/dashboard/campaigns",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
          <rect x="3" y="7" width="18" height="12" rx="2" />
          <path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
          <line x1="3" y1="12" x2="21" y2="12" />
        </svg>
      ),
    },
    {
      id: "chat",
      label: "Bandeja de DMs",
      href: "/dashboard/chat",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
          <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H9l-4.2 3.8a.5.5 0 0 1-.8-.4V5.5z" />
        </svg>
      ),
    },
    {
      id: "calendar",
      label: "Calendario",
      href: "/dashboard/calendar",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
          <line x1="16" y1="2" x2="16" y2="6" />
          <line x1="8" y1="2" x2="8" y2="6" />
          <line x1="3" y1="10" x2="21" y2="10" />
        </svg>
      ),
    },
    {
      id: "channels",
      label: "Canales Conectados",
      href: "/dashboard/channels",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
        </svg>
      ),
    },
    {
      id: "brand-voices",
      label: "Voces de Marca",
      href: "/dashboard/brand-voices",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
          <circle cx="12" cy="8" r="4" />
          <path d="M18 21a6 6 0 0 0-12 0" />
          <polygon points="12 2 15 9 22 9 17 14 19 21 12 17 5 21 7 14 2 9 9 9 12 2" className="fill-mustard/20" />
        </svg>
      ),
    },
    {
      id: "knowledge",
      label: "Base de RAG",
      href: "/dashboard/knowledge",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
          <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H12v18H6.5A2.5 2.5 0 0 1 4 18.5z" />
          <path d="M20 5.5A2.5 2.5 0 0 0 17.5 3H12v18h5.5a2.5 2.5 0 0 0 2.5-2.5z" />
        </svg>
      ),
    },
    {
      id: "settings",
      label: "Configuración",
      href: "/dashboard/settings",
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
          <circle cx="12" cy="12" r="3" />
          <path d="M19.4 13a8 8 0 0 0 0-2l2-1.5-2-3.4-2.4.6a8 8 0 0 0-1.7-1l-.3-2.5h-4l-.3 2.5a8 8 0 0 0-1.7 1l-2.4-.6-2 3.4 2 1.5a8 8 0 0 0 0 2l-2 1.5 2 3.4 2.4-.6a8 8 0 0 0 1.7 1l.3 2.5h4l.3-2.5a8 8 0 0 0 1.7-1l2.4.6 2-3.4z" />
        </svg>
      ),
    },
  ];

  return (
    <aside
      onMouseEnter={() => setIsExpanded(true)}
      onMouseLeave={() => setIsExpanded(false)}
      className={`sidebar hidden md:flex flex-col bg-ink text-bone/78 p-6 py-5 sticky top-0 h-screen overflow-hidden shrink-0 z-90 border-r border-white/5 transition-all duration-300 ease-[cubic-bezier(0.2,0.7,0.2,1)] ${
        isExpanded ? "w-[264px]" : "w-[84px]"
      }`}
    >
      {/* Brand logo at top */}
      <div className="flex items-center gap-4 pb-6 mb-3 border-b border-white/8">
        <span className="logo-mark flex-shrink-0">
          <svg width="28" height="28" viewBox="0 0 32 32">
            <rect width="32" height="32" rx="9" fill="#D9A441" />
            <path d="M9 19a7 7 0 1 1 9 6.5" stroke="#1B3A4D" strokeWidth="2.4" fill="none" strokeLinecap="round" />
            <circle cx="19.2" cy="25.7" r="2.1" fill="#1B3A4D" />
          </svg>
        </span>
        <span
          className={`logo-text font-display font-extrabold text-2xl bg-gradient-to-r from-white to-mustard bg-clip-text text-transparent filter drop-shadow-[0_2px_4px_rgba(0,0,0,0.5)] transition-all duration-300 ${
            isExpanded ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-2 pointer-events-none"
          }`}
        >
          Vira
        </span>
      </div>

      {/* Navigation List */}
      <ul className="flex flex-col gap-1.5 flex-1 p-0 m-0 list-none">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
          return (
            <li key={item.id}>
              <Link
                href={item.href}
                className={`flex items-center gap-4.5 p-3 rounded-lg text-sm transition-all duration-300 hover:bg-white/6 hover:translate-x-1 border-l-[3px] border-transparent cursor-pointer ${
                  isActive ? "bg-mustard/12 text-mustard-soft! border-mustard! font-semibold" : "text-bone/70"
                }`}
              >
                <span className="flex-shrink-0">{item.icon}</span>
                <span
                  className={`transition-all duration-200 whitespace-nowrap ${
                    isExpanded ? "opacity-100 delay-100" : "opacity-0 pointer-events-none"
                  }`}
                >
                  {item.label}
                </span>
              </Link>
            </li>
          );
        })}
      </ul>

      {/* Footer / Tenant Badge */}
      <div
        className={`font-display text-xs font-bold tracking-widest uppercase text-center mt-auto py-2 rounded bg-gradient-to-r from-mustard via-mustard-soft to-mustard bg-[size:200%_auto] bg-clip-text text-transparent transition-all duration-300 animate-[travel_3s_linear_infinite] ${
          isExpanded ? "opacity-100 scale-100 hover:scale-104 cursor-default" : "opacity-0 scale-95 pointer-events-none"
        }`}
      >
        VIRA Agent
      </div>
    </aside>
  );
}
