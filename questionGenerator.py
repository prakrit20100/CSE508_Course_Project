from lmqg import TransformersQG
import pandas as pd
import random
import numpy as np

def phrasing(temp_df):
    shap = temp_df[temp_df['subclassification'].notna()].shape[0]
    cl = list(temp_df['classification'])[0] if shap==0 else list(temp_df['subclassification'])[0]+' '+list(temp_df['classification'])[0] 
    s = f"{list(temp_df['title'])[0]}, a {cl} by {list(temp_df['attribution'])[0]}, was developed over a period spanning from {int(list(temp_df['beginyear'])[0])} to {int(list(temp_df['endyear'])[0])}, executed in the medium of {list(temp_df['medium'])[0]}."
    return [s,random.choice([['title',list(temp_df['title'])[0]],['attribution',list(temp_df['attribution'])[0]],['medium',list(temp_df['medium'])[0]],['endyear',int(list(temp_df['endyear'])[0])],['classification',list(temp_df['classification'])[0]]])]

def generateQuestion(n):
    model = TransformersQG(model='lmqg/t5-base-squad-qg')
    new_df = pd.read_csv('merged_df.csv')
    random_indexes = np.random.choice(new_df.index, size=200, replace=False)
    # print(random_indexes)
    # Creating a new DataFrame with selected indexes
    new_df = pd.DataFrame(new_df.loc[random_indexes])
    # print(new_df)
    t = n
    Required_Data = []

    for tt in range(min(6,t)):
        Question_data = {
            'question': '',
            'options': [],
            'correctOption': '',
            'image' : '',
            'review': ''
        }

        #Question and correct option
        obj_id = new_df['objectid']
        idd = random.choice(list(obj_id))
        phras = phrasing(new_df[new_df['objectid']==idd])
        context, answer = [phras[0]],[str(phras[1][1])]
        question = model.generate_q(list_context=context, list_answer=answer)
        Question_data['question'] = question[0]    #Question Store
        Question_data['correctOption'] = answer[0]

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

# print(generateQuestion(1))
