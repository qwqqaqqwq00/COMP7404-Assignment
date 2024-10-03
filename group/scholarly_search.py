import json
import time
import pandas as pd
from scholarly import scholarly
from scholarly import ProxyGenerator
import tqdm

# pg = ProxyGenerator()
# pg.FreeProxies()
# pg.SingleProxy(http="http://localhost:10809?sslVerify=false", https="https://localhost:10809?sslVerify=false")
# scholarly.use_proxy(pg)

df = pd.read_csv('new_nips2023_papers.csv')
# import scholarly as sch
scholarly.set_retries(10)
scholarly.set_timeout(30)
pbar = tqdm.tqdm(total=len(df))
# 定义函数，用于获取作者单位和引用量
def get_author_info(title, authors):
    try:
        # title = row['title']
        # authors = row['authors']
        # 搜索论文
        search_query = scholarly.search_single_pub(title)
        paper = search_query
        # time.sleep(1)
        # pbar.update(1)
        citation_count = int(paper['num_citations'])
        author_id = [p for p in paper['author_id'] if len(p)>0]
        author_query = scholarly.search_author_id(author_id[0])
        first_author_info = author_query
        # time.sleep(1)
        # pbar.update(1)
        first_author_cited = first_author_info['citedby']
        first_author_interest = first_author_info['interests']
        first_author_affiliation = first_author_info['affiliation']
        first_author_email = first_author_info['email_domain']
        return citation_count, first_author_cited, first_author_affiliation, first_author_email, first_author_interest
    except Exception as e:
        with open('errlog.txt', 'a') as f:
            f.write(str(e))
        return 0, 0, "", "", []

df['paperCites'] = 0
df['authorCites'] = 0
df['affiliation'] = ""
df['emailDomain'] = ""
df['interests'] = ""
for idx in range(len(df)):
    pbar.update(1)
    if idx > 0 and idx % 10 == 0:
        time.sleep(300)
    try:
        title = df.loc[idx, 'title']
        authors = df.loc[idx, 'authors']
    except:
        continue
    if df.loc[idx, 'emailDomain'] != "":
        continue
    pc, ac, a, e, i = get_author_info(title, authors)
    df.loc[idx, 'paperCites'] = pc
    df.loc[idx, 'authorCites'] = ac
    df.loc[idx, 'affiliation'] = a
    df.loc[idx, 'emailDomain'] = e
    df.loc[idx, 'interests'] = ''.join(i)
    df.to_csv('new_nips2023_papers.csv')
pbar.close()
