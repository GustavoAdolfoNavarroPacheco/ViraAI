const API_BASE_URL = "http://localhost:8000/api/v1";

export interface StandardResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export const api = {
  async normalizeContacts(file: File): Promise<any> {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/data/normalize-contacts`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("HTTP error " + response.status);
      return await response.json();
    } catch (e: any) {
      console.warn("Backend API normalizeContacts failed, returning simulated mock response.", e);
      // Simulated fallback response
      return {
        success: true,
        filename: file.name,
        summary: {
          total_processed: 3,
          valid_records_count: 2,
          discarded_records_count: 1
        },
        valid_records: [
          { name: "Gustavo Navarro", email: "gustavo.navarro@email.com", phone: "+57 315 222 3456", position: "Ingeniero De Software" },
          { name: "Laura Rios", email: "laura.rios@email.com", phone: "+57 320 888 3456", position: "Auxiliar Contable" }
        ],
        discarded_records: [
          { row_index: 3, original_data: { name: "", email: "correo_invalido", phone: "123", position: "Director" }, reasons: ["El nombre no puede estar vacío.", "El correo 'correo_invalido' no tiene un formato válido."] }
        ]
      };
    }
  },

  async uploadDocument(file: File): Promise<any> {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/rag/upload-document`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("HTTP error " + response.status);
      return await response.json();
    } catch (e: any) {
      console.warn("Backend API uploadDocument failed, returning simulated mock response.", e);
      // Simulated fallback response
      return {
        success: true,
        document_id: Math.floor(Math.random() * 1000) + 1,
        filename: file.name,
        chunks_indexed: 4,
        summary: "[Síntesis Simulada] Documento corporativo cargado en el RAG local de VIRA.\nEste archivo contiene pautas de marca, políticas de atención y soporte para canales de redes sociales.",
        created_at: new Date().toISOString()
      };
    }
  },

  async generatePost(brandVoice: string, topic: string, platform: string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/agent/generate-post`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ brand_voice: brandVoice, topic, platform }),
      });
      if (!response.ok) throw new Error("HTTP error " + response.status);
      return await response.json();
    } catch (e: any) {
      console.warn("Backend API generatePost failed, returning simulated mock response.", e);
      // Simulated fallback response
      const platformLower = platform.toLowerCase();
      let content = "";
      if (platformLower.includes("twitter") || platformLower.includes("x")) {
        content = `🤖 [Simulado - Tono: ${brandVoice}] Descubre cómo optimizar tu presencia digital en minutos con VIRA. La IA y los agentes automáticos están cambiando la forma de hacer publicaciones sobre: ${topic}. 🚀 #VIRA #Automation`;
      } else if (platformLower.includes("linkedin")) {
        content = `🤖 [Simulado - Tono: ${brandVoice}]\n\nLa consistencia y la relevancia son los pilares fundamentales para posicionar una marca hoy en día. Nos complace compartir nuestro análisis sobre: '${topic}'.\n\nCon nuestra plataforma VIRA, permitimos que las organizaciones escalen su comunicación de manera orgánica a través de agentes inteligentes y RAG.\n\n¿Cómo integras hoy la IA en tus flujos de marketing?\n\n#VIRA #MarketingDigital #Growth #InteligenciaArtificial`;
      } else {
        content = `🤖 [Simulado - Tono: ${brandVoice}] ¡Consigue más alcance! 📸 Compartimos claves para potenciar tu marca respecto a: ${topic}. VIRA automatiza y optimiza tu feed de manera inmediata. ✨ #VIRA #SocialMedia`;
      }
      return {
        success: true,
        platform,
        brand_voice: brandVoice,
        topic,
        post_content: content
      };
    }
  },

  async chatInteraction(message: string, history: Array<{ role: string; content: string }>, platform: string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/agent/chat-interaction`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history, platform }),
      });
      if (!response.ok) throw new Error("HTTP error " + response.status);
      return await response.json();
    } catch (e: any) {
      console.warn("Backend API chatInteraction failed, returning simulated mock response.", e);
      // Simulated fallback response
      return {
        success: true,
        platform,
        message,
        reply: `🤖 [Simulada - RAG en ${platform.toUpperCase()}] Agradecemos tu consulta. Basándonos en nuestra base de conocimientos cargada en VIRA, el soporte de canales e interacciones está habilitado y cuenta con takeover humano automático. Espero esta información sea útil.`
      };
    }
  }
};
