
'use client';

import React from 'react';
import MarkdownRenderer from '@/components/MarkdownRenderer';

export default function TestHoverPage() {
    const documents = [
        {
            page_content: "This is the content of document 1.",
            metadata: { id: 1, page: 1, source: "test" }
        },
        {
            page_content: "This is quite a long content for document 2 to see if it wraps or causes issues. It should display in the tooltip.",
            metadata: { id: 2, page: 5, source: "test" }
        }
    ];

    const content = "Here is a reference [1] and another one [2]. Hover over them.";

    return (
        <div className="p-20 bg-gray-100 min-h-screen">
            <h1 className="text-2xl mb-4">Hover Test Page</h1>
            <div className="bg-white p-8 rounded shadow max-w-lg mx-auto overflow-hidden">
                <MarkdownRenderer
                    content={content}
                    onCitationClick={(id) => console.log('clicked', id)}
                    setPdfPage={(page) => console.log('page', page)}
                    documents={documents}
                />
            </div>
            <div className="mt-8">
                <p>Testing outside container clipping.</p>
            </div>
        </div>
    );
}
