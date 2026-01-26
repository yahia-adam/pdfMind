import ReactMarkdown from 'react-markdown';
import * as React from 'react';
import { createPortal } from 'react-dom';
import remarkGfm from 'remark-gfm';

// Tooltip Portal Component
const Tooltip = ({
    children,
    rect
}: {
    children: React.ReactNode;
    rect: DOMRect | null;
}) => {
    if (!rect) return null;

    // We render this into document.body to break out of any overflow:hidden/auto containers
    const style: React.CSSProperties = {
        position: 'fixed',
        top: `${rect.top}px`, // Align bottom of tooltip to top of target
        left: `${rect.left + rect.width / 2}px`,
        transform: 'translate(-50%, -100%) translateY(-8px)', // Center horizontally and move up
        zIndex: 9999, // Ensure it's on top of everything
    };

    return createPortal(
        <div
            style={style}
            className="w-64 bg-slate-800 text-white text-xs rounded-lg p-3 shadow-xl pointer-events-none animate-in fade-in zoom-in-95 duration-200"
        >
            {children}
            {/* Arrow */}
            <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-px border-4 border-transparent border-t-slate-800"></div>
        </div>,
        document.body
    );
};

// Markdown Renderer Component
const MarkdownRenderer = ({ content, onCitationClick, setPdfPage, documents }: {
    content: string;
    onCitationClick: (id: number) => void;
    setPdfPage: (page: number) => void;
    documents?: any[];
}) => {
    // State to track which citation is being hovered and its position
    const [hoveredId, setHoveredId] = React.useState<number | null>(null);
    const [hoveredRect, setHoveredRect] = React.useState<DOMRect | null>(null);

    // Transform [12] into a special link format for the markdown parser
    const processedContent = React.useMemo(() => {
        return content.replace(/\[(\d+)\]/g, ' [**[$1]**](citation:$1)');
    }, [content]);

    // Find the document content for the currently hovered ID
    const hoveredDoc = React.useMemo(() => {
        if (!hoveredId || !documents) return null;
        // Loose equality check (==) to handle string vs number ID mismatches
        return documents.find((d: any) => d.metadata.id == hoveredId);
    }, [hoveredId, documents]);

    return (
        <div className="prose prose-sm prose-slate max-w-none break-words [&>p]:mb-2 [&>ul]:mb-2 [&>ol]:mb-2">
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                    a: ({ href, children, ...props }) => {
                        if (href?.startsWith('citation:')) {
                            const id = parseInt(href.split(':')[1]);

                            // Find doc just for the click handler validation
                            // Use loose equality here too for consistency
                            const doc = documents?.find((d: any) => d.metadata.id == id);

                            return (
                                <span className="inline-block align-middle">
                                    <button
                                        onClick={(e) => {
                                            e.preventDefault();
                                            if (doc) {
                                                console.log(`Navigating to citation ${id}, page ${doc.metadata.page}`);
                                                onCitationClick(id);
                                                setPdfPage(doc.metadata.page);
                                            } else {
                                                console.warn(`Document not found for citation ${id}`);
                                            }
                                        }}
                                        onMouseEnter={(e) => {
                                            setHoveredId(id);
                                            setHoveredRect(e.currentTarget.getBoundingClientRect());
                                        }}
                                        onMouseLeave={() => {
                                            setHoveredId(null);
                                            setHoveredRect(null);
                                        }}
                                        className="inline-flex items-center justify-center px-1.5 py-0.5 ml-1 text-xs font-bold text-blue-600 bg-blue-100 rounded cursor-pointer hover:bg-blue-200 no-underline transform -translate-y-px transition-colors z-10 relative"
                                    >
                                        {id}
                                    </button>
                                </span>
                            );
                        }
                        return (
                            <a
                                href={href}
                                {...props}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:underline"
                            >
                                {children}
                            </a>
                        );
                    },
                    p: ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>,
                    ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-1">{children}</ul>,
                    ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-1">{children}</ol>,
                    li: ({ children }) => <li className="pl-1">{children}</li>,
                    h1: ({ children }) => <h1 className="text-xl font-bold mb-3 mt-4 text-slate-800">{children}</h1>,
                    h2: ({ children }) => <h2 className="text-lg font-bold mb-2 mt-3 text-slate-800 border-b pb-1">{children}</h2>,
                    h3: ({ children }) => <h3 className="text-md font-bold mb-2 mt-3 text-slate-800">{children}</h3>,
                    strong: ({ children }) => <strong className="font-bold text-slate-900">{children}</strong>,
                    blockquote: ({ children }) => <blockquote className="border-l-4 border-slate-300 pl-4 italic my-2 text-slate-600">{children}</blockquote>,
                    code: ({ children }) => <code className="bg-slate-100 px-1 py-0.5 rounded text-xs font-mono text-slate-800">{children}</code>,
                }}
            >
                {processedContent}
            </ReactMarkdown>

            {/* Portal Tooltip */}
            {hoveredDoc && (
                <Tooltip rect={hoveredRect}>
                    <div className="font-bold mb-1 border-b border-slate-600 pb-1 text-slate-300">
                        Page {hoveredDoc.metadata.page}
                    </div>
                    <div className="line-clamp-4 leading-relaxed text-slate-200">
                        {hoveredDoc.page_content}
                    </div>
                </Tooltip>
            )}
        </div>
    );
};

export default MarkdownRenderer;
