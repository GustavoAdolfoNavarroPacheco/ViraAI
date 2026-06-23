import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VIRA · Agente de IA para Redes Sociales",
  description: "Plataforma automatizada impulsada por agentes de IA para la generación, programación e interacción de contenido en redes sociales.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="h-full">
      <body className="min-h-full flex flex-col bg-bone text-ink">
        {children}
      </body>
    </html>
  );
}
