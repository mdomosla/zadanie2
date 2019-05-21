import requests

url = "http://18.195.251.80:9000/signup"

payload = "{\n\t\"username\":\"testerasw\",\n\t\"password\":\"1234aaa\",\n\t\"firstname\":\"mdmdmd\",\n\t\"lastname\":\"mdmdmdm\"\n}"
headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "387481ac-0763-dacb-bbc2-e613fc7eb847"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)