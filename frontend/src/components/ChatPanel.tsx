'use client';

import * as React from 'react';
import { Send, Bot, User } from 'lucide-react';
import Image from 'next/image';
import { clsx } from 'clsx';
import { askQuestion } from '@/lib/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    isLoading?: boolean;
}

interface ChatPanelProps {
    onCitationClick: (id: number) => void;
    setPdfPage: (page: number) => void;
    documentsMap: Record<number, { page: number; content: string }>;
}

// Markdown Renderer Component
const MarkdownRenderer = ({ content, onCitationClick, setPdfPage, documents }: {
    content: string;
    onCitationClick: (id: number) => void;
    setPdfPage: (page: number) => void;
    documents?: any[];
}) => {
    // Transform [12] into a special link format for the markdown parser
    // Format: [**[12]**](citation:12) to make it bold and linkable
    const processedContent = React.useMemo(() => {
        return content.replace(/\[(\d+)\]/g, ' [**[$1]**](citation:$1)');
    }, [content]);

    return (
        <div className="prose prose-sm prose-slate max-w-none break-words [&>p]:mb-2 [&>ul]:mb-2 [&>ol]:mb-2">
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                    a: ({ href, children, ...props }) => {
                        if (href?.startsWith('citation:')) {
                            const id = parseInt(href.split(':')[1]);
                            const doc = documents?.find((d: any) => d.metadata.id === id); // Find doc once

                            return (
                                <span className="group relative inline-block align-middle">
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
                                        className="inline-flex items-center justify-center px-1.5 py-0.5 ml-1 text-xs font-bold text-blue-600 bg-blue-100 rounded cursor-pointer hover:bg-blue-200 no-underline transform -translate-y-px transition-colors z-10 relative"
                                    >
                                        {id}
                                    </button>

                                    {/* Tooltip */}
                                    {doc && (
                                        <div className="invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-opacity absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-slate-800 text-white text-xs rounded-lg p-3 shadow-xl z-50 pointer-events-none">
                                            <div className="font-bold mb-1 border-b border-slate-600 pb-1 text-slate-300">
                                                Page {doc.metadata.page}
                                            </div>
                                            <div className="line-clamp-4 leading-relaxed text-slate-200">
                                                {doc.page_content}
                                            </div>
                                            {/* Arrow */}
                                            <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-px border-4 border-transparent border-t-slate-800"></div>
                                        </div>
                                    )}
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
                    // Custom styling for elements if needed
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
        </div>
    );
};

// Typewriter component
const Typewriter = ({ content, onCitationClick, setPdfPage, documents, onComplete }: {
    content: string;
    onCitationClick: (id: number) => void;
    setPdfPage: (page: number) => void;
    documents?: any[];
    onComplete?: () => void;
}) => {
    const [displayedContent, setDisplayedContent] = React.useState("");

    React.useEffect(() => {
        let currentIndex = 0;
        // Faster speed: 5ms per char for snappier feel
        const interval = setInterval(() => {
            if (currentIndex >= content.length) {
                clearInterval(interval);
                onComplete?.();
                return;
            }
            setDisplayedContent(content.slice(0, currentIndex + 1));
            currentIndex++;
        }, 5);

        return () => clearInterval(interval);
    }, [content, onComplete]);

    return (
        <MarkdownRenderer
            content={displayedContent}
            onCitationClick={onCitationClick}
            setPdfPage={setPdfPage}
            documents={documents}
        />
    );
};

export default function ChatPanel({ onCitationClick, setPdfPage, documentsMap }: ChatPanelProps) {
    const [input, setInput] = React.useState('');
    const [messages, setMessages] = React.useState<Message[]>([
        {
            id: 'welcome',
            role: 'assistant',
            content: 'Bonjour ! Je suis votre assistant **Qualibat**. Posez-moi une question sur la nomenclature ou les qualifications.',
        },
    ]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg: Message = { id: Date.now().toString(), role: 'user', content: input };
        setMessages((prev) => [...prev, userMsg]);
        setInput('');

        const aiMsgId = (Date.now() + 1).toString();
        setMessages((prev) => [...prev, { id: aiMsgId, role: 'assistant', content: '', isLoading: true }]);

        try {
            const response = await askQuestion(userMsg.content);

            setMessages((prev) =>
                prev.map((m) =>
                    m.id === aiMsgId
                        ? { ...m, content: response.answer, isLoading: false, documents: response.documents }
                        : m
                )
            );

        } catch (err) {
            setMessages((prev) =>
                prev.map((m) =>
                    m.id === aiMsgId ? { ...m, content: "Désolé, une erreur est survenue.", isLoading: false } : m
                )
            );
        }
    };

    return (
        <div className="flex flex-col h-full bg-white relative">
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.map((msg, index) => {
                    const isLast = index === messages.length - 1;
                    const isAI = msg.role === 'assistant';

                    const showTypewriter = isAI && isLast && !msg.isLoading;

                    return (
                        <div
                            key={msg.id}
                            className={clsx(
                                'flex w-full max-w-3xl mx-auto gap-4',
                                msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                            )}
                        >
                            <div
                                className={clsx(
                                    'w-8 h-8 rounded-full flex items-center justify-center shrink-0',
                                    msg.role === 'user' ? 'bg-slate-200' : 'bg-[var(--color-qualibat-blue)] text-white'
                                )}
                            >
                                {msg.role === 'user' ? <User size={16} /> : (
                                    <div className="relative w-5 h-5">
                                        <Image
                                            src="/logo_qualibat.svg"
                                            alt="Bot"
                                            fill
                                            className="object-contain"
                                        />
                                    </div>
                                )}
                            </div>
                            <div
                                className={clsx(
                                    'p-4 rounded-2xl text-sm leading-relaxed max-w-[85%]',
                                    msg.role === 'user'
                                        ? 'bg-slate-100 text-slate-800 rounded-tr-none'
                                        : 'bg-white border border-slate-100 shadow-sm text-slate-700 rounded-tl-none'
                                )}
                            >
                                {msg.isLoading ? (
                                    <div className="flex gap-1">
                                        <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" />
                                        <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce [animation-delay:0.1s]" />
                                        <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce [animation-delay:0.2s]" />
                                    </div>
                                ) : (
                                    showTypewriter ? (
                                        <Typewriter
                                            content={msg.content}
                                            onCitationClick={onCitationClick}
                                            setPdfPage={setPdfPage}
                                            documents={(msg as any).documents}
                                        />
                                    ) : (
                                        <MarkdownRenderer
                                            content={msg.content}
                                            onCitationClick={onCitationClick}
                                            setPdfPage={setPdfPage}
                                            documents={(msg as any).documents}
                                        />
                                    )
                                )}
                            </div>
                        </div>
                    )
                })}
            </div>

            <div className="p-4 border-t border-slate-100 bg-white/80 backdrop-blur-sm">
                <form onSubmit={handleSubmit} className="max-w-3xl mx-auto relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Posez votre question technique..."
                        className="w-full pl-5 pr-14 py-4 bg-white border border-slate-200 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 shadow-lg shadow-slate-100 transition-all font-medium text-slate-700"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim()}
                        className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-[var(--color-qualibat-blue)] text-white rounded-full hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send size={18} />
                    </button>
                </form>
                <div className="text-center mt-2 text-[10px] text-slate-400 font-medium tracking-wide">
                    ASSISTANT IA RAG • NOMENCLATURE QUALIBAT
                </div>
            </div>
        </div>
    );
}
