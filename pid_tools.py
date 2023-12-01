import requests
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv('NUM_API_KEY')


def get_phone_info(phone_number):
    url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}"
    response = requests.get(url)
    data = response.json()
    return {"phone_number_info": data}
