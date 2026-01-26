import * as React from 'react';
import MarkdownRenderer from '@/components/MarkdownRenderer';

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

export default Typewriter;
