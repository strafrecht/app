from bs4 import *
import requests
import json
import time
import os

def get_json():
    f = open('newsscrape.json')
    data = json.load(f)
    return data

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

def get_article(link_source, article_link):
    base_dir = os.getcwd()
    dir_name = "news_content"
    dir_path = os.path.join(base_dir, dir_name)

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    link_soup = BeautifulSoup(link_source, 'lxml')

    date = link_soup.find('p', class_='dachzeile')
    try:
        date_text = date.text
        date_text = "".join(line.strip() for line in date_text.split("\n"))
    except:
        print("date not found")
        pass
    # print(date_text)

    title = date.find_next('h1')
    try:
        title_text = title.text
        title_text = "".join(line.strip() for line in title_text.split("\n"))
    except:
        print("article title not found")
        pass
    print(title_text)

    author = title.find_next('p')
    try:
        author_text = author.text
        author_text = " ".join(line.strip() for line in author_text.split("\n"))
        author_link = author.find('a')['href']
        author_link = "".join(line.strip() for line in author_link.split("\n"))
    except:
        print("article title not found")
        pass
    # print(author_text)
    
    contents = author.find_next_siblings('p')
    contents_strs = []
    for content in contents:
        try:
            content_str = str(content)
            content_str = content_str.replace('<a', ' <a')
            content_str = content_str.replace('a>', 'a> ')
            content_str = "".join(line for line in content_str.split("\n"))
            contents_strs.append(content_str)
        except:
            pass
    contents_strs = ''.join(contents_strs)
    # print(contents_strs)

    side_soup = link_soup.find('aside')

    news_data = {}
    news_data['date'] = date_text
    news_data['title'] = title_text
    news_data['author'] = {
        'author_text': author_text,
        'author_link': author_link
    }
    news_data['text'] = contents_strs 
    news_data['widgets'] = []

    if side_soup.find_all('div', class_='infokasten'):
        if side_soup.find('h1'):
            news_data['widgets'].append({'type': 'headline', 'content': str(side_soup.find('h1').text)})

        infokastens = side_soup.find_all('div', class_='infokasten')
        for infokasten in infokastens:
            try:
                kasten_widget = {}
                image = infokasten.find('img')['src']
                image_str = str(image)
                # print(image_str)
                kasten_widget['type'] = "text + image"
                kasten_widget['image'] = image_str
                kasten_contents = infokasten.find_all(['h2', 'h3', 'p']) # add h1 if LINKS ZUM ARTIKEL title is wanted         
                for kasten_content in kasten_contents:
                    try:
                        kasten_str = str(kasten_content).replace('\n', '')
                        kasten_str = kasten_str.replace('<a', ' <a')
                        kasten_str = kasten_str.replace('a>', 'a> ')
                        kasten_str = kasten_str.replace('a> .', 'a>.')
                        kasten_str = "".join(line.strip() for line in kasten_str.split("\n"))
                        kasten_widget['text'] = kasten_str
                        # print(kasten_str)
                    except:
                        pass
                news_data['widgets'].append(kasten_widget)
                filename = image_str.split('/')[-1]
                if image_str.startswith('/'):
                    image_url = 'https://strafrecht-online.org' + image_str
                    # print(image_url)
                    r = requests.get(image_url)
                    with open(os.path.join(dir_path, filename), 'wb') as f:
                        f.write(r.content)
                elif image_str.startswith('http'):
                    image_url = image_str
                    r = requests.get(image_url)
                    with open(os.path.join(dir_path, filename), 'wb') as f:
                        f.write(r.content)
                else:
                    image_url = article_link + image_str
                    r = requests.get(image_url)
                    with open(os.path.join(dir_path, filename), 'wb') as f:
                        f.write(r.content)
            except:
                pass
        try:
            # if enters here: it has content after kastens    
            if kasten_content.find_all_next(['h2', 'h3', 'p']):
                side_contents = kasten_content.find_all_next(['h2', 'h3', 'p']) # add h1 if LINKS ZUM ARTIKEL title is wanted
                side_strs = []
                side_widget = {}
                side_widget['type'] = "only text"
                for side_content in side_contents:
                    try:
                        side_str = str(side_content)
                        side_str = side_str.replace('<a', ' <a')
                        side_str = side_str.replace('a>', 'a> ')
                        side_str = side_str.replace('a> .', 'a>.')
                        side_str = "".join(line.strip() for line in side_str.split("\n"))
                        side_strs.append(side_str)
                    except:
                        pass
                        # side_str = None
                side_strs = ''.join(side_strs)
                side_widget['text'] = side_strs
                news_data['widgets'].append(side_widget)
            else:
                pass                
        except: 
            pass           
    # if enters here: no image only text kasten
    elif side_soup.find_all(['h2', 'h3', 'p']):
        side_contents = side_soup.find_all(['h2', 'h3', 'p'])
        side_strs = []
        side_widget = {}
        side_widget['type'] = "only text"
        for side_content in side_contents:
            try:
                side_str = str(side_content)
                side_str = side_str.replace('<a', ' <a')
                side_str = side_str.replace('a>', 'a> ')
                side_str = side_str.replace('a> .', 'a>.')
                side_str = "".join(line.strip() for line in side_str.split("\n"))
                side_strs.append(side_str)
            except:
                pass
        side_strs = ''.join(side_strs)
        side_widget['text'] = side_strs
        news_data['widgets'].append(side_widget)
    else:
        # if enters here: no content on sidebar (empty)
        print('article has not side content')
        pass

    return news_data

def scrape():
    source = requests.get('https://strafrecht-online.org/archiv/news/').text
    soup = BeautifulSoup(source, 'lxml')
    news_items = soup.find_all('ul', class_='linkliste')

    articles = {}
    key_id = 1
    break_val = 0
    for news_item in news_items:
        news_links = news_item.find_all('a', href=True)
        for link in news_links:
            href = link['href']
            endpoint = href[2:]
            final_link = 'https://strafrecht-online.org/archiv' + endpoint
            try:
                link_source = requests.get(final_link).text
            except:
                print('Unexpected error: Trying again...')
                time.sleep(50/1000)
                try:
                    link_source = requests.get(final_link).text
                    print('Unexpected error: Trying again...')
                except:
                    print('Scrape failed!')
                    pass
            current_article = get_article(link_source, final_link)
            articles[key_id] = current_article
            key_id += 1

    print('DONE!')

    writeToJSONFile('./', 'newsscrape', articles)

#scrape()