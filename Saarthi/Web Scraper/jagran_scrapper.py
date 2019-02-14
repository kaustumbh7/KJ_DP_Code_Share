
# coding: utf-8

# In[ ]:


from urllib.request import urlopen,Request

from bs4 import BeautifulSoup

import pandas as pd 


# In[ ]:


# Function to remove English text
def remove_eng_char(text):
    alphabets = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM()')
    st2 = text
    for i in text:
        if i in alphabets:
            st2 = st2.replace(i,"")
    return(st2)


# In[ ]:


# Creating dataframe
columns = ['source','category','text']
df = pd.DataFrame(columns=columns)


# In[ ]:


#Different categories of news
category_news = ["cricket/apni-baat","politics/national","politics/international","technology/tech-news","business/top15","lifestyle/travel-tourism","news/national-news","entertainment/bollywood"]

for category in category_news:
    txt_lst=[]

    #url_lst=[]
    for i in range(2,3):
        # Extracting different categories url
        url = "https://www.jagran.com/" + str(category) + "-news-hindi-page"+str(i)+".html"
        req=Request(url,headers={'User-Agent':'Mozilla/5.0'})
        web_page = urlopen(req).read()
        soup = BeautifulSoup(web_page, 'html.parser')
        # Extracting individual articles url
        url_lst=[]
        for extract_div in soup.findAll("div", {"class" : "newsFJagran"}):
            for extract_a in extract_div.findAll("a"):
                url_lst.append(extract_a['href'])
        for i in url_lst:
            # Extracting text from url
            url_i = "https://www.jagran.com"+i
            req=Request(url_i,headers={'User-Agent':'Mozilla/5.0'})
            web_page_i = urlopen(req).read()
            soup_i = BeautifulSoup(web_page_i, 'html.parser')
            for j in soup_i.findAll("div", {'class': 'articleBody'}):
                para_str = ""
                for paragraph in j.findAll("p"):
                    for letter in paragraph.text:
                        para = remove_eng_char(paragraph.text)
                    para_str = para_str + " " + para
                txt_lst.append(para_str)
                df = df.append({'source':'jagran','category':str(category),'text':para_str}, ignore_index=True)
    print(txt_lst)
df.to_csv('jagran_hindi_data')

