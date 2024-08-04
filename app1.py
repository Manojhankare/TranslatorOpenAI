#gemini API_KEY = AIzaSyBFh9DbNNIpIqSd-0u-eakRyVzEUwpZW4Y

import google.generativeai as genai
import os
 
genai.configure(api_key=os.environ["API_KEY"])
 
model = genai.GenerativeModel('gemini-1.5-flash')
 
question = "What is the capital of France?"
 
response = model.generate_content(question)
 
print(response)