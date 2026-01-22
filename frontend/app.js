const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const messagesContainer = document.getElementById('messages');
const sourcesContainer = document.getElementById('sources-container');
const sendBtn = document.getElementById('send-btn');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = userInput.value.trim();
    if (!query) return;

    // Add user message to UI
    appendMessage(query, 'user');
    userInput.value = '';
    sendBtn.disabled = true;

    // Show typing indicator
    const loadingId = showLoading();

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: query })
        });

        const data = await response.json();

        // Remove loading indicator
        removeLoading(loadingId);

        if (response.ok) {
            // Append bot answer
            const answer = data.response.answer || "Désolé, je n'ai pas pu trouver de réponse.";
            appendMessage(answer, 'bot');

            // Update sources
            updateSources(data.response.documents);
        } else {
            appendMessage("Erreur: Impossible de communiquer avec le serveur.", 'bot');
        }

    } catch (error) {
        console.error('Error:', error);
        removeLoading(loadingId);
        appendMessage("Une erreur est survenue. Veuillez vérifier que le serveur est démarré.", 'bot');
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
});

function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');

    // Convert newlines to breaks for bot messages if needed
    // Simple text node for safety against XSS
    messageDiv.innerText = text;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function showLoading() {
    const id = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.id = id;
    loadingDiv.className = 'typing-indicator';
    loadingDiv.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;
    messagesContainer.appendChild(loadingDiv);
    scrollToBottom();
    return id;
}

function removeLoading(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateSources(documents) {
    sourcesContainer.innerHTML = '';

    if (!documents || documents.length === 0) {
        sourcesContainer.innerHTML = '<p class="placeholder-text">Aucune source utilisée pour cette réponse.</p>';
        return;
    }

    documents.forEach(doc => {
        // doc structure depends on backend, assuming standard RAG output
        // Adjust if doc is just a string or object. 
        // Based on typical LangChain/RAG, it might be Document object or serialized.
        // Let's assume the backend returns a list of objects or strings.
        // If it's the `res["documents"]` from the provided user code, we need to see what `rag_bot` returns.
        // Usually it returns Document objects. 

        // Safety check if doc might be complex
        const content = doc.page_content || doc.content || JSON.stringify(doc);
        const metadata = doc.metadata || {};
        const sourceName = metadata.source || "Document";

        const sourceItem = document.createElement('div');
        sourceItem.className = 'source-item';

        const title = document.createElement('span');
        title.className = 'source-title';
        title.innerText = sourceName.split('/').pop(); // Show filename

        const text = document.createElement('div');
        text.className = 'source-content';
        text.innerText = content;

        sourceItem.appendChild(title);
        sourceItem.appendChild(text);
        sourcesContainer.appendChild(sourceItem);
    });
}
