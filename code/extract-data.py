import os
from openai import OpenAI

import requests
import json
from dotenv import load_dotenv


def call_gpt5(system_prompt: str, user_prompt: str, image_path: str = None) -> str:
    """
    Call GPT-5 with optional image input using the official OpenAI client.
    """
    input_payload = [
        {"role": "system", "content": [
            {"type": "input_text", "text": system_prompt}]},
        {"role": "user", "content": [
            {"type": "input_text", "text": user_prompt}]}
    ]

    # If an image is included, append it
    if image_path:
        with open(image_path, "rb") as f:
            img_obj = client.files.create(file=f, purpose="vision")

        input_payload[1]["content"].append(
            {"type": "input_image", "file_id": img_obj.id}
        )

    response = client.responses.create(
        model="gpt-5-mini",
        input=input_payload,
        reasoning={"effort": "medium"}
    )

    return response.output_text


def extract_gpt5_text(result: dict) -> str:
    """
    Parse GPT-5 API result to extract the first assistant text output.
    """
    try:
        if not result or "output" not in result:
            return "Invalid response format."

        message_blocks = [b for b in result["output"] if b.get(
            "type") == "message" and b.get("content")]
        if not message_blocks:
            return "No message block found in response."

        text_blocks = [c for c in message_blocks[0]
                       ["content"] if c.get("type") == "output_text"]
        if not text_blocks:
            return "No output_text found in response."

        return text_blocks[0]["text"].strip()
    except Exception as e:
        return f"Error parsing response: {e}"


if __name__ == "__main__":

    # Load environment variables
    load_dotenv(override=True)
    GPT_API_KEY = os.getenv("GPT_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open("prompts/data-extraction.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    user_prompt = "Extract the data and information from this image."

    img_path = "images/test image.png"

    response = call_gpt5(system_prompt, user_prompt, img_path)
    print(response)

