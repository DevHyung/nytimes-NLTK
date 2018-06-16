import requests
from bs4 import BeautifulSoup
import re
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from PIL import Image
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main__":
    tknzr = TweetTokenizer()
    lemmatizer = WordNetLemmatizer()

    # 기사의 내용 수집하기
    article = "" # 기사내용 저장변수
    html = requests.get('https://www.nytimes.com/2017/06/12/well/live/having-friends-is-good-for-you.html')
    bs4 = BeautifulSoup(html.text,'lxml')
    pTags = bs4.find_all('p',class_='css-1i0edl6 e2kc3sl0')
    for pTag in pTags:
        article += pTag.get_text().strip()
    # 불필요한 기호나 마크 제거 정규표현식이용
    # 대문자 -> 소문자
    article = re.sub('[^가-힣0-9a-zA-Z\\s]', '', article.lower())
    tmp = article
    print("[ #1 불필요한 기호나 마크 제거 및 대문자 -> 소문자] ")
    print(article)
    print("___"*30)
    # tokenize
    print("[ #2 tokenize ] ")
    tokens =tknzr.tokenize(article)
    print(tokens)
    print("___" * 30)
    # 품사 구별 및 찾기
    print("[ #3 품사 구별 및 찾기 , 명사만 추출] ")
    tags = pos_tag(tokens)
    # 만약에 명사만 찾고 싶다면 AREA1 를 찾고싶은 품사로 변경
    for word, pos in tags:
        # 명사 단어 추출
        if pos == "NN": # AREA1
            print ( word, end=',' )
    print("___" * 30)
    #원형찾기
    print("[ #4 원형 찾기 ] ")
    for word, pos in tags:
        print("단어 : {} , {}   => 원형 {} ".format(word,pos,lemmatizer.lemmatize(word)))
    print("___" * 30)
    # 불용어제거
    print("[ #5 불용어 제거] ")
    stopWords = set(stopwords.words('english'))
    # 내가 만든 불용어 사전
    myStopWords = set(['this','is','my','stop','word'])
    filteredTokens = [w for w in tokens if not w in stopWords if not w in myStopWords]
    filteredTags = pos_tag(filteredTokens)
    print(filteredTokens)
    print("___" * 30)

    # counter 모듈 이용 상위 10개명사 추출
    print("[ #6 빈도 분석 상위 10개 명사] ")
    NNList = [] # 명사단어만 저잘할 리스트
    for word, pos in filteredTags:
        # 명사 단어 추출
        if pos == "NN": # AREA1
            NNList.append(word)
    cnt = Counter(NNList)
    print(cnt.most_common(10))
    print("___" * 30)
    print("[ #7 워드클라우드 ")
    #mask 모양 본따기
    alice_mask = np.array(Image.open("./alice.png"))
    wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask)
    wc.generate(article)
    # store to file
    wc.to_file("./alicewc.png")
    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    print("___" * 30)
