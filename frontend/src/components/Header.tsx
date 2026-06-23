"use client";

import React from "react";
import { useRouter, usePathname } from "next/navigation";

export default function Header() {
  const router = useRouter();
  const pathname = usePathname();

  // Determine page title based on path
  const getPageTitle = () => {
    if (pathname.includes("/chat")) return "Bandeja de DMs";
    if (pathname.includes("/campaigns")) return "Campañas Editoriales";
    if (pathname.includes("/calendar")) return "Calendario de Publicaciones";
    if (pathname.includes("/channels")) return "Canales Conectados";
    if (pathname.includes("/brand-voices")) return "Voces de Marca";
    if (pathname.includes("/knowledge")) return "Base de Conocimiento RAG";
    if (pathname.includes("/settings")) return "Configuración del Sistema";
    return "Dashboard";
  };

  const handleLogout = () => {
    router.push("/login");
  };

  return (
    <header className="h-[72px] bg-white border-b border-line flex items-center justify-between px-8 select-none z-40">
      {/* Page Title */}
      <div className="flex items-center gap-3">
        {/* Mobile menu trigger */}
        <button className="md:hidden p-1.5 rounded-lg text-slate hover:bg-pearl hover:text-ink transition-all">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
        <h1 className="font-display font-semibold text-lg text-ink m-0">
          {getPageTitle()}
        </h1>
      </div>

      {/* Topbar Actions */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="p-1.5 rounded-lg text-slate hover:bg-pearl hover:text-ink transition-colors cursor-pointer" aria-label="Notificaciones">
          <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
            <path d="M18 8a6 6 0 1 0-12 0c0 5-2 6-2 6h16s-2-1-2-6" />
            <path d="M10 20a2 2 0 0 0 4 0" />
          </svg>
        </button>

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="p-1.5 rounded-lg text-slate hover:bg-pearl hover:text-ink transition-colors cursor-pointer"
          aria-label="Cerrar sesión"
        >
          <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
        </button>

        {/* User Profile Info */}
        <div className="flex items-center gap-3 pl-4 border-l border-line">
          <span className="w-[34px] h-[34px] rounded-full bg-gradient-to-tr from-ink to-forest text-bone font-display font-semibold text-xs flex items-center justify-center">
            AD
          </span>
          <div className="text-left hidden sm:block">
            <p className="font-sans font-semibold text-xs text-ink leading-tight m-0">Administrador</p>
            <p className="font-sans text-[10px] text-slate leading-tight m-0">Social Media Mgr</p>
          </div>
        </div>
      </div>
    </header>
  );
}
