# Importing libraries
from transformers import CamembertTokenizer, CamembertModel
import torch
import pickle
import warnings
from transformers import CamembertTokenizer

warnings.filterwarnings('ignore')

"""
Prediction of a score from a new review / comment
"""

# Loading the model
#with open('./prediction/lgbm_model.pkl', 'rb') as model_file:
with open('./lgbm_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Load the tokenizer and model
tokenizer = CamembertTokenizer.from_pretrained('camembert-base')
model = CamembertModel.from_pretrained('camembert-base')

# Function to embedding a new sentence
def get_sentence_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding='max_length', max_length=512)
    if torch.cuda.is_available():
        inputs = {k: v.to('cuda') for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].squeeze().detach()
    if embeddings.is_cuda:
        embeddings = embeddings.cpu()
    return embeddings.numpy()

# Prediction 
def predict(title, comment, main_category, sub_category, sub_sub_category, location):
    # Construct the text
    text = " ".join([title, comment, main_category, sub_category, sub_sub_category, location]).strip()
    senetence_embedded = get_sentence_embedding(text)
    # Model prediction
    prediction = loaded_model.predict([senetence_embedded])[0]  
    return {"text": text, "score": prediction}

warnings.filterwarnings('ignore', category=DeprecationWarning)

# print(predict('mauvais','mauvais','mauvais','mauvais','mauvais','mauvais'))
