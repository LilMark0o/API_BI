import requests
import json

# The FastAPI server URL (Make sure your FastAPI server is running at this address)
url = "http://127.0.0.1:8000/predict"

# The data you want to send (JSON array with feature data)
data = [
    {
        "objid": 1237648722306924571,
        "ra": 185.5744857,
        "dec": 0.701402405,
        "u": 19.11034,
        "g": 17.62099,
        "r": 17.03464,
        "i": 16.82993,
        "z": 16.71711,
        "run": 756,
        "camcol": 5,
        "field": 466,
        "score": 0.8641446,
        "clean": 1,
        "class_object": "STAR",  # class_object instead of class because 'class' is a reserved word
        "mjd": 54140,
        "rowv": 0.002417854,
        "colv": 0.001363113
    },
    {
        "objid": 1237648722306924572,
        "ra": 185.5744858,
        "dec": 0.701402406,
        "u": 19.11035,
        "g": 17.62100,
        "r": 17.03465,
        "i": 16.82994,
        "z": 16.71712,
        "run": 757,
        "camcol": 6,
        "field": 467,
        "score": 0.8641447,
        "clean": 1,
        "class_object": "GALAXY",
        "mjd": 54141,
        "rowv": 0.002417855,
        "colv": 0.001363114
    }
]
# Send a POST request to the FastAPI server
response = requests.post(url, json=data)

# Check the response from the server
if response.status_code == 200:
    print("Prediction Response:")
    print(response.json())  # Print the response in JSON format
else:
    print(f"Error: {response.status_code}")
    print(response.text)
