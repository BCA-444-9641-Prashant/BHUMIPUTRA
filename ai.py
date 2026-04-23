import nltk
import random
import string
import warnings
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# Load farming knowledge base
try:
    with open('ai_knowledge.txt', 'r', errors='ignore') as f:
        raw = f.read().lower()
except FileNotFoundError:
    # Default farming knowledge if file doesn't exist
    raw = """
    Farming is the practice of cultivating plants and livestock. 
    Modern farming involves various techniques including irrigation, crop rotation, and use of fertilizers.
    Common crops include wheat, rice, corn, and vegetables.
    Soil health is important for successful farming.
    Organic farming avoids synthetic pesticides and fertilizers.
    Sustainable farming practices help maintain environmental balance.
    Weather conditions greatly affect farming outcomes.
    Farmers should monitor soil moisture levels regularly.
    Proper irrigation systems can improve crop yields.
    Pest control is essential for protecting crops.
    Modern technology can help optimize farming operations.
    """

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Download required NLTK data
try:
    nltk.download('punkt')
    nltk.download('wordnet')
except:
    pass

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    """Lemmatize tokens."""
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    """Normalize text by lemmatizing and removing punctuation."""
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "hey", "good morning", "good afternoon", "good evening")
GREETING_RESPONSES = ["Hello! I'm your farming assistant. How can I help you today?", 
                      "Hi there! What farming questions do you have?", 
                      "Hey! Ready to help with your farming needs!",
                      "Good day! How can I assist you with farming?"]

FARMING_KEYWORDS = {
    "crop": "Crops are plants grown for food. Common crops include wheat, rice, corn, and vegetables. Choose crops based on your climate and soil conditions.",
    "soil": "Soil health is crucial for farming. Test your soil regularly and add organic matter. Good soil should have proper pH balance and nutrients.",
    "water": "Proper irrigation is essential. Most crops need 1-2 inches of water per week. Consider drip irrigation for efficiency.",
    "fertilizer": "Fertilizers provide nutrients to soil. Use organic fertilizers like compost or manure for sustainable farming. Follow recommended application rates.",
    "pest": "Pest control is important. Use integrated pest management combining biological, cultural, and chemical methods when necessary.",
    "harvest": "Harvest timing affects crop quality. Monitor maturity indicators and harvest during dry weather for best results.",
    "weather": "Weather impacts farming significantly. Plan activities around seasonal patterns and use weather forecasting tools.",
    "organic": "Organic farming avoids synthetic chemicals. Focus on soil health, crop rotation, and natural pest control methods.",
    "irrigation": "Irrigation systems include drip, sprinkler, and flood methods. Choose based on crop needs and water availability.",
    "seed": "Quality seeds are essential. Choose disease-resistant varieties adapted to your local conditions. Store seeds properly."
}

def greeting(sentence):
    """Check if the sentence contains a greeting and return an appropriate response."""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
    return None

def check_farming_keywords(sentence):
    """Check for specific farming keywords and provide relevant responses."""
    sentence_lower = sentence.lower()
    for keyword, response in FARMING_KEYWORDS.items():
        if keyword in sentence_lower:
            return response
    return None

def response(user_response):
    """Generate a response based on the user's input."""
    # Check for greetings first
    greet_response = greeting(user_response)
    if greet_response:
        return greet_response
    
    # Check for specific farming keywords
    keyword_response = check_farming_keywords(user_response)
    if keyword_response:
        return keyword_response
    
    # Add user response to tokens for similarity matching
    sent_tokens.append(user_response)
    
    try:
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words="english")
        tfidf = TfidfVec.fit_transform(sent_tokens)
        
        # Compute cosine similarity
        vals = cosine_similarity(tfidf[-1], tfidf[:-1])
        idx = vals.argsort()[0][-1]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-1]
        
        # Remove the user's input after processing
        sent_tokens.pop()
        
        # If similarity score is very low, return a default response
        if req_tfidf == 0:
            return "I'm still learning about farming. Could you provide more details about your question? I can help with topics like crops, soil, water, fertilizers, pests, and harvesting."
        else:
            return sent_tokens[idx]
            
    except Exception as e:
        sent_tokens.pop()  # Ensure we remove the user input even if there's an error
        return "I'm having trouble processing that. Could you rephrase your farming question?"

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat requests."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"response": "Please provide a message."})
        
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"response": "Please enter a message."})
        
        # Generate response
        bot_response = response(user_message)
        
        return jsonify({"response": bot_response})
        
    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"})

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "AI Farming Assistant"})

if __name__ == "__main__":
    print("Starting AI Farming Assistant...")
    app.run(host="0.0.0.0", port=5000, debug=True)
