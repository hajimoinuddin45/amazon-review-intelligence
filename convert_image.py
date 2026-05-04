import base64

with open("assets/amazon_bg.png", "rb") as img:
    encoded = base64.b64encode(img.read()).decode()

print(encoded)