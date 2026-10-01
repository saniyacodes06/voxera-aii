from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from core.llm_utils import get_llm, safe_invoke


def analyze_transcript(transcript: str) -> dict:
    print("Running Voxera analysis...")

    llm = get_llm(temperature=0.2)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are Voxera, an AI video and meeting assistant.

Analyze the transcript and return EXACTLY these sections:

TITLE:
A short professional title, maximum 8 words.

SUMMARY:
Give a concise bullet-point summary.

ACTION ITEMS:
List tasks, with owner/deadline only when mentioned.
If none: No action items found.

KEY DECISIONS:
List important decisions.
If none: No key decisions found.

OPEN QUESTIONS:
List unresolved questions or follow-ups.
If none: No open questions found.

Rules:
- Use ONLY information from the transcript.
- Do not invent anything.
- Keep the response concise.
""",
        ),
        ("human", "{text}"),
    ])

    chain = prompt | llm | StrOutputParser()

    analysis = safe_invoke(chain, {"text": transcript})

    sections = {
        "TITLE:": "title",
        "SUMMARY:": "summary",
        "ACTION ITEMS:": "action_items",
        "KEY DECISIONS:": "decisions",
        "OPEN QUESTIONS:": "questions",
    }

    result = {
        "title": [],
        "summary": [],
        "action_items": [],
        "decisions": [],
        "questions": [],
    }

    current = None

    for line in analysis.splitlines():
        line = line.strip()

        clean_line = line.replace("*", "").strip()

        if clean_line in sections:
            current = sections[clean_line]
        elif current and line:
            result[current].append(line)

    return {
        "title": "\n".join(result["title"]).strip(),
        "summary": "\n".join(result["summary"]).strip(),
        "action_items": "\n".join(result["action_items"]).strip(),
        "decisions": "\n".join(result["decisions"]).strip(),
        "questions": "\n".join(result["questions"]).strip(),
        "transcript": transcript,
    }