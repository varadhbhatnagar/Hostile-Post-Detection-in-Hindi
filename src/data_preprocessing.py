import numpy as np
import pandas as pd
import re
import emoji

emoticon_list = ['XD', 'O:-)', ')-:', '(-:', ':-|', '@', '<3', '~,~', ':-B', \
'<l:0', '$_$', '8-)', ':-/', ':-(', '>:)', ':*)', '#-o', '*<:o)', '|-O', '~:0', \
':/', '=-O', ':-#', ':-J', '=D', 'B-)', ":'(", '*-*', ':)', '<><', ':o', '=()', \
'</3', '@~)~~~~', '//_^', '[¬º-°]¬', ':P', '^_^', ':-Q', '=^.^=', ':-*', "'=p'", \
':->', '<:3)~', ':-E', ';-)', '=)', '#', ':S', '(*v*)', 'O.o', '=8)', ':(', '<3', \
'(.V.)', ':>', ':-D', '=D', '=o', '(-}{-)', 'X-(', ':-@', ':-\\', '.X-p', ':-&', \
':-)(-:', '=/', '\\:D/', '{}', ':o3']

def extract_emoticons(s):
    emoticons = []

    for e in range(len(emoticon_list)):
        #TODO: Get multiple occurences of Emoticon in the result
        if emoticon_list[e] in s:
            emoticons.append(emoticon_list[e])
            s = s.replace(emoticon_list[e], '')
  
    return pd.Series({'Post': s, 'emoticons': emoticons})

def extract_reserved_words(s):

    reserved_words = re.findall(r'^(RT|FAV|&amp)', s)

    for i in reserved_words:
        n=s.replace(i,'')
        s=n

    return pd.Series({'Post': s, 'reserved_words': reserved_words})

def extract_emojis(s):

    emojis = [c for c in s if c in emoji.UNICODE_EMOJI]
    for i in emojis:
        n=s.replace(i,'')
        s=n
  
    return pd.Series({'Post': s, 'emojis': emojis})

def extract_hashtags(s):

    hashtags = list(part[1:] for part in s.split() if part.startswith('#'))
    for i in hashtags:
        n=s.replace('#'+i,'')
        s=n

    return pd.Series({'Post': s, 'hashtags': hashtags})

def extract_mentions(s):

    mentions = re.findall(r'(?:(?<=\s)|(?<=^))@.*?(?=\s|$)', s)
    for i in mentions:
        n=s.replace(i,'')
        s=n

    return pd.Series({'Post': s, 'mentions': mentions})

def extract_emails(s):

    emails = re.findall(r'[\w\.-]+@[\w\.-]+', s)

    for i in emails:
        n=s.replace(i,'')
        s=n

    return pd.Series({'Post': s, 'emails': emails})

def extract_urls(s):

    urls = re.findall(r'http\S+', s)

    for i in urls:
        n=s.replace(i,'')
        s=n

    return pd.Series({'Post': s, 'urls': urls})

def remove_stopwords(s):
    hindi_stopwords = pd.read_csv('hindi_stopwords.csv', header=None)[0].tolist()
    
    resultwords  = [word for word in s.split() if word not in hindi_stopwords]
    s = ' '.join(resultwords)

    return pd.Series({'Post': s})


def process_tweets(df):

    processed_df = pd.DataFrame()
    processed_df['Post'] = df['Post']
    processed_df['Labels Set'] = df['Labels Set']

    # df = df.apply(lambda x: extract_emails(x['Post']), axis=1)
    # processed_df['emails'] = df['emails']

    # df = df.apply(lambda x: extract_urls(x['Post']), axis=1)
    # processed_df['urls'] = df['urls']

    # df = df.apply(lambda x: extract_mentions(x['Post']), axis=1)
    # processed_df['mentions'] = df['mentions']

    # df = df.apply(lambda x: extract_hashtags(x['Post']), axis=1)
    # processed_df['hashtags'] = df['hashtags']

    # df = df.apply(lambda x: extract_emojis(x['Post']), axis=1)
    # processed_df['emojis'] = df['emojis']

    # df = df.apply(lambda x: extract_emoticons(x['Post']), axis=1)
    # processed_df['emoticons'] = df['emoticons']

    # df = df.apply(lambda x: extract_reserved_words(x['Post']), axis=1)
    # processed_df['reserved_words'] = df['reserved_words']

    df = df.apply(lambda x: remove_stopwords(x['Post']), axis=1)
    processed_df['Filtered_Post'] = df['Post']

    return processed_df

train_file_path = '../data/raw/train.csv'
val_file_path = '../data/raw/val.csv'

train_data = pd.read_csv(train_file_path, header=0, index_col=0, usecols=[0,1,2])
val_data = pd.read_csv(val_file_path, header=0, index_col=0, usecols=[0,1,2])

print("Train Data Shape = {}".format(train_data.shape))
print("Val Data Shape = {}".format(val_data.shape))


processed_train_data = process_tweets(train_data)
processed_train_data.to_csv('train.csv')

processed_val_data = process_tweets(val_data)
processed_val_data.to_csv('val.csv')
