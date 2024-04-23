from lmqg import TransformersQG
import pandas as pd
import random
import numpy as np
import os
import spacy
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
from weaviate.embedded import EmbeddedOptions
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

nlp = spacy.load("en_core_web_sm")


model = TransformersQG(model='lmqg/t5-base-squad-qg')
new_df = None
# new_df = pd.read_csv('newMerged_df.csv')
random_indexes = None
# random_indexes = np.random.choice(new_df.index, size=200, replace=False)
# csv_file_path = '/content/drive/MyDrive/merged_df.csv'
# df = pd.read_csv(csv_file_path)
# df = df.iloc[:200]

# print(random_indexes)
# Creating a new DataFrame with selected indexes
# new_df = pd.DataFrame(new_df.loc[random_indexes])

text_file_path = None
# text_file_path = 'main_doc.txt'
# with open(text_file_path, 'w', encoding='utf-8') as file:
#     for index, row in new_df.iterrows():
#         line = ", ".join([f"{col}: {row[col]}" for col in new_df.columns])
#         file.write(line + "\n")

# print("Data has been successfully written to the text file.")
loader = None
# loader = TextLoader('main_doc.txt')
documents = None
# documents = loader.load()
text_splitter = None
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
chunks = None
# chunks = text_splitter.split_documents(documents)
client = None
# client = weaviate.Client(
# embedded_options = EmbeddedOptions()
# )
vectorstore = None
# vectorstore = Weaviate.from_documents(
#     client = client,
#     documents = chunks,
#     embedding = OpenAIEmbeddings(),
#     by_text = False
# )
retriever = None
# retriever = vectorstore.as_retriever()

def phrasing(temp_df):
    shap = temp_df[temp_df['subclassification'].notna()].shape[0]
    cl = list(temp_df['classification'])[0] if shap==0 else list(temp_df['subclassification'])[0]+' '+list(temp_df['classification'])[0] 
    s = f"{list(temp_df['title'])[0]}, a {cl} by {list(temp_df['attribution'])[0]}, was developed over a period spanning from {int(list(temp_df['beginyear'])[0])} to {int(list(temp_df['endyear'])[0])}, executed in the medium of {list(temp_df['medium'])[0]}."
    return [s,random.choice([['title',list(temp_df['title'])[0]],['attribution',list(temp_df['attribution'])[0]],['medium',list(temp_df['medium'])[0]],['endyear',int(list(temp_df['endyear'])[0])],['classification',list(temp_df['classification'])[0]]])]

def updateCSV():
    new_df.to_csv('newMerged_df.csv')

def updateDifficulty(id, review_text, review):
    learningRate = 0.01

    # if review_text:
    #     print(review_text)
    
    # print(review)
    # print(f"Debugger 1 {list(new_df[new_df['objectid']==id]['Difficulty'])[0]}")
    # print(f"id recieved is: {id}")

    if list(new_df[new_df['objectid']==id]['Difficulty'])[0]<=4:
        if review=='easy':
            pass
        elif review=='medium':
            new_df.loc[new_df['objectid'] == id, 'Difficulty'] += learningRate
        elif review=='hard':
            new_df.loc[new_df['objectid'] == id, 'Difficulty'] += 2*learningRate
        else:
            pass
    elif list(new_df[new_df['objectid']==id]['Difficulty'])[0]<=7:
        if review=='easy':
            new_df.loc[new_df['objectid'] == id, 'Difficulty'] -= learningRate
        elif review=='medium':
            pass
        elif review=='hard':
            new_df.loc[new_df['objectid'] == id, 'Difficulty'] += learningRate
        else:
            pass
    else:
        if review=='easy':
            new_df.loc[new_df['objectid'] == id, 'Difficulty'] -= 2*learningRate
        elif review=='medium':
            new_df.loc[new_df['objectid'] == id, 'Difficulty'] -= learningRate
        elif review=='hard':
            pass
        else:
            pass
    pass


def initalize():
    global new_df
    global random_indexes
    global text_file_path
    global loader
    global documents
    global text_splitter
    global chunks
    global client
    global vectorstore
    global retriever

    os.environ['OPENAI_API_KEY'] = 'sk-proj-AD8Av3qEYHvSVRwY5TsGT3BlbkFJHRoClOryP5RZWgeASOSZ'
    new_df = pd.read_csv('newMerged_df.csv')
    random_indexes = np.random.choice(new_df.index, size=100, replace=False)
    new_df = pd.DataFrame(new_df.loc[random_indexes])

    text_file_path = 'main_doc.txt'
    with open(text_file_path, 'w', encoding='utf-8') as file:
        for index, row in new_df.iterrows():
            line = ", ".join([f"{col}: {row[col]}" for col in new_df.columns])
            file.write(line + "\n")
            file.write("\n---\n")

    print("Data has been successfully written to the text file.")
    loader = TextLoader('main_doc.txt')
    documents = loader.load()
    # chunks = smart_split(documents)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    client = weaviate.Client(
    embedded_options = EmbeddedOptions()
    )

    vectorstore = Weaviate.from_documents(
        client = client,
        documents = chunks,
        embedding = OpenAIEmbeddings(),
        by_text = False
      ) 
    retriever = vectorstore.as_retriever()

