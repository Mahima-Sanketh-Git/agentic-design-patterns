from google import genai
from datetime import datetime
from google.genai import types
from dotenv import load_dotenv
import requests
import qrcode
from qrcode.image.styledpil import StyledPilImage
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

def get_current_time():
    """Get the current time and return it as a string."""
    try:
        return datetime.now().strftime("%H:%M:%S")
    except Exception as exc:
        return f"Time lookup failed: {exc}"

def get_weather_from_ip():
    """
    Gets the current, high, and low temperature in Fahrenheit for the user's
    location and returns it to the user.
    """
    try:
        location_response = requests.get('https://ipinfo.io/json', timeout=10)
        location_response.raise_for_status()
        lat, lon = location_response.json()['loc'].split(',')

        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m",
            "daily": "temperature_2m_max,temperature_2m_min",
            "temperature_unit": "fahrenheit",
            "timezone": "auto"
        }

        weather_response = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        return (
            f"Current: {weather_data['current']['temperature_2m']}°F, "
            f"High: {weather_data['daily']['temperature_2m_max'][0]}°F, "
            f"Low: {weather_data['daily']['temperature_2m_min'][0]}°F"
        )
    except Exception as exc:
        return f"Weather lookup failed: {exc}"

# Write a text file
def write_txt_file(file_path: str, content: str):
    """
    Write a string into a .txt file (overwrites if exists).
    Args:
        file_path (str): Destination path.
        content (str): Text to write.
    Returns:
        str: Path to the written file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path
    except Exception as exc:
        return f"File write failed: {exc}"

# Create a QR code
def generate_qr_code(data: str, filename: str, image_path: str):
    """Generate a QR code image given data and an image path.

    Args:
        data: Text or URL to encode
        filename: Name for the output PNG file (without extension)
        image_path: Path to the image to be used in the QR code
    """
    try:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)

        if image_path and os.path.isfile(image_path):
            img = qr.make_image(
                image_factory=StyledPilImage,
                embedded_image_path=image_path
            )
        else:
            img = qr.make_image(fill_color="black", back_color="white")

        output_file = f"{filename}.png"
        img.save(output_file)

        return f"QR code saved as {output_file} containing: {data[:50]}..."
    except Exception as exc:
        return f"QR code generation failed: {exc}"


available_functions = {
    "get_current_time": get_current_time,
    "get_weather_from_ip": get_weather_from_ip,
    "write_txt_file": write_txt_file,
    "generate_qr_code":generate_qr_code
}

tool_1 = {
    "name":"get_current_time",
    "description":"Get the current time and return it as a string.",
    "parameters": {}
}

tool_2 = {
    "name":"get_weather_from_ip",
    "description":"Get the current, high, and low temperature in Fahrenheit for the user's location.",
    "parameters": {}
}

tool_3 = {
    "name":"write_txt_file",
    "description":"Write a string into a .txt file (overwrites if exists).",
    "parameters": {
        "type":"OBJECT",
        "properties":{
            "file_path": {"type": "STRING"},
            "content": {"type": "STRING"}
        },
        "required":["file_path","content"]
    }
}

tool_4 = {
    "name":"generate_qr_code",
    "description":"Generate a QR code image given data and an image path.",
    "parameters": {
        "type":"OBJECT",
        "properties":{
            "data": {"type": "STRING"},
            "filename": {"type": "STRING"},
            "image_path": {"type": "STRING"}
        },
        "required":["data","filename"]
    }
}


def run_workflow():
    try:
        chat = client.chats.create(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                tools=[{"function_declarations": [tool_1, tool_2, tool_3, tool_4]}]
            )
        )

        response = chat.send_message("Can you find my location weather, write it to a text file, and generate a QR code for to navigate my website mahimasanketh.dev? txt file names is weather.txt and qr code image path is qr_image.png")
        while True:
            function_responses = []
            has_function_calls = False

            try:
                parts = response.candidates[0].content.parts
            except Exception as exc:
                print(f"Could not read model response: {exc}")
                return

            for part in parts:
                if part.function_call:
                    has_function_calls = True
                    call = part.function_call
                    print("Agent called function:", call.name)
                    if call.name in available_functions:
                        try:
                            result = available_functions[call.name](**call.args)
                        except Exception as exc:
                            result = f"Tool execution failed: {exc}"

                        response_part = types.Part.from_function_response(
                            name=call.name,
                            response={"output": result}
                        )

                        function_responses.append(response_part)

            if not has_function_calls:
                print("\nFinal AI Summary:")
                print(response.text)
                break

            response = chat.send_message(function_responses)
    except Exception as exc:
        print(f"Workflow failed: {exc}")
    
if __name__ == "__main__":
    try:
        run_workflow()
    except Exception as exc:
        print(f"Unexpected error: {exc}")