'use client';

import * as React from 'react';
import { Viewer, Worker } from '@react-pdf-viewer/core';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import { pageNavigationPlugin } from '@react-pdf-viewer/page-navigation';
import { searchPlugin } from '@react-pdf-viewer/search';

import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import '@react-pdf-viewer/search/lib/styles/index.css';

interface PDFViewerProps {
    fileUrl: string;
    targetPage?: number;
    highlightText?: string;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ fileUrl, targetPage, highlightText }) => {
    const defaultLayoutPluginInstance = defaultLayoutPlugin();
    const pageNavigationPluginInstance = pageNavigationPlugin();
    const searchPluginInstance = searchPlugin();

    const { jumpToPage } = pageNavigationPluginInstance;
    const { highlight } = searchPluginInstance;

    // Jump to page when targetPage changes
    React.useEffect(() => {
        if (targetPage !== undefined && targetPage !== null) {
            jumpToPage(targetPage);
        }
    }, [targetPage, jumpToPage]);

    // Highlight text when it changes
    React.useEffect(() => {
        if (highlightText) {
            // highlight({
            //     keyword: highlightText,
            //     matchCase: false,
            // });
            // NOTE: Search highlight requires the search to be triggered.
            // For MVP, we focus on page jump. Interactive highlighting requires more state management.
            // We leave this hook here for future "text-to-highlight" feature.
        }
    }, [highlightText, highlight]);

    return (
        <div className="h-full w-full bg-slate-100 border-l border-slate-200">
            <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js">
                <div style={{ height: '100%' }}>
                    <Viewer
                        fileUrl={fileUrl}
                        plugins={[
                            defaultLayoutPluginInstance,
                            pageNavigationPluginInstance,
                            searchPluginInstance
                        ]}
                        onDocumentLoad={() => {
                            if (targetPage) jumpToPage(targetPage);
                        }}
                    />
                </div>
            </Worker>
        </div>
    );
};

export default PDFViewer;
