import requests

url = "https://instagramdimashirokovv1.p.rapidapi.com/user/tirtharaj_sinha"

headers = {
    'x-rapidapi-host': "InstagramdimashirokovV1.p.rapidapi.com",
    'x-rapidapi-key': "get api key"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
