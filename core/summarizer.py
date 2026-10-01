from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.llm_utils import get_llm, safe_invoke


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )
    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
    llm = get_llm(temperature=0.3)

    map_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Summarize this portion of a meeting transcript concisely."
        ),
        ("human", "{text}"),
    ])

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = []

    for i, chunk in enumerate(chunks):
        print(
            f"Summarizing transcript chunk "
            f"{i + 1}/{len(chunks)}"
        )

        summary = safe_invoke(
            map_chain,
            {"text": chunk}
        )

        chunk_summaries.append(summary)

    combined = "\n\n".join(chunk_summaries)

    final_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert meeting summarizer.

Combine the partial summaries into one final professional
meeting summary.

Use clear bullet points.
Focus on:
- Main topics
- Important points
- Conclusions
- Important details

Do not add information that is not present."""
        ),
        ("human", "{text}"),
    ])

    final_chain = final_prompt | llm | StrOutputParser()

    return safe_invoke(
        final_chain,
        {"text": combined}
    )


def generate_title(transcript: str) -> str:
    llm = get_llm(temperature=0.3)

    title_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """Based on the meeting transcript, generate a short
professional title.

Maximum 8 words.
Return only the title."""
        ),
        ("human", "{text}"),
    ])

    title_chain = title_prompt | llm | StrOutputParser()

    return safe_invoke(
        title_chain,
        {"text": transcript[:2000]}
    )
    