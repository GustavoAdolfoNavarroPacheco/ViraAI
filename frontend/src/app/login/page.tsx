"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";

type FormView = "login" | "register" | "forgot";

export default function LoginPage() {
  const router = useRouter();
  const [view, setView] = useState<FormView>("login");
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  
  // Status states
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [toastMsg, setToastMsg] = useState("");

  const triggerToast = (msg: string) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(""), 3000);
  };

  const handleLoginSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      triggerToast("Por favor complete todos los campos.");
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setSuccess(true);
      setTimeout(() => {
        router.push("/dashboard");
      }, 550);
    }, 900);
  };

  const handleRegisterSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !password || !confirmPassword) {
      triggerToast("Por favor complete todos los campos.");
      return;
    }
    if (password !== confirmPassword) {
      triggerToast("Las contraseñas no coinciden.");
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setSuccess(true);
      setTimeout(() => {
        setLoading(false);
        setSuccess(false);
        setView("login");
        triggerToast("Cuenta creada con éxito. Ya puedes iniciar sesión.");
      }, 600);
    }, 900);
  };

  const handleForgotSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      triggerToast("Por favor ingrese su correo.");
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
      triggerToast("Enlace de recuperación enviado al correo.");
    }, 900);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-[minmax(380px,42%)_1fr] min-h-screen animate-screen-in">
      {/* BRAND PANEL */}
      <div className="brand-panel hidden md:flex flex-col justify-between p-12 text-bone relative overflow-hidden bg-gradient-to-br from-ink to-ink-deep">
        {/* Glow effect */}
        <div className="absolute w-[520px] height-[520px] right-[-220px] top-[-220px] rounded-full bg-radial from-mustard/18 to-transparent pointer-events-none" />
        
        {/* Top Logo */}
        <div className="flex items-center gap-3 relative z-10">
          <span className="logo-mark w-8 h-8 rounded-lg bg-mustard flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 32 32">
              <path d="M9 19a7 7 0 1 1 9 6.5" stroke="#1B3A4D" strokeWidth="2.4" fill="none" strokeLinecap="round" />
              <circle cx="19.2" cy="25.7" r="2.1" fill="#1B3A4D" />
            </svg>
          </span>
          <span className="logo-text font-display font-bold text-xl tracking-wide">vira</span>
        </div>

        {/* Middle Copy and Flow */}
        <div className="relative z-10 max-w-[420px] my-auto">
          <h1 className="font-display font-semibold text-3xl lg:text-4xl leading-[1.32] mb-4">
            Tu generación de contenido y publicación, potenciada por IA.
          </h1>
          <p className="text-sm leading-relaxed text-bone/70 mb-8 max-w-[380px]">
            VIRA redacta tus posts en base a tu tono de marca, programa en tus canales y responde interacciones en vivo automáticamente.
          </p>

          {/* SVG Dot Flow Animation */}
          <div className="relative w-[380px] h-[130px]" aria-hidden="true">
            <svg viewBox="0 0 380 130" width="380" height="130">
              <path d="M28,98 C108,38 150,150 198,73 C248,-2 298,90 368,38" fill="none" stroke="rgba(255,255,255,0.18)" strokeWidth="1.5" />
            </svg>
            <span className="absolute w-2 h-2 rounded-full bg-mustard shadow-[0_0_0_4px_rgba(217,164,65,0.18)]" style={{ left: "24px", top: "94px" }} />
            <span className="absolute w-2 h-2 rounded-full bg-mustard shadow-[0_0_0_4px_rgba(217,164,65,0.18)]" style={{ left: "194px", top: "69px" }} />
            <span className="absolute w-2 h-2 rounded-full bg-mustard shadow-[0_0_0_4px_rgba(217,164,65,0.18)]" style={{ left: "364px", top: "34px" }} />
            
            <span className="absolute font-mono text-[10px] tracking-widest uppercase text-bone/50" style={{ left: "0px", top: "108px" }}>Idea</span>
            <span className="absolute font-mono text-[10px] tracking-widest uppercase text-bone/50" style={{ left: "166px", top: "18px" }}>Redacción</span>
            <span className="absolute font-mono text-[10px] tracking-widest uppercase text-bone/50" style={{ left: "300px", top: "46px" }}>Publicación</span>
          </div>
        </div>

        {/* Bottom Workspace Badge */}
        <div className="relative z-10">
          <div className="inline-flex items-center gap-3 p-3 pl-2 bg-white/6 border border-white/13 rounded-xl">
            <span className="w-8 h-8 rounded-lg bg-mustard text-ink-deep flex items-center justify-center font-display font-bold text-xs">
              VI
            </span>
            <div className="text-left leading-tight">
              <p className="font-mono text-[10px] tracking-widest uppercase text-bone/45 m-0">Agente Activo</p>
              <p className="text-xs font-semibold m-0">VIRA Workspace</p>
            </div>
          </div>
        </div>
      </div>

      {/* FORM PANEL */}
      <div className="flex items-center justify-center p-8 bg-bone">
        <div className="w-full max-w-[380px]">
          <span className="font-display font-extrabold text-5xl tracking-wide bg-gradient-to-r from-mustard via-mustard-soft to-mustard-deep bg-clip-text text-transparent mb-8 block leading-none drop-shadow-[0_2px_8px_rgba(217,164,65,0.25)]">
            Vira
          </span>

          {/* Form Header */}
          <div className="mb-8">
            <p className="font-mono text-[11px] tracking-widest uppercase text-forest mb-2">
              {view === "login" ? "Acceso al workspace" : view === "register" ? "Nuevo en vira" : "Recuperar acceso"}
            </p>
            <h2 className="font-display font-semibold text-2xl mb-1">
              {view === "login" ? "Inicia sesión" : view === "register" ? "Crea tu cuenta" : "¿Olvidaste tu contraseña?"}
            </h2>
            <p className="text-sm text-slate">
              {view === "login" ? "Consola de control de redes" : view === "register" ? "Únete al workspace de VIRA" : "Te enviaremos un enlace para restablecerla"}
            </p>
          </div>

          {/* FORMS */}
          <div className="relative">
            {/* LOGIN VIEW */}
            {view === "login" && (
              <form onSubmit={handleLoginSubmit} className="animate-fade-up space-y-5">
                <div className="relative">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder=" "
                    className="floating-label-input w-full p-4 pt-5 pb-2 border-1.4 border-line rounded-lg font-sans text-sm text-ink bg-white focus:border-forest-soft focus:shadow-[0_0_0_3px_rgba(63,102,87,0.12)] focus:outline-none transition-all"
                  />
                  <label className="absolute left-4 top-4 text-sm text-slate-light pointer-events-none transition-all bg-white px-1">
                    Correo corporativo
                  </label>
                </div>

                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder=" "
                    className="floating-label-input w-full p-4 pt-5 pb-2 border-1.4 border-line rounded-lg font-sans text-sm text-ink bg-white focus:border-forest-soft focus:shadow-[0_0_0_3px_rgba(63,102,87,0.12)] focus:outline-none transition-all"
                  />
                  <label className="absolute left-4 top-4 text-sm text-slate-light pointer-events-none transition-all bg-white px-1">
                    Contraseña
                  </label>
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3.5 p-1 text-slate-light hover:text-forest transition-colors"
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M1.5 12S5 5 12 5s10.5 7 10.5 7-3.5 7-10.5 7S1.5 12 1.5 12z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  </button>
                </div>

                <div className="flex justify-end mt-[-8px]">
                  <button
                    type="button"
                    onClick={() => setView("forgot")}
                    className="text-xs font-semibold text-forest hover:underline"
                  >
                    ¿Olvidaste tu contraseña?
                  </button>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full py-4 px-5 rounded-lg border-none bg-ink text-bone font-semibold text-sm flex items-center justify-center gap-2 shadow-sm transition-all hover:bg-ink-soft hover:shadow-md active:scale-98 cursor-pointer ${
                    success ? "bg-forest!" : ""
                  }`}
                >
                  <span className={loading ? "opacity-55" : ""}>{success ? "Ingresando..." : "Iniciar sesión"}</span>
                  {loading && <span className="w-4 h-4 rounded-full border-2 border-bone/35 border-t-bone animate-spin-fast" />}
                  {success && (
                    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="4 12 9 17 20 6" />
                    </svg>
                  )}
                </button>

                <p className="text-center text-xs text-slate mt-5">
                  ¿No tienes una cuenta?{" "}
                  <button type="button" onClick={() => setView("register")} className="text-forest font-semibold hover:underline bg-transparent border-none p-0 cursor-pointer">
                    Regístrate
                  </button>
                </p>
              </form>
            )}

            {/* REGISTER VIEW */}
            {view === "register" && (
              <form onSubmit={handleRegisterSubmit} className="animate-fade-up space-y-5">
                <div className="relative">
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder=" "
                    className="floating-label-input w-full p-4 pt-5 pb-2 border-1.4 border-line rounded-lg font-sans text-sm text-ink bg-white focus:border-forest-soft focus:shadow-[0_0_0_3px_rgba(63,102,87,0.12)] focus:outline-none transition-all"
                  />
                  <label className="absolute left-4 top-4 text-sm text-slate-light pointer-events-none transition-all bg-white px-1">
                    Nombre completo
                  </label>
                </div>

                <div className="relative">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder=" "
                    className="floating-label-input w-full p-4 pt-5 pb-2 border-1.4 border-line rounded-lg font-sans text-sm text-ink bg-white focus:border-forest-soft focus:shadow-[0_0_0_3px_rgba(63,102,87,0.12)] focus:outline-none transition-all"
                  />
                  <label className="absolute left-4 top-4 text-sm text-slate-light pointer-events-none transition-all bg-white px-1">
                    Correo corporativo
                  </label>
                </div>

                <div className="relative">
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder=" "
                    className="floating-label-input w-full p-4 pt-5 pb-2 border-1.4 border-line rounded-lg font-sans text-sm text-ink bg-white focus:border-forest-soft focus:shadow-[0_0_0_3px_rgba(63,102,87,0.12)] focus:outline-none transition-all"
                  />
                  <label className="absolute left-4 top-4 text-sm text-slate-light pointer-events-none transition-all bg-white px-1">
                    Contraseña
                  </label>
                </div>

                <div className="relative">
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder=" "
                    className="floating-label-input w-full p-4 pt-5 pb-2 border-1.4 border-line rounded-lg font-sans text-sm text-ink bg-white focus:border-forest-soft focus:shadow-[0_0_0_3px_rgba(63,102,87,0.12)] focus:outline-none transition-all"
                  />
                  <label className="absolute left-4 top-4 text-sm text-slate-light pointer-events-none transition-all bg-white px-1">
                    Confirmar contraseña
                  </label>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full py-4 px-5 rounded-lg border-none bg-ink text-bone font-semibold text-sm flex items-center justify-center gap-2 shadow-sm transition-all hover:bg-ink-soft hover:shadow-md active:scale-98 cursor-pointer ${
                    success ? "bg-forest!" : ""
                  }`}
                >
                  <span className={loading ? "opacity-55" : ""}>{success ? "Creando..." : "Crear cuenta"}</span>
                  {loading && <span className="w-4 h-4 rounded-full border-2 border-bone/35 border-t-bone animate-spin-fast" />}
                  {success && (
                    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="4 12 9 17 20 6" />
                    </svg>
                  )}
                </button>

                <p className="text-center text-xs text-slate mt-5">
                  ¿Ya tienes una cuenta?{" "}
                  <button type="button" onClick={() => setView("login")} className="text-forest font-semibold hover:underline bg-transparent border-none p-0 cursor-pointer">
                    Inicia sesión
                  </button>
                </p>
              </form>
            )}

            {/* FORGOT VIEW */}
            {view === "forgot" && (
              <form onSubmit={handleForgotSubmit} className="animate-fade-up space-y-5">
                <div className="relative">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder=" "
                    className="floating-label-input w-full p-4 pt-5 pb-2 border-1.4 border-line rounded-lg font-sans text-sm text-ink bg-white focus:border-forest-soft focus:shadow-[0_0_0_3px_rgba(63,102,87,0.12)] focus:outline-none transition-all"
                  />
                  <label className="absolute left-4 top-4 text-sm text-slate-light pointer-events-none transition-all bg-white px-1">
                    Correo corporativo
                  </label>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full py-4 px-5 rounded-lg border-none bg-ink text-bone font-semibold text-sm flex items-center justify-center gap-2 shadow-sm transition-all hover:bg-ink-soft hover:shadow-md active:scale-98 cursor-pointer ${
                    success ? "bg-forest!" : ""
                  }`}
                >
                  <span className={loading ? "opacity-55" : ""}>{success ? "Enviado" : "Enviar enlace de recuperación"}</span>
                  {loading && <span className="w-4 h-4 rounded-full border-2 border-bone/35 border-t-bone animate-spin-fast" />}
                  {success && (
                    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="4 12 9 17 20 6" />
                    </svg>
                  )}
                </button>

                <p className="text-center text-xs text-slate mt-5">
                  <button type="button" onClick={() => setView("login")} className="text-forest font-semibold hover:underline bg-transparent border-none p-0 cursor-pointer">
                    Volver al inicio de sesión
                  </button>
                </p>
              </form>
            )}
          </div>
        </div>
      </div>

      {/* TOAST NOTIFICATION */}
      {toastMsg && (
        <div className="fixed left-1/2 bottom-7 -translate-x-1/2 bg-ink-deep text-bone px-5 py-3.5 rounded-xl text-sm shadow-lg flex items-center gap-2.5 z-[200] animate-fade-up">
          <span className="w-1.5 h-1.5 rounded-full bg-mustard flex-shrink-0" />
          <span>{toastMsg}</span>
        </div>
      )}
    </div>
  );
}
