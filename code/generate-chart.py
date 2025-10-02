import os
from openai import OpenAI
import subprocess
import time
from dotenv import load_dotenv
import re

MAX_RETRIES = 3


def call_gpt5mini(system_prompt: str, user_prompt: str, image_path: str = None) -> str:
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


def design_plan_factor(system_prompt, chart_data, factor) -> str:
    user_prompt = f"Make a design plan for this data that fits Factor {factor}. {chart_data}"
    response = call_gpt5mini(system_prompt, user_prompt)
    return response


chart_image1 = """

    {
        "topic": “Budget deficit and surplus compared between Spain and the Euro Zone as a whole”,
        "data": [
            {"year": 1999, "spain": -1.2, "euro_zone_average": -0.9},
            {"year": 2000, "spain": -0.6, "euro_zone_average": -0.4},
            {"year": 2001, "spain": -0.4, "euro_zone_average": -0.8},
            {"year": 2002, "spain": -1.0, "euro_zone_average": -1.6},
            {"year": 2003, "spain": -0.8, "euro_zone_average": -2.6},
            {"year": 2004, "spain": 0.6, "euro_zone_average": -2.9},
            {"year": 2005, "spain": 1.3, "euro_zone_average": -1.8},
            {"year": 2006, "spain": 2.4, "euro_zone_average": 1.1},
            {"year": 2007, "spain": 1.9, "euro_zone_average": -0.8},
            {"year": 2008, "spain": -4.5, "euro_zone_average": -3.6},
            {"year": 2009, "spain": -11.2, "euro_zone_average": -6.3},
            {"year": 2010, "spain": -9.5, "euro_zone_average": -6.0},
            {"year": 2011, "spain": -7.8, "euro_zone_average": -4.1},
            {"year": 2012, "spain": -4.2, "euro_zone_average": -4.6},
            {"year": 2013, "spain": -5.0, "euro_zone_average": -3.8},
            {"year": 2014, "spain": -2.5, "euro_zone_average": -2.0}
        ]
    }

    I mostly want to focus on the differences between Spain and the Euro-Zone Average values.
    """


chart_image2 = """

        {
            “topic”: “Cellphone service cost in 2019 in USD”
            "data": [
                { "category": "Russia", "value": 4.0 },
                { "category": "Other", "value": 7.0 },
                { "category": "Other", "value": 7.2 },
                { "category": "Other", "value": 9.0 },
                { "category": "Other", "value": 12.0 },
                { "category": "France", "value": 15.0 },
                { "category": "Other", "value": 18.0 },
                { "category": "Britain", "value": 33.0 },
                { "category": "Other", "value": 34.0 },
                { "category": "Other", "value": 37.0 },
                { "category": "Other", "value": 42.0 },
                { "category": "China", "value": 49.5 },
                { "category": "Other", "value": 60.0 },
                { "category": "U.S.", "value": 63.0 }
                ]
        }

        I mostly want to focus on the comparisons between the named countries. 
        The information about the "Other" countries is less relevant.
    """


def generate_chart(system_prompt, design_plan, chart_info) -> str:
    user_prompt = f"""Provide the code for a chart that follows the given design plan. 
                    {design_plan}
                    
                    Here is the chart data.
                    {chart_info}
                    """
    response = call_gpt5mini(system_prompt, user_prompt)
    return response


def clean_code_response(code_response, img_name):

    clean_code = re.sub(r"^```(?:python)?\n|```$", "",
                        code_response, flags=re.MULTILINE).strip()

    # matplotlib case
    if "plt.show()" in clean_code:
        clean_code = clean_code.replace(
            "plt.show()",
            f'plt.savefig("generated_images/design_{img_name}.png", dpi=300, bbox_inches="tight")\nplt.show()'
        )
    # plotly case
    elif "fig.show()" in clean_code:
        clean_code = clean_code.replace(
            "fig.show()",
            f'fig.write_image("generated_images/design_{img_name}.png")\nfig.show()'
        )

    return clean_code


def run_pipeline(design_prompt, chart_prompt, image_info, factor, img_name):

    start = time.time()
    print("Beginning work on Image.")

    # generate the design plan
    design_plan = design_plan_factor(design_prompt, image_info, factor)
    design_end = time.time()
    print(
        f"Made design plan. Took {round(design_end - start, 1)} seconds to complete.")
    # print(design_plan)

    # write the code for the chart, allowing for retrying if the code does not work
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n--- Attempt {attempt} at constructing chart code---")

        code_response_raw = generate_chart(
            chart_prompt, design_plan, image_info)
        code_response = clean_code_response(code_response_raw, img_name)

        # run the returned code
        code_fname = f"generated_code/chart_code_{img_name}.py"

        with open(code_fname, "w") as f:
            f.write(code_response)
        chart_code = subprocess.run(
            ["python", code_fname],
            capture_output=True,
            text=True
        )
        print("stdout:", chart_code.stdout)
        print("stderr:", chart_code.stderr)
        if chart_code.returncode == 0:
            print("Chart script successful!")
            break

        if chart_code.returncode != 0:
            print("Chart script failed!")

    code_end = time.time()

    print(
        f"Wrote the code. Took {round(code_end - design_end, 1)} seconds to complete. Pipeline took {round(code_end -start, 1)} seconds total.")
    # print(code_response_raw)

    return


if __name__ == "__main__":

    # Load environment variables
    load_dotenv(override=True)
    GPT_API_KEY = os.getenv("GPT_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open("prompts/design-description.txt", "r", encoding="utf-8") as f:
        design_prompt = f.read()

    with open("prompts/generate-chart.txt", "r", encoding="utf-8") as f:
        chart_prompt = f.read()

    run_pipeline(design_prompt, chart_prompt, chart_image1, 2, "1")
    # run_pipeline(design_prompt, chart_prompt, chart_image2, 4, "2")
