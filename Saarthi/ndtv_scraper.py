from urllib.request import urlopen
from bs4 import BeautifulSoup

import pandas as pd 

# Function to remove English text
def remove_eng_char(text):
    alphabets = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM()')
    st2 = text
    for i in text:
        if i in alphabets:
            st2 = st2.replace(i,"")
    return(st2)

# Creating dataframe 
columns = ['source','category','text']
df = pd.DataFrame(columns=columns)

categories_news = ['india','world','filmy','television','blogs','politics','sports','business','lifestyle']

for category in categories_news:
    # Extracting different categories url
    url  = "https://khabar.ndtv.com/news/" + str(category) + "/page-"
    text_lst = []

    for url_index in range(1,51):
        web_page = urlopen(url+str(url_index))

        soup = BeautifulSoup(web_page, 'html.parser')

        # Extracting individual articles url
        url_lst = []
        for extract_div in soup.findAll("div", {"class" : "nstory_header"}):
            url_lst.append(extract_div.a['href'])

        # Extracting text from url
        for i in url_lst:
            url_i = i
            web_page_i = urlopen(url_i)
            soup_i = BeautifulSoup(web_page_i, 'html.parser')
            for j in soup_i.findAll("span", {'class': 'ins_storybody listmargin'}):
                para_str = ""
                for paragraph in j.findAll("p"):
                    for letter in paragraph.text:
                        para = remove_eng_char(paragraph.text)
                    para_str = para_str + " " + para
                text_lst.append(para_str)
                
                # Append to dataframe 
                df = df.append({'source':'ndtv','category':str(category),'text':para_str}, ignore_index=True)
df.to_csv('ndtv_hindi_data')
