"use client";

import React, { useState, useEffect, useRef } from "react";
import { api } from "@/lib/api";

interface Message {
  type: "in" | "out-sora" | "out-human" | "sys";
  time: string;
  text: string;
}

interface ChatContact {
  name: string;
  initials: string;
  color: string;
  role: string;
  score: string;
  scoreColor: string;
  time: string;
  lastMsg: string;
  status: "sora" | "manual" | "wait" | "blocked";
  tags: string[];
  warnTags: string[];
  analysis: string;
  email: string;
  phone: string;
  messages: Message[];
  timerSeconds?: number;
  timerActive?: boolean;
}

export default function ChatPage() {
  const [contacts, setContacts] = useState<Record<string, ChatContact>>({
    "Carlos Mendoza": {
      name: "Carlos Mendoza",
      initials: "CM", color: "#2C4F66", role: "Seguidor Activo / Lead", score: "94%",
      scoreColor: "var(--color-forest)", time: "Ahora", lastMsg: "Entendido, allí estaré puntual.",
      status: "sora",
      tags: ["Interés en AI", "LinkedIn Activo", "Ubicación ideal"],
      warnTags: ["Falta validar correo"],
      analysis: "Usuario interesado en adquirir licencias de VIRA. Tono respetuoso y disposición absoluta. Confirmó presupuesto.",
      email: "carlos.mendoza@email.com", phone: "+57 300 123 4567",
      timerSeconds: 300,
      timerActive: false,
      messages: [
        { type: "sys", time: "09:15 AM", text: "VIRA IA ha iniciado la interacción automática" },
        { type: "out-sora", time: "09:15 AM", text: "¡Hola Carlos! Soy VIRA, asistente de automatización. Veo que comentaste en nuestro post de LinkedIn. ¿Te gustaría agendar una demo?" },
        { type: "in", time: "09:18 AM", text: "Hola Vira, sí claro. Me interesa ver cómo se configura el RAG y las respuestas de takeover." },
        { type: "out-sora", time: "09:18 AM", text: "¡Estupendo! Te puedo agendar mañana mismo. ¿Te viene bien a las 10:30 AM?" },
        { type: "in", time: "10:45 AM", text: "Entendido, allí estaré puntual." }
      ]
    },
    "Laura Ríos": {
      name: "Laura Ríos",
      initials: "LR", color: "#D9A441", role: "Diseñadora Gráfica", score: "88%",
      scoreColor: "var(--color-mustard-deep)", time: "10:42 AM", lastMsg: "Sí, tengo una duda de precios.",
      status: "manual",
      tags: ["Diseño UX", "Insta Creator"],
      warnTags: ["Ubicación remota"],
      analysis: "Creadora activa en Instagram. Duda de precios sobre hilos automatizados. Requiere atención personal.",
      email: "l.rios22@email.com", phone: "+57 320 987 6543",
      timerSeconds: 180,
      timerActive: true,
      messages: [
        { type: "sys", time: "10:30 AM", text: "Control manual activado por administrador" },
        { type: "out-human", time: "10:30 AM", text: "¡Hola Laura! Soy Gustavo de VIRA. Vi tu comentario en Instagram sobre los precios. ¿Tienes alguna duda específica?" },
        { type: "in", time: "10:42 AM", text: "Sí, tengo una duda de precios. ¿Hay plan para creadores independientes?" }
      ]
    },
    "Javier Pinto": {
      name: "Javier Pinto",
      initials: "JP", color: "#5C8473", role: "Consultor de Marketing", score: "91%",
      scoreColor: "var(--color-forest)", time: "Ayer", lastMsg: "Perfecto, gracias.",
      status: "wait",
      tags: ["B2B Expert", "LinkedIn"],
      warnTags: [],
      analysis: "Consultor corporativo. Desea validar si el RAG soporta PDFs pesados. En espera de revisión técnica.",
      email: "jpinto.driver@email.com", phone: "+57 311 555 4433",
      timerSeconds: 300,
      timerActive: false,
      messages: [
        { type: "sys", time: "Ayer", text: "Evaluación de requerimientos iniciada" },
        { type: "out-sora", time: "Ayer", text: "Hola Javier, para ver los alcances de PDFs pesados en el RAG, ¿podrías indicarme qué peso promedio tienen tus manuales?" },
        { type: "in", time: "Ayer", text: "Generalmente entre 15MB y 50MB." },
        { type: "sys", time: "Ayer", text: "Consulta en revisión por Ingeniería (En espera)" }
      ]
    }
  });

  const [activeName, setActiveName] = useState<string>("Carlos Mendoza");
  const [filter, setFilter] = useState<string>("all");
  const [search, setSearch] = useState<string>(" ");
  const [typeInput, setTypeInput] = useState<string>("");
  const [showProfilePop, setShowProfilePop] = useState<boolean>(false);
  const chatBodyRef = useRef<HTMLDivElement>(null);

  const activeChat = contacts[activeName];

  // Scroll chat history to bottom
  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [activeName, activeChat?.messages]);

  // Global Timer Effect
  useEffect(() => {
    const interval = setInterval(() => {
      setContacts((prev) => {
        const updated = { ...prev };
        let changed = false;

        Object.keys(updated).forEach((name) => {
          const contact = updated[name];
          if (contact.status === "manual" && contact.timerActive && contact.timerSeconds !== undefined) {
            if (contact.timerSeconds > 0) {
              contact.timerSeconds -= 1;
              changed = true;
            } else {
              // Timer expired, return control to Sora AI
              contact.status = "sora";
              contact.timerActive = false;
              contact.timerSeconds = 300;
              contact.messages.push({
                type: "sys",
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                text: "VIRA IA ha retomado el control automáticamente"
              });
              contact.lastMsg = "VIRA IA ha retomado el control automáticamente";
              changed = true;
            }
          }
        });

        return changed ? updated : prev;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleTakeover = () => {
    setContacts((prev) => {
      const updated = { ...prev };
      const contact = updated[activeName];
      
      if (contact.status === "manual") {
        // Leave to AI
        contact.status = "sora";
        contact.timerActive = false;
        contact.timerSeconds = 300;
        contact.messages.push({
          type: "sys",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          text: "VIRA IA ha retomado el control"
        });
        contact.lastMsg = "VIRA IA ha retomado el control";
      } else {
        // Take manual control
        contact.status = "manual";
        contact.timerActive = true;
        contact.timerSeconds = 300; // Reset to 5m
        contact.messages.push({
          type: "sys",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          text: "Control manual activado por administrador"
        });
        contact.lastMsg = "Control manual activado";
      }
      return updated;
    });
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!typeInput.trim()) return;

    const inputMsg = typeInput;
    setTypeInput("");

    // Append human message
    setContacts((prev) => {
      const updated = { ...prev };
      const contact = updated[activeName];
      contact.messages.push({
        type: "out-human",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        text: inputMsg
      });
      contact.lastMsg = inputMsg;
      // Reset timer inactivity
      if (contact.status === "manual") {
        contact.timerSeconds = 300;
      }
      return updated;
    });

    // If chat is manual, we don't trigger AI reply.
    // If we want to simulate AI answering on RAG, let's trigger it.
    // Let's simulate a reply from VIRA RAG if the chat is not manual
    if (activeChat.status !== "manual") {
      setTimeout(async () => {
        const response = await api.chatInteraction(
          inputMsg,
          activeChat.messages.map(m => ({ role: m.type === "in" ? "user" : "assistant", content: m.text })),
          "whatsapp"
        );
        
        setContacts((prev) => {
          const updated = { ...prev };
          const contact = updated[activeName];
          contact.messages.push({
            type: "out-sora",
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            text: response.reply
          });
          contact.lastMsg = response.reply;
          return updated;
        });
      }, 1000);
    }
  };

  const formatTimer = (seconds?: number) => {
    if (seconds === undefined) return "05:00";
    const m = Math.floor(seconds / 60).toString().padStart(2, "0");
    const s = (seconds % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  };

  const filteredContacts = Object.values(contacts).filter((c) => {
    const matchSearch = c.name.toLowerCase().includes(search.toLowerCase()) || c.role.toLowerCase().includes(search.toLowerCase());
    const matchFilter = filter === "all" || c.status === filter;
    return matchSearch && matchFilter;
  });

  return (
    <div className="flex h-[calc(100vh-144px)] bg-white border border-line rounded-2xl overflow-hidden shadow-sm relative animate-screen-in select-none">
      
      {/* LEFT PANEL: Chat List */}
      <div className="w-[320px] border-r border-line flex flex-col bg-bone shrink-0">
        <div className="p-5 bg-white border-b border-line">
          <h2 className="font-display font-semibold text-base text-ink mb-3">Mensajes</h2>
          <div className="flex items-center bg-pearl px-3 py-2 rounded-full gap-2 text-slate text-xs">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>
            <input
              type="text"
              placeholder="Buscar contacto o cargo..."
              className="bg-transparent border-none outline-none w-full text-ink"
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        {/* Filters */}
        <div className="flex gap-2 p-3 overflow-x-auto border-b border-line bg-white shrink-0 scrollbar-none">
          {["all", "sora", "manual", "wait", "blocked"].map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`text-[10px] font-bold px-3 py-1.5 rounded-full border border-line cursor-pointer capitalize transition-all ${
                filter === type ? "bg-ink text-white border-ink" : "bg-white text-slate hover:bg-pearl/50"
              }`}
            >
              {type === "all" ? "Todos" : type === "sora" ? "Vira IA" : type}
            </button>
          ))}
        </div>

        {/* List items */}
        <div className="flex-1 overflow-y-auto divide-y divide-line/70">
          {filteredContacts.map((c) => {
            const isActive = c.name === activeName;
            return (
              <div
                key={c.name}
                onClick={() => setActiveName(c.name)}
                className={`flex gap-3 p-4 border-l-3 border-transparent cursor-pointer transition-colors ${
                  isActive ? "bg-white border-forest!" : "hover:bg-white/50"
                }`}
              >
                <span className="w-10 h-10 rounded-full text-white font-semibold flex items-center justify-center text-sm shrink-0" style={{ backgroundColor: c.color }}>
                  {c.initials}
                </span>
                <div className="flex-1 min-w-0 flex flex-col justify-center">
                  <div className="flex justify-between items-baseline mb-0.5">
                    <span className="text-xs font-bold text-ink truncate">{c.name}</span>
                    <span className="font-mono text-[9px] text-slate-light">{c.time}</span>
                  </div>
                  <p className="text-xs text-slate truncate m-0 flex items-center gap-1.5">
                    {c.status === "sora" && <span className="w-1.5 h-1.5 rounded-full bg-forest" />}
                    {c.status === "manual" && <span className="w-1.5 h-1.5 rounded-full bg-ink" />}
                    {c.status === "wait" && <span className="w-1.5 h-1.5 rounded-full bg-mustard-deep" />}
                    {c.status === "blocked" && <span className="w-1.5 h-1.5 rounded-full bg-red-500" />}
                    <span className="truncate">{c.lastMsg}</span>
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* CENTRAL PANEL: Chat Area */}
      <div className="flex-1 flex flex-col bg-white relative">
        {/* Header */}
        <div className="p-4 px-6 border-b border-line bg-white flex justify-between items-center shrink-0">
          <div className="flex items-center gap-3 cursor-pointer p-1 rounded-lg hover:bg-bone transition-colors" onClick={() => setShowProfilePop(!showProfilePop)}>
            <span className="w-9 h-9 rounded-full text-white font-semibold flex items-center justify-center text-sm" style={{ backgroundColor: activeChat.color }}>
              {activeChat.initials}
            </span>
            <div>
              <h3 className="text-sm font-bold text-ink m-0 leading-tight">{activeChat.name}</h3>
              <p className="text-[10px] text-slate m-0 font-medium">{activeChat.role}</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleTakeover}
              className={`px-4 py-2 text-xs font-bold rounded-lg cursor-pointer transition-all border ${
                activeChat.status === "manual"
                  ? "bg-ink border-ink text-white"
                  : "bg-white border-line text-ink hover:border-forest hover:text-forest"
              }`}
            >
              {activeChat.status === "manual" ? "Dejar a la IA" : "Tomar Control Manual"}
            </button>
          </div>
        </div>

        {/* Chat History */}
        <div ref={chatBodyRef} className="flex-1 overflow-y-auto p-6 space-y-4 bg-pearl/10">
          {activeChat.messages.map((msg, idx) => {
            if (msg.type === "sys") {
              return (
                <div key={idx} className="flex justify-center my-3 animate-fade-up">
                  <span className="bg-pearl/80 text-[10px] font-bold text-slate-light px-3 py-1 rounded-full uppercase tracking-wider">
                    {msg.text}
                  </span>
                </div>
              );
            }
            const isUser = msg.type === "in";
            const isAI = msg.type === "out-sora";
            const isHuman = msg.type === "out-human";
            
            return (
              <div key={idx} className={`flex flex-col max-w-[75%] animate-fade-up ${isUser ? "self-start" : "self-end"}`}>
                <span className={`font-mono text-[9px] text-slate-light mb-1 px-1 ${isUser ? "self-start" : "self-end"}`}>
                  {msg.time}
                </span>
                <div className={`p-3.5 px-4.5 rounded-2xl text-xs leading-relaxed ${
                  isUser 
                    ? "bg-white text-ink border border-line shadow-sm rounded-bl-xs" 
                    : isAI 
                      ? "bg-forest/6 text-ink border border-forest/15 rounded-br-xs before:content-['✨_Vira_IA'] before:block before:text-[9px] before:font-bold before:text-forest before:mb-1 before:uppercase before:tracking-wider" 
                      : "bg-ink text-white rounded-br-xs shadow-sm"
                }`}>
                  {msg.text}
                </div>
              </div>
            );
          })}
        </div>

        {/* Inactivity Floating Timer */}
        {activeChat.status === "manual" && (
          <div className={`absolute bottom-[90px] left-1/2 -translate-x-1/2 bg-ink text-white px-4 py-2 rounded-full text-xs font-semibold flex items-center gap-2 shadow-md z-10 transition-all ${
            (activeChat.timerSeconds || 0) <= 60 ? "animate-pulse border border-red-500/30" : ""
          }`}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="text-mustard-soft"><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></svg>
            <span>Retorno IA: {formatTimer(activeChat.timerSeconds)}</span>
          </div>
        )}

        {/* Chat Footer Input */}
        {activeChat.status === "manual" && (
          <form onSubmit={handleSendMessage} className="p-4 px-6 bg-white border-t border-line flex gap-3 items-center shrink-0 animate-fade-up">
            <div className="flex-1 bg-pearl rounded-full px-4.5 py-2.5 flex items-center border border-transparent focus-within:border-forest/20 focus-within:bg-white focus-within:shadow-[0_0_0_3px_rgba(63,102,87,0.04)] transition-all">
              <input
                type="text"
                value={typeInput}
                onChange={(e) => setTypeInput(e.target.value)}
                placeholder="Escribe tu mensaje manual..."
                className="bg-transparent border-none outline-none w-full text-sm text-ink font-sans"
              />
            </div>
            <button type="submit" className="w-10 h-10 bg-forest text-white rounded-full flex items-center justify-center border-none shadow-sm cursor-pointer hover:bg-forest-soft hover:-translate-y-0.5 hover:shadow-md transition-all active:translate-y-0">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" /></svg>
            </button>
          </form>
        )}
      </div>

      {/* RIGHT PANEL: Copilot & RAG Details */}
      <div className="w-[340px] border-l border-line bg-bone flex flex-col overflow-y-auto shrink-0 select-text">
        <div className="p-5 pb-3">
          <h3 className="font-display font-semibold text-sm text-ink flex items-center gap-2 m-0">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="text-mustard-deep"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>
            Vira Copilot IA
          </h3>
        </div>

        <div className="p-5 pt-2 space-y-5">
          {/* Card Score */}
          <div className="bg-white p-4.5 rounded-xl border border-line shadow-sm relative overflow-hidden before:content-[''] before:absolute before:left-0 before:top-0 before:w-1 before:h-full before:bg-forest">
            <p className="text-[10px] font-bold text-slate tracking-wider uppercase mb-1 flex justify-between">
              <span>Score de Compatibilidad</span>
              <span className="font-mono" style={{ color: activeChat.scoreColor }}>{activeChat.score}</span>
            </p>
            <p className="text-xs text-slate-light leading-relaxed m-0">{activeChat.analysis}</p>
            
            {/* Tags */}
            <div className="flex flex-wrap gap-1.5 mt-3">
              {activeChat.tags.map((t, idx) => (
                <span key={idx} className="text-[9px] font-bold px-2 py-0.5 rounded bg-forest/8 text-forest border border-forest/15">
                  {t}
                </span>
              ))}
              {activeChat.warnTags.map((t, idx) => (
                <span key={idx} className="text-[9px] font-bold px-2 py-0.5 rounded bg-red-500/8 text-red-500 border border-red-500/15">
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Contact details */}
          <div className="bg-white p-4.5 rounded-xl border border-line shadow-sm space-y-3">
            <h4 className="text-[10px] font-bold text-slate tracking-wider uppercase mb-1">Información de Contacto</h4>
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-light">Correo:</span>
              <span className="font-medium font-mono text-ink text-[11px]">{activeChat.email}</span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-light">Teléfono:</span>
              <span className="font-medium font-mono text-ink text-[11px]">{activeChat.phone}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
