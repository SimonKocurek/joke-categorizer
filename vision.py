

from google.cloud import vision
from google.oauth2 import service_account



GOOGLE_CLOUD_PROJECT = "joke-categorizer"
GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('./auth.json')
client = vision.ImageAnnotatorClient(credentials=GOOGLE_APPLICATION_CREDENTIALS)

def get_words(img):
    content = img.read()
    resp = client.annotate_image(
        {'image': {'content': content}, 'features': [{'type': 'TEXT_DETECTION'}]})
    return

def get_words_url(url):
    image = vision.types.Image()
    image.source.image_uri = url
    resp = client.text_detection(image=image)
    print(resp.full_text_annotation.text)
    return resp.full_text_annotation.text
