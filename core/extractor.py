from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from core.llm_utils import get_llm, safe_invoke


def build_chain(system_prompt: str):
    llm = get_llm(temperature=0.2)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{text}"),
    ])

    return prompt | llm | StrOutputParser()


def extract_action_items(transcript: str) -> str:
    chain = build_chain(
        """You are an expert meeting analyst.

From the meeting transcript, extract all action items.

For each action item provide:
- Task description
- Owner, if mentioned
- Deadline, if mentioned

Format the answer as a numbered list.

If there are no action items, say:
"No action items found."
"""
    )

    return safe_invoke(chain, {"text": transcript})


def extract_key_decisions(transcript: str) -> str:
    chain = build_chain(
        """You are an expert meeting analyst.

From the meeting transcript, extract all important decisions
that were made.

Format the answer as a numbered list.

Only include decisions supported by the transcript.

If there are no decisions, say:
"No key decisions found."
"""
    )

    return safe_invoke(chain, {"text": transcript})


def extract_questions(transcript: str) -> str:
    chain = build_chain(
        """You are an expert meeting analyst.

From the meeting transcript, extract unresolved questions,
open issues, or topics that need follow-up.

Format the answer as a numbered list.

If there are no unresolved questions, say:
"No open questions found."
"""
    )

    return safe_invoke(chain, {"text": transcript})