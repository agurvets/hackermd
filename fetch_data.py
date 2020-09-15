import csv
from urllib.parse import urlparse

import requests

# make this a little smarter by being case-insensitive
relevanceTerms=["therap","deadly","covid","virus","infect","nature","doctor","surgeon","body","surgery","hospital","nurse","medical","medicine","drug","health","DNA","RNA","diagnos","disease","biom","psycho","scientist"]
def scrape_item(story):
    item_url = 'https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty'
    item_response = requests.get(item_url.format(item_id=story))
    item = item_response.json()
    if not item:
        return
    item.pop('kids', None)
    fields = list(item.keys())
    if 'url' not in fields:
        fields.append('url')
        item['url'] = ''
    if 'text' not in fields:
        fields.append('text')
        item['text'] = ''

    fields.append('domain')
    item['domain'] = ''
    if item['url']:
        parsed_uri = urlparse(item['url'])
        domain = parsed_uri.netloc
        if domain.count('.') > 1:
            if domain.startswith(sub_domains):
                domain = domain.split('.', 1)[1]
        item['domain'] = domain
    return item

def check_for_relevance(story):
    title=story['title']
    for term in relevanceTerms:
        if term in title:
            return True
    return False


if __name__ == '__main__':
    urls = {
        'top': 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    }

    sub_domains = ('www.', 'mail.', 'blog.', 'ns.', 'smtp.', 'webmail.', 'docs.', 'jobs.', 'cs.', 'apply.', 'boards.')

    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    stories = response.json()

    items = []
    for story in stories:
        item = scrape_item(story)
        if check_for_relevance(item):
            items.append(item)

    with open('data/top.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)
