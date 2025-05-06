import base64
from colorthief import ColorThief
from openai import OpenAI

OPENAI_API_KEY = "Your api key" 
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_image_with_gpt(image_path, user_prompt):
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI music assistant."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Here is an image and a prompt: {user_prompt}. Based on the mood and color of the image, suggest 3 music genres or moods."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content

def extract_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

def run_music_recommendation(image_path, prompt):
    color = extract_dominant_color(image_path)
    gpt_output = analyze_image_with_gpt(image_path, prompt)
    return gpt_output, color
