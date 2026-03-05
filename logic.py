from config import API_Token
import json
import requests
import time

api_key = "<YOUR TOKEN HERE>"
authorization = "Bearer %s" % api_key

class LeonardoAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.authorization = "Bearer %s" % api_key

        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": authorization
        }
        self.url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    def generate_image(self, prompt, filename="result.jpg"):
        payload = {
            "height": 512,
            "width": 512,
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
            "prompt": prompt,
        }
        response = requests.post(self.url, json=payload, headers=self.headers)
        print(response.status_code)
        generation_id = response.json()['sdGenerationJob']['generationId']
        time.sleep(20)
        result_url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id
        response = requests.get(result_url, headers=self.headers)
        data = response.json()
        image_url = data["generations_by_pk"]["generated_images"][0]["url"]
        image_data = requests.get(image_url).content

        # Сохраняем изображение в файл
        with open(filename, "wb") as file:
            file.write(image_data)
        return image_url
    

api = LeonardoAPI(API_Token)
