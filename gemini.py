from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the client properly
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Generate content using the Gemini model
response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain about generative AI in few words."
)

# Print the text response
print("response:", response.text)


client.close()