def smart_split(documents, max_length=10000, overlap=200):
    split_docs = []
    for document in documents:
        text = str(document)  # Ensures we are working with a string representation of the document
        start = 0
        while start < len(text):
            end = start + max_length
            if end > len(text):
                end = len(text)
            else:
                # Move the end to the nearest delimiter to avoid cutting in the middle of a data point
                end = text.rfind('\n---\n', start, end) + 5
            split_docs.append(text[start:end].strip())
            start = end - overlap  # Use overlap
    return split_docs
# def split_into_chunks(document, max_tokens=16000):

#     chunks = []
#     current_chunk = []
#     current_tokens = 0

#     for sentence in nlp(document).sents:
#         sentence_text = sentence.text.strip()
#         sentence_tokens = len(nlp(sentence_text))
        
#         if current_tokens + sentence_tokens > max_tokens:
#             chunks.append(' '.join(current_chunk))
#             current_chunk = [sentence_text]
#             current_tokens = sentence_tokens
#         else:
#             current_chunk.append(sentence_text)
#             current_tokens += sentence_tokens

#     if current_chunk:
#         chunks.append(' '.join(current_chunk))

#     return chunks
def generateQuestion(n, diff):
    t = n
    Required_Data = []

    for tt in range(min(6,t)):
        Question_data = {
            'question': '',
            'options': [],
            'correctOption': '',
            'image' : '',
            'review': '',
            'title' : '',
            'id' : ''
        }

        #Question and correct option
        # obj_id = new_df['objectid']
        # idd = random.choice(list(obj_id))
        random_row = pd.DataFrame()
        # print(f"diffiliculty recieved: {diff}")
        if diff=='easy':
            random_row = new_df.loc[new_df['Difficulty'].between(0,4)].sample(n=1)
        elif diff=='medium':
            random_row = new_df.loc[new_df['Difficulty'].between(4,7)].sample(n=1)
        elif diff=='hard':
            random_row = new_df.loc[new_df['Difficulty'].between(7,10)].sample(n=1)
        print(random_row)
        try:
            idd = random_row['objectid'].values[0]
        except:
            temp_ind = np.random.choice(new_df.index, size=1, replace=False)
            temp_df = pd.DataFrame(new_df.loc[temp_ind])
            print(temp_df)
            idd = temp_df['objectid'].values[0]
        print(idd)
        phras = phrasing(new_df[new_df['objectid']==idd])
        context, answer = [phras[0]],[str(phras[1][1])]
        question = model.generate_q(list_context=context, list_answer=answer)
        Question_data['question'] = question[0]    #Question Store
        Question_data['correctOption'] = answer[0]
        Question_data['title'] = new_df[new_df['objectid']==idd]['title']
        Question_data['id'] = idd

        #Image link
        temp=list(new_df[new_df['objectid']==idd]['iiifthumburl'])[0]
        temp = temp[:68]+'400,400'+temp[75:]
        Question_data['image'] = temp   #Image Link Store

        #Options
        uniq = random.sample(list(new_df[phras[1][0]].unique()),4)
        if phras[1][0] == 'endyear':
            uniq = [str(int(un)) for un in uniq]
        if answer not in uniq:
            uniq[3]=str(answer[0])
        uniq = random.sample(uniq,4)
        Question_data['options'] = [str(uniq[0]), str(uniq[1]), str(uniq[2]), str(uniq[3])]

        #Review
        Question_data['review'] = context[0]

        Required_Data.append(Question_data)

    return Required_Data


def generateQuestionByID(id):
    gen_df = pd.read_csv("merged_df.csv")
    Required_Data = []
    Question_data = {
        'question': '',
        'options': [],
        'correctOption': '',
        'image' : '',
        'review': '',
        'title' : '',
        'id' : ''
    }

        #Question and correct option
    idd = id
    # print(gen_df[gen_df['objectid']==idd])
    phras = phrasing(gen_df[gen_df['objectid']==idd])
    context, answer = [phras[0]],[str(phras[1][1])]
    question = model.generate_q(list_context=context, list_answer=answer)
    Question_data['question'] = question[0]    #Question Store
    Question_data['correctOption'] = answer[0]
    Question_data['title'] = gen_df[gen_df['objectid']==idd]['title']
    Question_data['id'] = idd

    #Image link
    temp=list(gen_df[gen_df['objectid']==idd]['iiifthumburl'])[0]
    temp = temp[:68]+'400,400'+temp[75:]
    Question_data['image'] = temp   #Image Link Store

    #Options
    uniq = random.sample(list(gen_df[phras[1][0]].unique()),4)
    if phras[1][0] == 'endyear':
        uniq = [str(int(un)) for un in uniq]
    if answer not in uniq:
        uniq[3]=str(answer[0])
    uniq = random.sample(uniq,4)
    Question_data['options'] = [str(uniq[0]), str(uniq[1]), str(uniq[2]), str(uniq[3])]

    #Review
    Question_data['review'] = context[0]
    Required_Data.append(Question_data)
    return Required_Data


# print(generateQuestion(1))
def rag(title):

    print("This is the title going into rag funtion : ", title)
    template = """You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    Question: {question}
    Context: {context}
    Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0)

    rag_chain = (
        {"context": retriever,  "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    query = f"Can you educate me about {title} (Do not mention about the difficulty)?"
    return rag_chain.invoke(query)
