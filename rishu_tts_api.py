# Import necessary modules
from flask import Flask, request, send_file
from gtts import gTTS
import io

# Initialize the Flask application
app = Flask(__name__)

# Define the API endpoint (route)
# The route is set to /RISHU/text_to_audio
@app.route('/RISHU/text_to_audio', methods=['GET'])
def text_to_audio():
    # Get the text parameter from the URL query string
    text = request.args.get('text')
    
    # Check if text parameter is missing
    if not text:
        return "Error: 'text' parameter is missing. Please use: /RISHU/text_to_audio?text=your_message", 400

    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang='hi') # Using 'hi' for Hindi, but it handles English too

        # Use io.BytesIO to store the audio data in memory
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0) # Rewind the stream to the beginning

        # Send the audio file as a response
        return send_file(
            mp3_fp,
            mimetype='audio/mp3',
            as_attachment=False, # Plays directly in browser
            download_name='audio.mp3'
        )
    except Exception as e:
        # Log the error and return a server error message
        print(f"Error generating TTS: {e}")
        return f"Internal Server Error during TTS generation: {e}", 500

# Vercel needs this 'handler' for the serverless function
# This is usually not required for standard Flask but helps Vercel
# You can uncomment this if needed, but the main code should be fine.
# from flask import jsonify
# @app.route('/')
# def home():
#     return jsonify({"message": "TTS API is running! Use /RISHU/text_to_audio?text=..."})
