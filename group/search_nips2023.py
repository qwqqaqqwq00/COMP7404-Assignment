import requests
from bs4 import BeautifulSoup
import pandas as pd
from googleapiclient.discovery import build

def fetch_paper_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    papers = []
    # 假设论文标题和作者信息都包含在特定的HTML标签内
    for item in soup.find_all('li', class_='conference'):
        title = item.find('a', title='paper title').text.strip()
        authors = item.find('i').text.strip()
        papers.append({'title': title, 'authors': authors})
    
    return papers

nips_url = 'https://proceedings.neurips.cc/paper/2023'
papers = fetch_paper_list(nips_url)

df_papers = pd.DataFrame(papers)
df_papers.to_csv('group/nips2023_papers.csv')