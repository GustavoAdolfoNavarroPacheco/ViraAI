import React from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex flex-row min-h-screen bg-bone">
      {/* Sidebar navigation */}
      <Sidebar />
      
      {/* Main workspace area */}
      <div className="flex flex-col flex-1 min-w-0">
        <Header />
        
        {/* Subview container */}
        <main className="flex-1 p-8 overflow-y-auto bg-pearl/40">
          {children}
        </main>
      </div>
    </div>
  );
}
