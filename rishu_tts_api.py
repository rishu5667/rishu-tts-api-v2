# Import zaroori modules
from flask import Flask, request, send_file
from gtts import gTTS
import io

# Flask application shuru karein
app = Flask(__name__)

# API endpoint (route) define karein
# Yahin se aapka API access hoga: /RISHU/text_to_audio
@app.route('/RISHU/text_to_audio', methods=['GET'])
def text_to_audio():
    # URL query string se 'text' parameter lein
    text = request.args.get('text')
    
    # Agar 'text' parameter nahi hai, toh error message dein
    if not text:
        return "Error: 'text' parameter missing. Use: /RISHU/text_to_audio?text=your_message", 400

    try:
        # gTTS object banayein. 'hi' (Hindi) bhasha set karein, jo English bhi handle karti hai.
        tts = gTTS(text=text, lang='hi') 

        # Audio data ko memory mein store karne ke liye io.BytesIO ka upyog karein
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0) # Stream ko shuruwat tak le jaayein

        # Audio file ko browser mein bhej dein
        return send_file(
            mp3_fp,
            mimetype='audio/mp3',
            as_attachment=False, # Seedhe browser mein play hoga
            download_name='audio.mp3'
        )
    except Exception as e:
        # Agar koi galti ho toh log karein aur server error message dein
        print(f"Error generating TTS: {e}")
        # Aapki Vercel galti ko theek karne ke liye, yahan ek generic error denge
        return "Internal Server Error. Please check logs for details.", 500

# Final check: Force redeploy to clear Vercel cache
