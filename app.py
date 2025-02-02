# from flask import Flask, request, jsonify
# import cohere
# import pinecone

# # Initialize Cohere and Pinecone
# cohere_api_key = "Me7DHIuwMpPtjLWUN73h8QZKPezZB13JZ0y0WKFb"  # Your Cohere API key
# cohere_client = cohere.Client(cohere_api_key)

# pinecone_api_key = "6ebf67d9-74dd-4aff-9a81-9e182cd22bc3"
# pc = pinecone.Pinecone(api_key=pinecone_api_key, environment="us-east-1-gcp")  # Specify your environment
# index_name = "parenting-chatbot"
# index = pc.Index(index_name)

# # Flask app setup
# app = Flask(__name__)

# # Function to generate embedding for user query using Cohere
# def generate_query_embedding(query):
#     response = cohere_client.embed(texts=[query])
#     embedding = response.embeddings[0]
#     print(f"Generated embedding: {embedding[:10]}...")  # Print the first 10 elements for debugging
#     return embedding


# # Function to query Pinecone for the most similar response
# def query_pinecone(query_embedding):
#     # Ensure the query embedding is valid
#     if not isinstance(query_embedding, list) or not all(isinstance(i, float) for i in query_embedding):
#         raise ValueError("The query_embedding should be a list of floats.")
    
#     print(f"Query embedding length: {len(query_embedding)}")  # Debugging line to check the embedding length
#     print(f"Query embedding (first 10 elements): {query_embedding[:10]}...")  # Debugging line to print first 10 elements of the embedding
    
#     # Query Pinecone for the most similar vectors
#     result = index.query(
#         vector=query_embedding,  # The embedding you generated
#         top_k=1,  # Retrieve the top response
#         include_metadata=True  # Retrieve metadata along with the vectors
#     )
    
#     # If matches are found, return the response from metadata
#     if result['matches']:
#         return result['matches'][0]['metadata']['response']  # Return the response
#     else:
#         return "Sorry, I couldn't find a relevant answer to your question."

# @app.route('/')
# def home():
#     return '''
#         <h1>Parenting Chatbot</h1>
#         <form action="/ask" method="post">
#             <label for="query">Ask your question:</label><br>
#             <input type="text" id="query" name="query"><br><br>
#             <input type="submit" value="Ask">
#         </form>
#     '''

# @app.route('/ask', methods=['POST'])
# def ask():
#     # Get the user's query from the form
#     user_query = request.form['query']
    
#     # Generate embedding for the user's query using Cohere
#     query_embedding = generate_query_embedding(user_query)
    
#     # Query Pinecone for the most similar response
#     response = query_pinecone(query_embedding)
    
#     # Return the chatbot response to the user
#     return jsonify({"response": response})

# if __name__ == '__main__':
#     app.run(debug=True)















# from flask import Flask, request, jsonify, render_template
# import requests

# app = Flask(__name__)

# API_KEY = "AIzaSyAjgynltiF_SVDedXyDVyyqaqtbDGm7Dpk"
# API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/generate_response', methods=['POST'])
# def generate_response():
#     try:
#         user_message = request.json.get('message')
        
#         payload = {
#             "contents": [
#                 {
#                     "role": "user",
#                     "parts": [{"text": user_message}]
#                 }
#             ]
#         }

#         headers = {"Content-Type": "application/json"}
#         response = requests.post(API_URL, json=payload, headers=headers)

#         if response.status_code == 200:
#             data = response.json()
#             # bot_message = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
#             bot_message = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Sorry, no response available.')

#             return jsonify({"response": bot_message})
#         else:
#             return jsonify({"error": "Failed to get response from API"}), 500
    
#     except Exception as e:
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=8080)














# # app.py
# import os
# from flask import Flask, request, jsonify, render_template
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import torch
# import requests

# # Load Fine-Tuned GPT-2 Model and Tokenizer
# model_name = "fine_tuned_model1"
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# # Ensure the model uses the right device (GPU if available, else CPU)
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model.to(device)

# # Flask Setup
# app = Flask(__name__)

# # Gemini API configuration (example)
# GEMINI_API_URL = "https://api.gemini.com/v1/query"
# GEMINI_API_KEY = "AIzaSyAjgynltiF_SVDedXyDVyyqaqtbDGm7Dpk"


# def get_gpt2_response(query):
#     # Encode the input query
#     inputs = tokenizer.encode(query, return_tensors="pt").to(device)
    
#     # Generate response
#     with torch.no_grad():
#         outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
    
#     # Decode and return the generated response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response.strip()

# def get_gemini_response(query):
#     headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
#     data = {"query": query}
    
#     response = requests.post(GEMINI_API_URL, json=data, headers=headers)
    
#     if response.status_code == 200:
#         return response.json().get("response", "Sorry, I couldn't understand.")
#     else:
#         return "Sorry, I couldn't connect to Gemini API."



# @app.route('/')
# def home():
#     return render_template('index.html')

# # app.py
# @app.route('/chat', methods=['POST'])
# def chat():
#     query = request.json.get('query')
    
#     if query:
#         # Try generating a response with GPT-2
#         gpt2_response = get_gpt2_response(query)
        
#         # If GPT-2 response is not satisfactory, fall back to Gemini API
#         if not gpt2_response or len(gpt2_response.split()) < 2:
#             response = get_gemini_response(query)
#         else:
#             response = gpt2_response
        
#         return jsonify({"response": response})
#     else:
#         return jsonify({"error": "No query provided."}), 400



# if __name__ == "__main__":
#     app.run(debug=True, port=8080)

