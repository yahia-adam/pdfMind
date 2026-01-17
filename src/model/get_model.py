from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 6. Setup LLM
def get_model(model_name):
    llm = ChatOllama(model=model_name)
    return llm

# 7. Setup Prompt
def get_prompt():
    template = """Reponds a cette question en utilisant que le contexte suivant:
    {context}
    
    Question: {question}
    Réponse: """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt


# 8. Create Chain
def create_rag_chain(llm, prompt, retriever):
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

def process_query(rag_chain, query):
    return rag_chain.invoke({"question": query})