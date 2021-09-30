from bs4 import *
import requests
import json
import time
import os
from urllib.parse import urlparse
import re

def get_json():
    os.chdir('/home/dev/Workspace/app/core/scrape')
    #f = open('eventsscrape.json', encoding='iso-8859-1')
    #f = open('eventsscrape_fixed.json', encoding='utf-8')
    #f = unicode(str, errors='replace')
    #f = f.decode('latin-1').encode('utf8')
    #data = json.load(f)
    with open('eventsscrape.json', encoding='utf-8-sig') as f:
        data = json.load(f)
    return data

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

def get_lehre(link_source, lehre_link):
    base_dir = os.getcwd()
    dir_name = "lehre_content"
    dir_path = os.path.join(base_dir, dir_name)

    # print(dir_path)

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    link_soup = BeautifulSoup(link_source, 'lxml')

    lehre_data = {}

    lehre_data['link_source'] = link_source
    lehre_data['lehre_link'] = lehre_link

    try:
        straf_title = link_soup.find('h1')
        lesson_title = straf_title.find_next('h1')
        lesson_str = str(lesson_title)
        lesson_str = "".join(line.strip() for line in lesson_str.split("\n"))
        lehre_data['lehre'] = lesson_str
        # print(lesson_str) # return lesson_str if full html element is required
        lesson_text = lesson_title.text
        lesson_text = "".join(line.strip() for line in lesson_text.split("\n"))
        print(lesson_text)
    except:
        print("article title not found")
        pass
    

    try:
        semester = link_soup.find('p', class_='subhead')
        semester_str = str(semester)
        semester_str = "".join(line.strip() for line in semester_str.split("\n"))
        lehre_data['semester'] = semester_str
        # print(semester_str) # return semester_str if full html element is required
        semester_text = semester.text
        semester_text = "".join(line.strip() for line in semester_text.split("\n"))
        # print(semester_text)
    except:
        print("article title not found")
        pass


    try:
        seminar = semester.find_next('h2')
        seminar_title = seminar.text
        seminar_title = "".join(line.strip() for line in seminar_title.split("\n"))
        seminar_content = []
        if seminar_title.startswith('Seminarank'): 
            seminar_str = str(seminar)
            seminar_str = "".join(line.strip() for line in seminar_str.split("\n"))
            seminar_content.append(seminar_str)
            seminar_info = seminar.find_next_siblings('p')
            for p in seminar_info:
                p_str = str(p)
                p_str = "".join(line.strip() for line in p_str.split("\n"))
                seminar_content.append(p_str)
            seminar_content = ''.join(seminar_content)
            lehre_data['seminar'] = seminar_content
            # print(seminar_content)
        else:
            print("no seminar")
            pass
    except:
        print("no seminar section")
        pass


    info_content = []
    try:
        info = link_soup.find('div', class_='infokasten spalt2')
        info_title = info.find_previous_sibling('h2')
        info_title = str(info_title)
        info_title = "".join(line.strip() for line in info_title.split("\n"))
        info_content.append(info_title)
        info_str = str(info)
        info_str = "".join(line.strip() for line in info_str.split("\n"))
        info_content.append(info_str)
        info_content = ''.join(info_content)
        lehre_data['informationen'] = info_content
        # print(info_content)
    except:
        print("no info found")
        pass

    # GET PDFs IN INFO

    """
    links = info.find_all('a')
    for link in links:
        try: 
            if '.pdf' in link['href']:
                href = link['href']
                pdf_link = 'https://strafrecht-online.org/lehre' + root_path + href
                filename = href.split('/')[-1]
                # filename = link.text.replace(' ', '_')
                pdf_response = requests.get(pdf_link)
                if pdf_response.status_code == 200:
                    with open(os.path.join(dir_path, filename), 'wb') as f:
                        f.write(pdf_response.content)
                        f.close()
                else:
                    print("pdf does not exist")
            else:
                print('pdf not found')
        except:
            pass
    """

    
    try:
        separator = info.find_next('hr')
        materials = separator.find_next_siblings()
        material_strs = []
        for material in materials:
            try:
                material_str = str(material)
                material_str = "".join(line.strip() for line in material_str.split("\n"))
                material_strs.append(material_str)
            except:
                pass
        material_strs = ''.join(material_strs)
        lehre_data['materialien'] = material_strs 
        # print(material_strs)
    except:
        print("materialien not found")
        pass

    parse = urlparse(lehre_link)
    root_path = str(parse.path)
    root_path = re.sub('lehre/', '', root_path)
    # print(root_path)

    # GET PDFs IN MATERIALIEN
    """
    try:
        for link_list in materials:
            links = link_list.find_all('a')
            for link in links:
                try: 
                    if '.pdf' in link['href']:
                        href = link['href']
                        pdf_link = 'https://strafrecht-online.org/lehre' + root_path + href
                        filename = href.split('/')[-1]
                        # filename = link.text.replace(' ', '_')
                        pdf_response = requests.get(pdf_link)
                        if pdf_response.status_code == 200:
                            with open(os.path.join(dir_path, filename), 'wb') as f:
                                f.write(pdf_response.content)
                                f.close()
                        else:
                            print("pdf does not exist")
                    else:
                        print('pdf not found')
                except:
                    pass
    except:
        print("no links found in materialien")
    """


    side_soup = link_soup.find('aside')

    # GET PDFs IN SIDEBAR
    """
    try:
        links = side_soup.find_all('a')
        for link in links:
            try: 
                if '.pdf' in link['href']:
                    href = link['href']
                    pdf_link = 'https://strafrecht-online.org/lehre' + root_path + href
                    filename = href.split('/')[-1]
                    # filename = link.text.replace(' ', '_')
                    pdf_response = requests.get(pdf_link)
                    if pdf_response.status_code == 200:
                        with open(os.path.join(dir_path, filename), 'wb') as f:
                            f.write(pdf_response.content)
                            f.close()
                    else:
                        print("pdf does not exist")
                else:
                    print('pdf not found')
            except:
                pass
    except:
        pass
    """


    lehre_data['widgets'] = []


    try:
        if side_soup.find_all('div', class_='infokasten'):
            infokastens = side_soup.find_all('div', class_='infokasten')
            for infokasten in infokastens:
                kasten_widget = {}
                try:
                    if infokasten.find('img')['src']: 
                        image = infokasten.find('img')['src']
                        image_str = str(image)
                        kasten_widget['type'] = "text + image"
                        kasten_widget['image'] = image_str
                        """
                        try:
                            filename = image_str.split('/')[-1]
                            # print(filename)
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
                                image_url = lehre_link + image_str
                                r = requests.get(image_url)
                                with open(os.path.join(dir_path, filename), 'wb') as f:
                                    f.write(r.content)
                        except:
                            pass
                        """
                    else:
                        pass
                except:
                    kasten_widget['type'] = "only text"
                    pass
                infokasten_str = str(infokasten)
                infokasten_str = "".join(line.strip() for line in infokasten_str.split("\n"))
                kasten_widget['text'] = infokasten_str
                lehre_data['widgets'].append(kasten_widget)
            # try:
            #     # if enters here: it has content after kastens    
            #     if infokasten.find_all_next(['h2', 'h3', 'p']):
            #         side_contents = infokasten.find_all_next(['h2', 'h3', 'p']) # add h1 if LINKS ZUM ARTIKEL title is wanted
            #         side_strs = []
            #         side_widget = {}
            #         side_widget['type'] = "only text"
            #         for side_content in side_contents:
            #             try:
            #                 side_str = str(side_content)
            #                 side_str = "".join(line.strip() for line in side_str.split("\n"))
            #                 side_strs.append(side_str)
            #             except:
            #                 pass
            #                 # side_str = None
            #         side_strs = ''.join(side_strs)
            #         side_widget['text'] = side_strs
            #         lehre_data['widgets'].append(side_widget)
            #         # print(side_strs) # side_strs contain the side bar content
            #     else:
            #         pass 
            # except: 
            #     pass   
        # if enters here: no image only text kasten
        elif side_soup.find_all(['h2', 'h3', 'p']):
            side_contents = side_soup.find_all(['h2', 'h3', 'p'])
            side_strs = []
            side_widget = {}
            side_widget['type'] = "only text"
            for side_content in side_contents:
                try:
                    side_str = str(side_content)
                    side_str = "".join(line.strip() for line in side_str.split("\n"))
                    side_strs.append(side_str)
                except:
                    pass
                    # side_str = None
            side_strs = ''.join(side_strs)
            side_widget['text'] = side_strs
            lehre_data['widgets'].append(side_widget)
            # print(side_strs) # side_strs contain the side bar content
        else:
            # if enters here: no content on sidebar (empty)
            print('no sidebar')
            pass
    except:
        pass

    return lehre_data


