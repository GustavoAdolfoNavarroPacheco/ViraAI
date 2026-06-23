# 🤖 Sora — Plataforma Inteligente de Reclutamiento

> **Sora** es una plataforma web de gestión de talento humano potenciada por Inteligencia Artificial, diseñada para optimizar cada etapa del proceso de selección: desde la publicación de vacantes hasta la contratación final.

---

## 📌 ¿Qué es Sora?

Sora es un sistema de reclutamiento todo-en-uno que combina la gestión operativa clásica de RRHH con un agente de IA conversacional que interactúa directamente con los candidatos vía WhatsApp. El equipo de selección supervisa, copilota y toma decisiones en tiempo real desde un panel centralizado y moderno.

El sistema fue desarrollado como una aplicación web monolítica (`index.html`) sin dependencias externas, utilizando únicamente **HTML5**, **CSS3 (Vanilla)** y **JavaScript (ES6+)**, garantizando máxima portabilidad y rendimiento.

---

## ✨ Características Principales

### 🏠 Dashboard General
Panel de control central con los KPIs más importantes del proceso de selección:
- **Tasa de respuesta** del agente IA.
- **Embudo de conversión** visual (Aplicantes → Entrevistados → Contratados).
- **Agenda del día**: entrevistas programadas con hora, candidato y vacante.
- Métricas animadas que se actualizan al renderizar la vista.

### 📋 Gestión de Vacantes
Vista doble con alternancia entre **Kanban** y **Listado**:
- **Vista Kanban**: Tarjetas de vacantes organizadas por fase del proceso (Publicada, En proceso, Cierre, Archivada).
- **Vista Lista**: Tabla completa con filtros por nombre, score, días abierta y fase, con scroll horizontal responsive.
- **Modal de nueva vacante**: Selección de perfil de cargo, sede, cupos y SLA de cierre.
- Barra de SLA visual con indicador de alerta por vencimiento.

### 💬 Chat en Vivo (Copilotaje IA)
Bandeja unificada de mensajes de WhatsApp con tres paneles:
- **Panel izquierdo**: Lista de candidatos con búsqueda, filtros por estado (Sora IA, Manual, En Espera, Bloqueado) e indicadores de color.
- **Panel central**: Hilo de conversación con tipos de mensaje diferenciados (Candidato, Sora IA, Agente Humano, Sistema).
- **Panel derecho**: Copilot con score del candidato, análisis IA, etiquetas de perfil y acciones rápidas.

#### 🕹️ Control Manual
El botón **"Tomar Control Manual"** permite al reclutador intervenir en una conversación que maneja Sora:
- Al activarse, habilita la barra de escritura y un **temporizador de inactividad (5 min)** visible.
- El botón cambia a **"Dejar a la IA"** para devolver el control.
- Cada chat mantiene su **estado y temporizador de forma independiente**: cambiar de candidato pausa el contador del anterior y lo restaura al volver.
- Al expirar el tiempo, Sora retoma el control automáticamente con un mensaje de sistema.

### 📅 Calendario
Agenda de entrevistas con tres vistas:
- **Semanal**: Grilla por horas con tarjetas de entrevistas, scroll horizontal en móvil.
- **Mensual**: Calendario de cuadrícula con indicadores de eventos por día.
- **Anual**: Vista compacta de 12 meses con heatmap de actividad.

### 👤 Candidatos
Base de datos inteligente de perfiles con:
- Pipeline oficial de **10 estados** en 4 fases (Atracción → Evaluación → Selección → Cierre).
- Score de compatibilidad por candidato.
- Búsqueda en tiempo real y exportación de datos.

### 📄 Perfiles de Cargo
Catálogo maestro de los perfiles que alimentan al agente IA:
- Descripción del cargo, competencias requeridas y batería de preguntas de filtro.
- El agente usa estos perfiles para evaluar automáticamente a cada candidato.

### 📤 Plantillas de Envío
Catálogo de plantillas de mensajes de WhatsApp sincronizadas con **Meta Business Suite**:
- Plantillas de bienvenida, citación a entrevista, rechazo respetuoso y confirmación de oferta.
- Vista previa en tiempo real del mensaje como se vería en WhatsApp.

