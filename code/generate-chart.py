import os
from openai import OpenAI
import subprocess
import time
import json
from dotenv import load_dotenv
import re

MAX_RETRIES = 3

with open("prompts/design-description.txt", "r", encoding="utf-8") as f:
    DESIGN_PROMPT = f.read()

with open("prompts/generate-chart.txt", "r", encoding="utf-8") as f:
    CHART_PROMPT = f.read()

with open("prompts/recode.txt", "r", encoding="utf-8") as f:
    RECODE_PROMPT = f.read()

with open("prompts/loadings.json", "r") as f:
    LOADINGS = json.load(f)


chart_image1 = """

    {
        "topic": “Budget deficit and surplus compared between Spain and the Euro Zone as a whole”,
        "data": [
            {"year": 1999, "spain": -1.4, "euro_zone_average": -1.4},
            {"year": 2000, "spain": -1.0, "euro_zone_average": 0},
            {"year": 2001, "spain": -0.6, "euro_zone_average": -1.8},
            {"year": 2002, "spain": -0.2, "euro_zone_average": -2.5},
            {"year": 2003, "spain": -0.3, "euro_zone_average": -3.1},
            {"year": 2004, "spain": -0.1, "euro_zone_average": -2.9},
            {"year": 2005, "spain": 1.3, "euro_zone_average": -2.4},
            {"year": 2006, "spain": 2.4, "euro_zone_average": -1.3},
            {"year": 2007, "spain": 1.9, "euro_zone_average": -0.7},
            {"year": 2008, "spain": -4.5, "euro_zone_average": -2.1},
            {"year": 2009, "spain": -11.2, "euro_zone_average": -6.3},
            {"year": 2010, "spain": -9.3, "euro_zone_average": -6.2},
            {"year": 2011, "spain": -8.9, "euro_zone_average": -4.1},
            {"year": 2012, "spain": -6.3, "euro_zone_average": NA},
            {"year": 2013, "spain": -4.5, "euro_zone_average": NA},
            {"year": 2014, "spain": -2.8, "euro_zone_average": NA}
        ]
    }

    I mostly want to focus on the differences between Spain and the Euro-Zone Average values. 
    The final 3 years of this dataset are Spain's economic targets for those years, not actual values.
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


def design_plan_factor(chart_data, factor) -> str:

    # filter the json file
    loadings = {
        key: {
            "Category": value.get("Category"),
            "Definition": value.get("Definition"),
            "Loading": value.get(f"Factor {factor}")
        }
        for key, value in LOADINGS.items()
        # if value.get("Category") != "Source"
        if abs(value.get(f"Factor {factor}")) > 0.2
    }

    user_prompt = f"""Make a design plan for this data that fits with the attached variable loadings. 
        It should be a paired bar chart over the x-axis of time and be in at least a 3:4 aspect ratio (taller than it is wide).
        Make the text large enough to see in a presentation.

        LOADINGS:   
        {loadings}

        DATA:
        {chart_data}"""
    response = call_gpt5mini(DESIGN_PROMPT, user_prompt)
    return response


def generate_chart(design_plan, chart_info) -> str:
    user_prompt = f"""Write code for a chart that follows the given design plan. 
                    {design_plan}
                    
                    Here is the chart data.
                    {chart_info}
        """
    response = call_gpt5mini(CHART_PROMPT, user_prompt)
    return response


def clean_code_response(code_response, img_name):

    clean_code = re.sub(r"^```(?:python)?\n|```$", "",
                        code_response, flags=re.MULTILINE).strip()

    # matplotlib case
    if "plt.show()" in clean_code:
        clean_code = clean_code.replace(
            "plt.show()",
            f'plt.savefig("generated/{img_name}/{img_name}_design.png", dpi=300, bbox_inches="tight")'
        )
    # plotly case
    elif "fig.show()" in clean_code:
        clean_code = clean_code.replace(
            "fig.show()",
            f'fig.write_image("generated/{img_name}/{img_name}_design.png")'
        )

    return clean_code


def regenerate_chart_code(code, error):
    user_prompt = f"""The following Python code failed with an error. 
        Fix the error and return updated code that will run successfully.
        It should be a paired bar chart over the x-axis of time and be in at least a 3:4 aspect ratio (taller than it is wide).
        Make the text large enough to see in a presentation.

        ERROR: {error}

        CODE: {code}

        Return the updated code.
        """
    response = call_gpt5mini(RECODE_PROMPT, user_prompt)
    return response


def run_pipeline(image_info, factor, img_name):

    # make directory
    os.makedirs(os.path.join("generated", img_name), exist_ok=True)

    start = time.time()
    print(
        f"\n--- Beginning work on creating image for factor {factor}. {img_name}. ---")

    # Step 1: design plan
    design_plan = design_plan_factor(image_info, factor)
    design_end = time.time()
    print(
        f"Made design plan. Took {round(design_end - start, 1)} seconds to complete.")
    # print(design_plan)
    # save the design plan
    design_plan_fname = f"generated/{img_name}/{img_name}_design_plan.txt"
    with open(design_plan_fname, "w") as f:
        f.write(design_plan)

    # Step 2: generate + run chart with retries
    # write the code for the chart, allowing for retrying if the code does not work
    code_response_raw = None
    last_error = None
    for attempt in range(0, MAX_RETRIES):
        print(f"--- Attempt {attempt} at constructing chart code---")

        # Generate code
        if attempt == 0:
            code_response_raw = generate_chart(design_plan, image_info)
        else:
            print("Calling recoder to fix the error.")
            code_response_raw = regenerate_chart_code(
                code_response_raw, last_error)

        code_response = clean_code_response(code_response_raw, img_name)

        # save the returned code
        code_fname = f"generated/{img_name}/{img_name}_chart_code.py"
        with open(code_fname, "w") as f:
            f.write(code_response)
        # run the returned code
        chart_code = subprocess.run(
            ["python", code_fname],
            capture_output=True,
            text=True
        )

        if chart_code.returncode == 0:
            print("Chart script successful!")
            break

        if chart_code.returncode != 0:
            print("Chart script failed!")
            last_error = chart_code.stderr
            print("stderr:", last_error)
            if attempt >= MAX_RETRIES:
                print("All retries failed. Giving up.")
                with open(f"generated/{img_name}/{img_name}_failed_code.py", "w") as cf:
                    cf.write(code_response)

    code_end = time.time()

    print(
        f"Wrote the code. Took {round(code_end - design_end, 1)} seconds to complete. Pipeline took {round(code_end -start, 1)} seconds total.")

    return


if __name__ == "__main__":

    # Load environment variables
    load_dotenv(override=True)
    GPT_API_KEY = os.getenv("GPT_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    for i in range(0, 9):
        print("-------------------------")
        print("-------------------------")
        print(f"--------- Run {i} ---------")
        print("-------------------------")
        print("-------------------------")
        run_pipeline(chart_image1, 1, f"spain_factor1_bar{i}")
        run_pipeline(chart_image1, 2, f"spain_factor2_bar{i}")
        run_pipeline(chart_image1, 3, f"spain_factor3_bar{i}")
        run_pipeline(chart_image1, 4, f"spain_factor4_bar{i}")

    # run_pipeline(chart_image2, 4, "cellphone_factor4_2")
