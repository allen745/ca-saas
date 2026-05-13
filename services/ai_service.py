from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_document(extracted_text: str) -> str:
    prompt = f"""
    You are an expert CA (Chartered Accountant) assistant in India.

    Below is the text extracted from a client document (ITR or notice).
    Please provide a clear, simple summary of this document in 5-7 bullet points.
    Focus on key financial figures, important dates, and action items.

    Document text:
    {extracted_text[:3000]}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    return response.choices[0].message.content


def draft_notice_reply(extracted_text: str) -> str:
    prompt = f"""
    You are an expert CA (Chartered Accountant) assistant in India.

    Below is the text of an Income Tax Department (ITD) notice received by a client.
    Please draft a professional reply to this notice in formal language.
    The reply should acknowledge the notice, address the concerns raised, and request any necessary extensions if needed.

    Notice text:
    {extracted_text[:3000]}
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )

    return response.choices[0].message.content


def answer_question(extracted_text: str, question: str) -> str:
    prompt = f"""
    You are an expert CA (Chartered Accountant) assistant in India.

    Below is the text extracted from a client document.
    Answer the following question based on this document only.
    Be specific and precise in your answer.

    Document text:
    {extracted_text[:3000]}

    Question: {question}
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    return response.choices[0].message.content