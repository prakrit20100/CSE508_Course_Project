import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import spacy
from fuzzywuzzy import process
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import torchvision.transforms as transforms
import torchvision.models as models
import torch
import numpy as np
import pickle
from sklearn.decomposition import PCA
import faiss
from tqdm import tqdm

nlp = spacy.load('en_core_web_sm')

def clean_text(text):

    if pd.isna(text):
        return ""
    
    text = text.lower()

    text = re.sub(r'[\W_]+', ' ', text)

    text = re.sub(r'\s+', ' ', text).strip()

    return text

data_path = 'merged_df.csv'
data = pd.read_csv(data_path)

textual_columns = data.select_dtypes(include=['object']).columns
transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
pca = load_data('pca_model.pkl')
index = faiss.read_index('faiss_index.index')
ids = load_data('ids.pkl')
data[textual_columns] = data[textual_columns].applymap(clean_text)



def fuzzy_match_titles(query, data, limit=5):

    titles = data['title'].tolist()
    
    results = process.extract(query, titles, limit=limit)
    
    matched_indices = [data[data['title'] == result[0]].index[0] for result in results]
    
    return data.iloc[matched_indices[0]]['objectid']

def preprocess_and_vectorize(data, weights):
    combined_text = data.apply(lambda row: ' '.join(row[col] * weights.get(col, 1) 
                                                    for col in textual_columns), axis=1)
    
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_text)
    
    return tfidf_vectorizer, tfidf_matrix

def analyze_query_and_adjust_weights(query):
    doc = nlp(query)

    weights = {col: 1 for col in textual_columns} 

    for ent in doc.ents:
        if "title" in ent.text.lower():
            weights['title'] = 3

        if "description" in ent.text.lower():
            weights['assistivetext'] = 3 

        if "provenance" in ent.text.lower():
            weights['provenancetext'] = 3 
    return weights

def search_dataset(query,context, data):

    weights = analyze_query_and_adjust_weights(query)
    processed_query = ' '.join([token.lemma_ for token in nlp(query) 
                                    if not token.is_stop and not token.is_punct])
    if context =='title':
        return fuzzy_match_titles(processed_query,data)

    else:

        tfidf_vectorizer, tfidf_matrix = preprocess_and_vectorize(data, weights)
        
        query_vec = tfidf_vectorizer.transform([processed_query])
        
        similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        top_indices = similarity.argsort()[-5:][::-1]
        
        return data.iloc[top_indices[0]]['objectid']
    
def get_image(path):
    # response = requests.get(path)
    image = Image.open(path).convert('RGB')
    image = transform(image)
    image_tensor = image.unsqueeze(0)
    # if torch.cuda.is_available():
    #     image_tensor = image_tensor.to('cuda')
    return image_tensor    
def extract_features(image_tensor):
    model = models.resnet50(pretrained=True)
    # if torch.cuda.is_available():
    #     model = model.to('cuda')
    model.eval()

    # Image preprocessing transformations

    with torch.no_grad():
        features = model(image_tensor)
    return features.cpu().numpy().flatten()

def query_image(path, pca, index, ids, k=3):
    image_tensor = get_image(path)
    image_features = extract_features(image_tensor)
    image_pca = pca.transform([image_features])
    _, I = index.search(image_pca.astype('float32'), k)
    return [ids[i] for i in I[0]]

def get_results_image(path):
    ans_list = query_image(path,pca,index,ids,k=3)
    return ans_list[0]


def return_result(query, context):
    results = search_dataset(query,context, data)
    print(results)
    return int(results)