# ////////////////////////////////////////////////////////////

def scrape():
    source = requests.get('https://strafrecht-online.org/lehre/vorherige-semester/').text
    soup = BeautifulSoup(source, 'lxml')
    lehre_items = soup.find_all('ul', class_='linkliste')

    lessons = {}
    key_id = 1
    break_val = 0
    for lehre_item in lehre_items:
        lehre_links = lehre_item.find_all('a', href=True)
        for link in lehre_links:
            href = link['href']
            endpoint = href[2:]
            final_link = 'https://strafrecht-online.org/lehre' + endpoint
            try:
                link_source = requests.get(final_link).text
            except:
                print('link_source ERROR- cant run requests.get(final_link), info:')
                print('TRY AGAIN')
                time.sleep(50 / 1000)
                try:
                    link_source = requests.get(final_link).text
                    print('SECOND TRY: Success')
                except:
                    print('SECOND TRY: Fail')
                    pass
            current_lehre = get_lehre(link_source, final_link)
            lessons[key_id] = current_lehre
            key_id += 1

        # break

        #     if key_id == 2:
        #         print('BREAK!')
        #         break_val = 1
        #         break
        # if break_val == 1:
        #     break

    # print(lessons)
    print('DONE!')

    writeToJSONFile('./', 'lehrescrape', lessons)