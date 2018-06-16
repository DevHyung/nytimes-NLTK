import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords

if __name__=="__main__":
    # 기사의 내용 수집하기
    article = "" # 기사내용 저장변수
    html = requests.get('https://www.nytimes.com/2017/06/12/well/live/having-friends-is-good-for-you.html')
    bs4 = BeautifulSoup(html.text,'lxml')
    pTags = bs4.find_all('p',class_='css-1i0edl6 e2kc3sl0')
    for pTag in pTags:
        article += pTag.get_text().strip()
    # 불필요한 기호나 마크 제거 by 정규표현식
    article = re.sub('[^가-힣0-9a-zA-Z\\s]', '', article)
    print(article)


