import requests

# streaming chunk size
CHUNK_SIZE = 1024

XI_API_KEY = "<xi-api-key>"
VOICE_SAMPLE_PATH1 = "<path-to-file>"
VOICE_SAMPLE_PATH2 = "<path-to-file>"
OUTPUT_PATH = "<path-to-file>"

add_voice_url = "https://api.elevenlabs.io/v1/voices/add"

headers = {
  "Accept": "application/json",
  "xi-api-key": 3ce9b46da1e43ef365ee637c30fa0059
}

data = {
    'name': 'Voice name',
    'labels': '{"accent": "American", "gender": "Female"}',
    'description': 'An old American male voice with a slight hoarseness in his throat. Perfect for news.'
}

files = [
    ('files', ('sample1.mp3', open(VOICE_SAMPLE_PATH1, 'rb'), 'audio/mpeg')),
    ('files', ('sample2.mp3', open(VOICE_SAMPLE_PATH2, 'rb'), 'audio/mpeg'))
]

response = requests.post(add_voice_url, headers=headers, data=data, files=files)
voice_id = response.json()["voice_id"]

# get default voice settings
response = requests.get(
    "https://api.elevenlabs.io/v1/voices/settings/default",
    headers={ "Accept": "application/json" }
).json()
stability, similarity_boost = response["stability"], response["similarity_boost"]

tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

headers["Content-Type"] = "application/json"

data = {
  "text": "Some very long text to be read by the voice",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": stability,
    "similarity_boost": similarity_boost
  }
}

response = requests.post(tts_url, json=data, headers=headers, stream=True)

with open(OUTPUT_PATH, 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)

# Retrieve history. It should contain generated sample.
history_url = "https://api.elevenlabs.io/v1/history"

headers = {
  "Accept": "application/json",
  "xi-api-key": 3ce9b46da1e43ef365ee637c30fa0059
}

response = requests.get(history_url, headers=headers)

print(response.text)
