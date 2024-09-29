from time import sleep
import pandas as pd
from semanticscholar import SemanticScholar
import tqdm

# 创建SemanticScholar对象
sch = SemanticScholar()
df = pd.read_csv('group/nips2023_papers.csv')
pbar = tqdm.tqdm(total=len(df))

# 定义函数，用于获取作者单位和引用量
def get_author_info(title, authors):
    # 搜索论文
    while True:
        try:
            paper = sch.search_paper(title)
            sleep(1)
            break
        except Exception as e:
            sleep(5)
            pass
    # 检查是否找到论文
    pbar.update(1)
    if paper is None:
        return None, None
    # 获取作者信息
    author_info = paper.authors
    # 检查作者信息是否为空
    if author_info is None:
        return None, None
    # 提取作者单位和引用量
    author_affiliations = [author.affiliations for author in author_info]
    citation_count = paper.citationCount
    return author_affiliations, citation_count

# 应用函数获取作者单位和引用量
df['facility'], df['cites'] = zip(*df.apply(lambda x: get_author_info(x['title'], x['authors']), axis=1))
pbar.close()
# 将结果保存为csv文件
csv_path = './group/nips2023_papers_new.csv'
df.to_csv(csv_path)