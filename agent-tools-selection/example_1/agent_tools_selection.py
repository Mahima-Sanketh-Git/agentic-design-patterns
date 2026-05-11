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
    return datetime.now().strftime("%H:%M:%S")

def get_weather_from_ip():
    """
    Gets the current, high, and low temperature in Fahrenheit for the user's
    location and returns it to the user.
    """
    
    # Get location coordinates from the IP address
    lat,lon = requests.get('https://ipinfo.io/json').json()['loc'].split(',')
    
    # Set parameters for the weather API call
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "timezone": "auto"
    }
    
    # get weather data from the Open-Meteo API
    weather_data  = requests.get("https://api.open-meteo.com/v1/forecast", params=params).json()
    
    # Format and return the simplified string
    return (
        f"Current: {weather_data['current']['temperature_2m']}°F, "
        f"High: {weather_data['daily']['temperature_2m_max'][0]}°F, "
        f"Low: {weather_data['daily']['temperature_2m_min'][0]}°F"
    )

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
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

# Create a QR code
def generate_qr_code(data: str, filename: str, image_path: str):
    """Generate a QR code image given data and an image path.

    Args:
        data: Text or URL to encode
        filename: Name for the output PNG file (without extension)
        image_path: Path to the image to be used in the QR code
    """
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    
    
    # Only use embedded image if valid
    if image_path and os.path.isfile(image_path):

        img = qr.make_image(
            image_factory=StyledPilImage,
            embedded_image_path=image_path
        )

    else:
        # Normal QR code
        img = qr.make_image(fill_color="black", back_color="white")
        
    output_file = f"{filename}.png"
    img.save(output_file)

    return f"QR code saved as {output_file} containing: {data[:50]}..."


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
    chat = client.chats.create(
        model="gemini-3-flash-preview",
        config=types.GenerateContentConfig(
            tools=[{"function_declarations":[tool_1,tool_2,tool_3,tool_4]}]
        )
    )
    


    response = chat.send_message("Can you find my location weather, write it to a text file, and generate a QR code for to navigate my website mahimasanketh.dev? txt file names is weather.txt and qr code image path is qr_image.png")
    while True:
        function_responses = []
        has_function_calls = False
        for part in response.candidates[0].content.parts:
            if part.function_call:
                has_function_calls = True
                call = part.function_call
                print("Agent called function:", call.name)
                if call.name in available_functions:
                    try:
                     result = available_functions[call.name](**call.args)
                    except Exception as e:
                      result = f"Tool execution failed: {str(e)}"
                    
                    # Feed result back
                    response_part =types.Part.from_function_response(
                            name = call.name,
                            response={"output":result}
                        )
                    
                    function_responses.append(response_part)


        # If no more function calls → final text response
        if not has_function_calls:
            print("\nFinal AI Summary:")
            print(response.text)
            break
    
        response = chat.send_message(
            function_responses
        )
    
if __name__ == "__main__":
    run_workflow()