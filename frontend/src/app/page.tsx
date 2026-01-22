'use client';

import React, { useState, useRef } from 'react';
import ChatPanel from '@/components/ChatPanel';
import PDFViewer from '@/components/PDFViewer';
import { Settings, PanelLeftClose, PanelLeftOpen } from 'lucide-react';

export default function Home() {
  const [targetPage, setTargetPage] = useState<number>(0);
  const [isPdfVisible, setIsPdfVisible] = useState(true);

  const pdfPanelRef = useRef<any>(null);
  const pdfUrl = '/Nomenclature-Qualibat.pdf';

  const togglePdfPanel = () => {
    const panel = pdfPanelRef.current;
    if (panel) {
      if (panel.isCollapsed()) {
        panel.expand();
        setIsPdfVisible(true);
      } else {
        panel.collapse();
        setIsPdfVisible(false);
      }
    }
  };

  return (
    <main className="flex h-screen w-full flex-col overflow-hidden bg-slate-50">
      {/* Header */}
      <header className="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-6 shrink-0 z-10 shadow-sm relative">
        <div className="flex items-center gap-3">
          <button
            onClick={togglePdfPanel}
            className="p-1.5 rounded-md hover:bg-slate-100 text-slate-500 transition-colors"
            aria-label={isPdfVisible ? "Hide PDF panel" : "Show PDF panel"}
          >
            {isPdfVisible ? <PanelLeftClose size={20} /> : <PanelLeftOpen size={20} />}
          </button>

          <div className="bg-[#0055A4] text-white font-bold p-1 rounded text-xs">QB</div>
          <h1 className="font-bold text-slate-800 text-lg tracking-tight">
            QualiBot <span className="font-medium text-slate-400 text-sm ml-2">Assistant Nomenclature</span>
          </h1>
        </div>
        <button className="text-slate-400 hover:text-slate-600" aria-label="Settings">
          <Settings size={20} />
        </button>
      </header>

      {/* Main Content */}
      <div className="flex-1 w-full overflow-hidden relative">
        {/* Using a simple flex layout instead of PanelGroup until we resolve imports */}
        <div className="flex h-full">
          {/* PDF Panel */}
          {isPdfVisible && (
            <>
              <div
                className="bg-slate-100 h-full"
                style={{ width: '35%', minWidth: '300px' }}
              >
                <PDFViewer fileUrl={pdfUrl} targetPage={targetPage} />
              </div>

              {/* Resize Handle */}
              <div className="w-1.5 bg-slate-200 hover:bg-blue-400 transition-colors cursor-col-resize" />
            </>
          )}

          {/* Chat Panel */}
          <div className="flex-1 bg-white h-full" style={{ minWidth: '400px' }}>
            <ChatPanel
              onCitationClick={() => {
                setIsPdfVisible(true);
              }}
              setPdfPage={(page) => setTargetPage(page - 1)}
              documentsMap={{}}
            />
          </div>
        </div>
      </div>
    </main>
  );
}