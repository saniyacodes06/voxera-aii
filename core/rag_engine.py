from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from core.llm_utils import get_llm, safe_invoke
from core.vector_store import build_vector_store, load_vector_store, get_retriever


def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


def build_rag_chain(transcript: str):
    vector_store = build_vector_store(transcript)

    retriever = get_retriever(
        vector_store,
        k=4
    )

    llm = get_llm(temperature=0.3)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are Voxera, an AI meeting assistant.

Answer the user's question using ONLY the meeting transcript
context provided below.

If the answer cannot be found in the transcript, say:

"I could not find this information in the meeting transcript."

Be concise, accurate, and helpful.

Meeting transcript context:
{context}
"""
        ),
        ("human", "{question}"),
    ])

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(rag_chain, question: str) -> str:
    print(f"Question: {question}")

    answer = safe_invoke(
        rag_chain,
        question
    )

    print(f"Answer: {answer}")

    return answer