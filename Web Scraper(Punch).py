import pandas as pd
import requests
from bs4 import BeautifulSoup

articles = []
categories = ['news', 'metro-plus', 'sports', 'video', 'business']
for cat in categories:
    url = f'https://punchng.com/topics/{cat}/'
    response = requests.get(url).text

    soup = BeautifulSoup(response, 'html.parser')
    article_container = soup.find('div', class_='latest-news-timeline-section')
    article_temp = article_container.find_all_next('article')

    for article in article_temp:
        title = article.find('h1', class_='post-title').text.strip().replace(' ', '')
        excerpt = article.find('p', class_='post-excerpt').text.strip().replace(' ', '')
        date = article.find('span', class_='post-date').text.strip()
        article_link = article.find('a')['href']

        articles.append({
            'category': cat,
            'title': title,
            'excerpt': excerpt,
            'date': date,
            'links': article_link,
        })

    for arti in articles:
        article_page = requests.get(arti['links']).text
        article_soup = BeautifulSoup(article_page, 'html.parser')
        arti['author'] = article_soup.find('span', class_='post-author').text.strip().replace(' ', '')
        arti['content'] = article_soup.find('div', class_='post-content').text.strip().replace(' ', '')
        if article_soup.find('div', class_='post-image-wrapper') is None:
            arti['image'] = ''
        else:
            arti['image'] = article_soup.find('div', class_='post-image-wrapper').find_next('figure').find_next('img')['src']
    print(f'Category {cat} is Completed.')

df = pd.DataFrame(articles)
df.to_csv('punch.csv', index=False)
print('Done')
