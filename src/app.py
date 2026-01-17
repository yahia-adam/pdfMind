import gradio as gr
from src.rag import initialize_rag_system, process_query

def main():
    print("Initializing RAG system...")
    rag_chain = initialize_rag_system()
    print("RAG system initialized.")

    def chat_function(message, history):
        response = process_query(rag_chain, message)
        return response

    demo = gr.ChatInterface(
        fn=chat_function,
        title="QualiBot - Assistant Expert Qualibat",
        description="Assistant intelligent dédié à la Nomenclature officielle de QUALIBAT. Posez vos questions sur les qualifications, les codes techniques, les mentions RGE et les 9 familles de travaux.",
        examples=[
            "Quelles sont les activités de la Famille 5 ?",
            "C'est quoi la mention RGE ?",
            "Comment décrypter le code à 4 chiffres ?",
            "Quels travaux nécessitent une certification Amiante ?"
        ]
    )

    demo.launch()

if __name__ == "__main__":
    main()