### 📚 Base de Conocimiento
Repositorio de documentos oficiales que alimentan al agente con respuestas contextuales:
- Reglamento interno, beneficios, políticas de nómina, etc.
- El agente cita estos documentos cuando responde preguntas específicas de candidatos.

### ⚙️ Configuración
Panel de administración del sistema:
- Gestión de la organización y usuarios con roles.
- Configuración de canales de comunicación (WhatsApp, correo).
- Parámetros del agente IA (personalidad, tiempo de respuesta, escalación).

---

## 🗂️ Estructura del Proyecto

```
Sora/
├── index.html      # Aplicación completa (monolito HTML + CSS + JS)
└── README.md       # Este archivo
```

La aplicación es completamente **autocontenida en un único archivo**. No requiere servidor, framework ni instalación de dependencias.

---

## 🚀 Cómo Usar

1. **Clonar o descargar** el repositorio.
2. Abrir el archivo `index.html` directamente en cualquier navegador moderno (Chrome, Edge, Firefox).
3. Usar las credenciales de demostración en la pantalla de inicio de sesión:
   - **Correo**: cualquier correo válido (ej. `admin@empresa.com`)
   - **Contraseña**: cualquier contraseña (ej. `Admin123!`)
4. Navegar por los módulos desde el menú lateral izquierdo.

> ⚠️ Esta versión es un **prototipo funcional de demostración** (mockup interactivo). Los datos mostrados son ficticios y la integración real con WhatsApp/Meta Business Suite requiere configuración de backend.

---

## 📱 Diseño Responsive

La interfaz está optimizada para dispositivos móviles con un enfoque **Mobile First**:

| Módulo | Comportamiento en móvil |
|---|---|
| **Sidebar** | Oculto por defecto, se abre con botón hamburguesa (☰) |
| **Chat** | Navegación estilo WhatsApp: lista ↔ conversación |
| **Vacantes** | Scroll horizontal en vista de lista |
| **Calendario** | Scroll horizontal en vista semanal, tarjetas apiladas en mensual/anual |

---

## 🎨 Diseño y Tecnología

| Aspecto | Detalle |
|---|---|
| **Tecnología** | HTML5 · CSS3 · JavaScript ES6+ (sin frameworks) |
| **Tipografías** | Inter (UI), DM Serif Display (títulos), JetBrains Mono (datos) |
| **Paleta de color** | Tinta oscura (`#1B3A4D`) + Verde bosque (`#3F6657`) + Crema (`#F5F2EC`) |
| **Animaciones** | Transiciones CSS `cubic-bezier`, keyframes `dashEnter`, `fadeUp`, `vacEnter` |
| **Iconografía** | SVG inline (Feather Icons estilo) |
| **Tema** | Claro con acentos oscuros y toques de glassmorphism |

---

## 🧩 Módulos del Sistema

```
Sora/
├── 🏠 Dashboard          — KPIs, embudo y agenda
├── 📋 Vacantes           — Kanban + Lista + Modal de creación
├── 💬 Chat en vivo       — Bandeja WhatsApp + Copilot IA
├── 📅 Calendario         — Agenda semanal / mensual / anual
├── 👤 Candidatos         — Pipeline de 10 estados
├── 📄 Perfiles de cargo  — Catálogo maestro
├── 📤 Plantillas         — Mensajes WhatsApp
├── 📚 Conocimiento       — Documentos del agente
└── ⚙️ Configuración      — Organización y ajustes del agente
```

---

## 👥 Roles de Usuario

| Rol | Acceso |
|---|---|
| **Administrador** | Acceso total: configuración, usuarios, todos los módulos |
| **Reclutador** | Gestión de vacantes, chat, candidatos y calendario |
| **Analista** | Lectura de reportes, base de conocimiento y plantillas |

---

## 🤝 Créditos

Desarrollado como prototipo funcional de alta fidelidad para demostrar las capacidades de **Sora AI** en la automatización del reclutamiento de personal en empresas del sector agroindustrial y afines.

---

*© 2025 Sora — Desarrollado por Gustavo Navarro. Todos los derechos reservados.*