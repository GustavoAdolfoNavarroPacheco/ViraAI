"use client";

import React, { useState } from "react";
import { api } from "@/lib/api";

interface PostCard {
  id: number;
  platform: string;
  topic: string;
  content: string;
  status: "draft" | "review" | "approved" | "scheduled" | "published";
  scheduledFor?: string;
  metrics?: { impressions: number; engagement: string };
}

export default function CampaignsPage() {
  const [posts, setPosts] = useState<PostCard[]>([
    {
      id: 1,
      platform: "LinkedIn",
      topic: "Lanzamiento oficial de VIRA",
      content: "Nos complace anunciar el lanzamiento de VIRA, una plataforma impulsada por IA para automatizar tus redes sociales.",
      status: "published",
      metrics: { impressions: 1250, engagement: "5.8%" }
    },
    {
      id: 2,
      platform: "Twitter/X",
      topic: "Hilo sobre RAG en memoria",
      content: "Configurar un RAG en memoria en Qdrant es sumamente sencillo. Abro hilo para mostrar el paso a paso. 🧵",
      status: "scheduled",
      scheduledFor: "Hoy, 04:00 PM"
    },
    {
      id: 3,
      platform: "Instagram",
      topic: "Post de consejos de UI con Glassmorphism",
      content: "Claves de UI para aplicar glassmorphism moderno en tus interfaces web. 💎✨",
      status: "review"
    }
  ]);

  // Modal States
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [brandVoice, setBrandVoice] = useState("Profesional y Técnico");
  const [platform, setPlatform] = useState("LinkedIn");
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState("");

  const handleGeneratePost = async () => {
    if (!topic) return;
    setLoading(true);
    try {
      const response = await api.generatePost(brandVoice, topic, platform);
      setGeneratedContent(response.post_content);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = () => {
    if (!generatedContent) return;
    const newPost: PostCard = {
      id: Date.now(),
      platform,
      topic: topic || "Post de IA",
      content: generatedContent,
      status: "draft"
    };
    setPosts([...posts, newPost]);
    setIsModalOpen(false);
    // Reset fields
    setTopic("");
    setGeneratedContent("");
  };

  const movePost = (id: number, targetStatus: PostCard["status"]) => {
    setPosts(posts.map(p => p.id === id ? { ...p, status: targetStatus } : p));
  };

  const columns: { id: PostCard["status"]; label: string; bg: string }[] = [
    { id: "draft", label: "Borrador", bg: "bg-pearl/50" },
    { id: "review", label: "En Revisión", bg: "bg-mustard/5" },
    { id: "approved", label: "Aprobado", bg: "bg-forest/5" },
    { id: "scheduled", label: "Programado", bg: "bg-ink/5" },
    { id: "published", label: "Publicado", bg: "bg-emerald-500/5" }
  ];

  return (
    <div className="space-y-6 animate-fade-up select-none">
      {/* Header Bar */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="font-display font-semibold text-lg text-ink m-0">Tablero Kanban Editorial</h2>
          <p className="text-xs text-slate mt-1">Gestión del ciclo de vida del contenido generado</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-ink hover:bg-ink-soft text-bone px-4 py-2 rounded-lg text-xs font-bold shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md cursor-pointer flex items-center gap-1.5"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="w-3.5 h-3.5"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>
          Generar con IA
        </button>
      </div>

      {/* Columns Grid */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-start">
        {columns.map(col => {
          const colPosts = posts.filter(p => p.status === col.id);
          return (
            <div key={col.id} className={`p-4 rounded-xl border border-line flex flex-col gap-3 min-h-[480px] ${col.bg}`}>
              <div className="flex justify-between items-center border-b border-line pb-2 mb-1">
                <span className="text-xs font-bold text-ink">{col.label}</span>
                <span className="font-mono text-[9px] font-bold bg-pearl/80 text-slate-light px-2 py-0.5 rounded-full">{colPosts.length}</span>
              </div>

              {colPosts.map(post => (
                <div key={post.id} className="bg-white p-3 rounded-lg border border-line shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between gap-3 text-left">
                  <div className="space-y-1">
                    <p className="text-[9px] font-bold text-slate-light uppercase tracking-wider">{post.platform}</p>
                    <h4 className="text-xs font-bold text-ink leading-tight line-clamp-2">{post.topic}</h4>
                    <p className="text-[11px] text-slate line-clamp-3 leading-relaxed m-0">{post.content}</p>
                  </div>

                  {post.metrics && (
                    <div className="bg-pearl/30 p-2 rounded text-[9px] font-semibold text-slate flex justify-between">
                      <span>Impr: {post.metrics.impressions}</span>
                      <span>Eng: {post.metrics.engagement}</span>
                    </div>
                  )}

                  {post.scheduledFor && (
                    <p className="text-[9px] font-mono text-forest font-semibold m-0 flex items-center gap-1">
                      <span className="w-1 h-1 rounded-full bg-forest animate-pulse" />
                      {post.scheduledFor}
                    </p>
                  )}

                  {/* Actions to move */}
                  <div className="flex justify-between gap-1 mt-1 border-t border-line/50 pt-2 shrink-0 select-none">
                    {col.id !== "draft" && (
                      <button
                        onClick={() => {
                          const prevs: Record<string, PostCard["status"]> = { review: "draft", approved: "review", scheduled: "approved", published: "scheduled" };
                          movePost(post.id, prevs[col.id]);
                        }}
                        className="text-[9px] font-bold text-slate hover:text-ink cursor-pointer bg-transparent border-none p-0"
                      >
                        ◀ Atrás
                      </button>
                    )}
                    <div className="flex-1" />
                    {col.id !== "published" && (
                      <button
                        onClick={() => {
                          const nexts: Record<string, PostCard["status"]> = { draft: "review", review: "approved", approved: "scheduled", scheduled: "published" };
                          movePost(post.id, nexts[col.id]);
                        }}
                        className="text-[9px] font-bold text-forest hover:text-forest-soft cursor-pointer bg-transparent border-none p-0"
                      >
                        Avanzar ▶
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          );
        })}
      </div>

      {/* GENERATOR MODAL */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-ink-deep/50 backdrop-blur-xs flex items-center justify-center z-150 animate-fade-up">
          <div className="bg-white rounded-2xl border border-line shadow-lg max-w-xl w-full p-8 space-y-6 select-text">
            <div className="flex justify-between items-center border-b border-line pb-3">
              <h3 className="font-display font-semibold text-base text-ink m-0">Generar Publicación con VIRA IA</h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate hover:text-ink cursor-pointer bg-transparent border-none"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-bold text-slate">Voz de la Marca</label>
                <select
                  value={brandVoice}
                  onChange={(e) => setBrandVoice(e.target.value)}
                  className="w-full p-2.5 border border-line rounded-lg text-xs bg-white text-ink outline-none"
                >
                  <option value="Profesional y Técnico">Profesional y Técnico</option>
                  <option value="Divertido y Dinámico">Divertido y Dinámico</option>
                  <option value="Formativo e Inspirador">Formativo e Inspirador</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate">Plataforma</label>
                <select
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value)}
                  className="w-full p-2.5 border border-line rounded-lg text-xs bg-white text-ink outline-none"
                >
                  <option value="LinkedIn">LinkedIn</option>
                  <option value="Twitter/X">Twitter/X</option>
                  <option value="Instagram">Instagram</option>
                </select>
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-slate">Tema o Instrucción</label>
              <textarea
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Ej. La importancia de la arquitectura hexagonal en proyectos escalables..."
                rows={3}
                className="w-full p-3 border border-line rounded-lg text-xs text-ink outline-none"
              />
            </div>

            <button
              onClick={handleGeneratePost}
              disabled={loading || !topic}
              className="w-full py-3 bg-ink hover:bg-ink-soft disabled:opacity-50 text-bone text-xs font-bold rounded-lg cursor-pointer flex items-center justify-center gap-2 transition-all shadow-sm"
            >
              <span>{loading ? "Redactando borrador..." : "Redactar Borrador con Gemini"}</span>
              {loading && <span className="w-3.5 h-3.5 border-2 border-bone/35 border-t-bone rounded-full animate-spin-fast" />}
            </button>

            {generatedContent && (
              <div className="space-y-2 animate-fade-up">
                <label className="text-xs font-bold text-slate">Borrador Generado (Auto-corregido por IA)</label>
                <textarea
                  value={generatedContent}
                  onChange={(e) => setGeneratedContent(e.target.value)}
                  rows={6}
                  className="w-full p-3 bg-bone border border-line rounded-lg text-xs text-ink font-sans leading-relaxed outline-none"
                />
                <button
                  onClick={handleCreatePost}
                  className="w-full py-3 bg-forest hover:bg-forest-soft text-bone text-xs font-bold rounded-lg cursor-pointer transition-colors shadow-sm"
                >
                  Agregar al Kanban
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
