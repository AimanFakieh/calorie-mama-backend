# main_api.py

# Import required libraries
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for API key security)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load Calorie Mama API key from environment
CALORIE_MAMA_API_KEY = os.getenv("CALORIE_MAMA_API_KEY")

# Endpoint to receive image from the Android app
@app.route('/analyze', methods=['POST'])
def analyze_image():
    # Ensure a file was included in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Get the uploaded image
    image = request.files['image']

    # Send image to Calorie Mama API using POST request
    response = requests.post(
        f'https://api-2445582032290.production.gw.apicast.io/v1/foodrecognition?user_key={CALORIE_MAMA_API_KEY}',
        files={'media': (image.filename, image.stream, image.mimetype)}
    )

    # If the API request fails
    if response.status_code != 200:
        return jsonify({'error': 'Failed to analyze image'}), 500

    # Return the JSON response from Calorie Mama API
    return jsonify(response.json())

# Run the app on local server
if __name__ == '__main__':
    app.run(debug=True)
