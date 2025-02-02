import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if API key exists
if not GEMINI_API_KEY:
    raise ValueError("Missing API Key! Add GEMINI_API_KEY to your .env file.")

# Configure Google Gemini AI with the API key
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__, template_folder="school_html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    try:
        user_message = request.form["msg"]
        print(f"User message received: {user_message}")  # Debug print

        # Strict AI Prompt for School-related Questions
        system_prompt = """
        You are an AI assistant for Al Kamal American International School in Azra.
        Your job is to provide information ONLY about the school.

        School Details:
        - Location: Azra, Sharjah, UAE
        - Curriculum: American Curriculum
        - Grades: KG to Grade 12
        - Contact: +971-6-565-9870 | info@akaisschool.com
        - Facilities: Library, science labs, sports fields, mosque, medical clinic
        - Admissions: Open for new students. Visit https://www.akaisschool.com for details.
        - Fees: Contact the school for fee structure.

        If someone asks a question **unrelated to the school**, respond with:
        "I can only provide information about Al Kamal American International School in Azra. Please ask about admissions, fees, facilities, or school policies."

        Now, answer this question:
        """

        # Use Google Gemini AI
        model = genai.GenerativeModel("gemini-pro")  # Use Gemini Pro model
        response = model.generate_content(system_prompt + user_message)

        bot_reply = response.text
        print(f"Bot reply: {bot_reply}")  # Debug print

        return bot_reply

    except Exception as e:
        print(f"Error in chatbot: {e}")  # Print errors to CMD
        return "Error processing your request", 500

if __name__ == "__main__":
    app.run(debug=True)
