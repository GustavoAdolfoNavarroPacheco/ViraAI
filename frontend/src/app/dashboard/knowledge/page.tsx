"use client";

import React, { useState } from "react";
import { api } from "@/lib/api";

interface DocItem {
  id: number;
  filename: string;
  chunks: number;
  summary: string;
  date: string;
}

export default function KnowledgePage() {
  const [documents, setDocuments] = useState<DocItem[]>([
    {
      id: 101,
      filename: "VIRA_Guia_de_Marca.pdf",
      chunks: 8,
      summary: "Manual de identidad visual y lineamientos de comunicación del ecosistema VIRA. Especifica el uso de tipografías y el tono profesional en canales corporativos.",
      date: "2026-06-20"
    },
    {
      id: 102,
      filename: "VIRA_Manual_Tecnico_FastAPI.pdf",
      chunks: 14,
      summary: "Documentación sobre la arquitectura hexagonal y la conexión de adaptadores en el backend. Útil para que el agente responda consultas de soporte técnico.",
      date: "2026-06-22"
    }
  ]);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [toastMsg, setToastMsg] = useState("");

  const triggerToast = (msg: string) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(""), 3000);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      if (file.type !== "application/pdf") {
        triggerToast("Solo se permiten archivos en formato PDF.");
        setSelectedFile(null);
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setLoading(true);
    try {
      const response = await api.uploadDocument(selectedFile);
      
      const newDoc: DocItem = {
        id: response.document_id,
        filename: response.filename,
        chunks: response.chunks_indexed,
        summary: response.summary,
        date: new Date().toISOString().split("T")[0]
      };
      
      setDocuments([newDoc, ...documents]);
      setSelectedFile(null);
      triggerToast("Documento subido e indexado con éxito.");
    } catch (err) {
      console.error(err);
      triggerToast("Ocurrió un error al subir el documento.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (id: number) => {
    setDocuments(documents.filter(d => d.id !== id));
    triggerToast("Documento eliminado de la base vectorial.");
  };

  return (
    <div className="space-y-8 animate-fade-up select-none">
      
      {/* Upper Grid: Upload Box & Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_1.4fr] gap-6 items-stretch">
        
        {/* Upload Form Box */}
        <div className="bg-white p-8 rounded-2xl border border-line shadow-sm flex flex-col justify-between">
          <div className="space-y-2">
            <h3 className="font-display font-semibold text-base text-ink m-0">Alimentar Base Vectorial (RAG)</h3>
            <p className="text-xs text-slate">Sube manuales o especificaciones en formato PDF para entrenar al agente de IA.</p>
          </div>

          <form onSubmit={handleUpload} className="space-y-5 my-6">
            <div className="border-2 border-dashed border-line rounded-xl p-6 text-center hover:border-forest/40 transition-colors relative flex flex-col items-center justify-center cursor-pointer min-h-[140px]">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="absolute inset-0 opacity-0 cursor-pointer"
              />
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-8 h-8 text-slate mb-2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12" />
              </svg>
              <p className="text-xs font-semibold text-ink m-0">
                {selectedFile ? selectedFile.name : "Seleccionar archivo PDF"}
              </p>
              <p className="text-[10px] text-slate-light mt-1">Máximo 15MB por archivo</p>
            </div>

            <button
              type="submit"
              disabled={loading || !selectedFile}
              className="w-full py-3.5 bg-ink hover:bg-ink-soft disabled:opacity-55 text-bone font-bold text-xs rounded-lg cursor-pointer flex items-center justify-center gap-2 transition-all shadow-sm"
            >
              <span>{loading ? "Procesando PDF..." : "Indexar Documento"}</span>
              {loading && <span className="w-3.5 h-3.5 border-2 border-bone/35 border-t-bone rounded-full animate-spin-fast" />}
            </button>
          </form>
        </div>

        {/* General Summary Context */}
        <div className="bg-white p-8 rounded-2xl border border-line shadow-sm flex flex-col justify-between">
          <div className="space-y-2 pb-4 border-b border-line">
            <h3 className="font-display font-semibold text-base text-ink m-0">Estado del Procesamiento de IA</h3>
            <p className="text-xs text-slate">Flujo asíncrono para extracción y enriquecimiento semántico</p>
          </div>
          
          <div className="flex-1 flex flex-col justify-center py-6 space-y-4">
            <div className="flex items-start gap-4">
              <span className="w-8 h-8 rounded-lg bg-forest/8 text-forest flex items-center justify-center text-xs shrink-0 font-bold">1</span>
              <div>
                <h4 className="text-xs font-bold text-ink leading-tight mb-1">Layout Parsing (PyPDF)</h4>
                <p className="text-[11px] text-slate leading-relaxed m-0">Extrae el texto organizando los encabezados y bloques lógicos de los documentos cargados.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <span className="w-8 h-8 rounded-lg bg-mustard/12 text-mustard-deep flex items-center justify-center text-xs shrink-0 font-bold">2</span>
              <div>
                <h4 className="text-xs font-bold text-ink leading-tight mb-1">Síntesis Contextual (Gemini 3.5 Flash)</h4>
                <p className="text-[11px] text-slate leading-relaxed m-0">Genera una descripción enriquecida de cada bloque antes de vectorizar, disminuyendo el ruido de términos extraños.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <span className="w-8 h-8 rounded-lg bg-ink/8 text-ink flex items-center justify-center text-xs shrink-0 font-bold">3</span>
              <div>
                <h4 className="text-xs font-bold text-ink leading-tight mb-1">Indexación Vectorial (Qdrant)</h4>
                <p className="text-[11px] text-slate leading-relaxed m-0">Vectoriza a 768 dimensiones (`text-embedding-004`) y almacena indexado por similitud coseno.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Table: Ingested Documents */}
      <div className="bg-white p-8 rounded-2xl border border-line shadow-sm space-y-6">
        <h3 className="font-display font-semibold text-base text-ink m-0">Documentos Activos</h3>
        
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left text-xs text-ink select-text">
            <thead>
              <tr className="border-b border-line bg-bone/50 text-slate font-bold uppercase text-[9px] tracking-wider">
                <th className="p-3 pl-4">Nombre de Archivo</th>
                <th className="p-3">Indexación (Chunks)</th>
                <th className="p-3">Resumen Contextual de IA</th>
                <th className="p-3">Fecha de Carga</th>
                <th className="p-3 pr-4 text-right">Acción</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line/70">
              {documents.map(doc => (
                <tr key={doc.id} className="hover:bg-pearl/10 transition-colors">
                  <td className="p-3.5 pl-4 font-semibold text-ink-soft">{doc.filename}</td>
                  <td className="p-3.5 font-mono text-[10px] font-bold text-forest">{doc.chunks} vectores</td>
                  <td className="p-3.5 text-slate max-w-[280px] truncate leading-relaxed">{doc.summary}</td>
                  <td className="p-3.5 font-mono text-[10px] text-slate">{doc.date}</td>
                  <td className="p-3.5 pr-4 text-right select-none">
                    <button
                      onClick={() => handleDelete(doc.id)}
                      className="text-red-500 hover:text-red-600 font-bold bg-transparent border-none p-1 cursor-pointer transition-colors"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
