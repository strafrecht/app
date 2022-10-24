import html2text
import json
import logging
import os
from io import BytesIO
import requests
import wget
import uuid
import itertools

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from tqdm import tqdm
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from collections import deque
from time import sleep
from itertools import chain
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
from wagtail.core.models import Page

from wiki.models import Article, ArticleRevision, URLPath
from wiki.plugins.notifications.models import ArticleSubscription

from .models import Question, QuestionVersion, AnswerVersion, Quiz, UserAnswer, Choice
from pages.models.exams import Exams
from pages.models.news import ArticlesPage, ArticlePage
from pages.models.sessions import SessionsPage, SessionPage
from pages.models.events import EventsPage, EventPage

from rest_framework import viewsets, permissions, mixins, generics, response
from .serializers import QuestionSerializer, ChoiceSerializer, UserAnswerSerializer, QuizSerializer, AnswerSerializer, \
    QuestionVersionSerializer, QuestionOnlySerializer
from .scrape.news import get_json as get_news_json
from .scrape.abstimmungen import get_json as get_abstimmungen_json
from .scrape.lehre import get_json as get_lehre_json
from .scrape.events import get_json as get_events_json

logger = logging.getLogger('django')
from wagtail.core.blocks import StreamValue
from wagtail.core.rich_text import RichText
from wagtail.contrib.redirects.models import Redirect
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtail.core.models import Collection, CollectionManager

# image upload
import willow
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from willow.plugins.pillow import PillowImage
import PIL

# redirects
import re

def start(request):
    if not request.user.is_superuser:
        raise "only for superusers"

    # OK
    # scrape_redirects(request)
    # scrape_wiki(request)

    # NOK
    #scrape_news(request)
    #scrape_abstimmungen(request)
    #scrape_events(request)
    #scrape_newsletter(request)
    #scrape_lehre(request)
    #scrape_exams(request)
    #seed_redirects(request)
    print("OK")
    return HttpResponse(200)

def scrape_wiki(request):
    # init
    path = os.path.dirname(os.path.abspath(__file__))
    print(path)
    os.chdir(path)
    # os.chdir('/home/dev/Workspace/app/core')
    #os.chdir('C://Users//sfvso//Documents//serg1o//straf//app//core')

    # delete all wiki/categories
    ArticleSubscription.objects.all().delete()
    URLPath.objects.all().delete()
    ArticleRevision.objects.all().delete()
    Article.objects.all().delete()

    Quiz.objects.all().delete()
    AnswerVersion.objects.all().delete()
    QuestionVersion.objects.all().delete()
    Question.objects.all().delete()

    # Create root article
    root_url = URLPath.create_root(title="StGB")
    root_url.save()

    # prepare module
    base_dir = 'scrape/problemfelder'
    wiki_root_dir = 'stgb'
    # get = lambda node_id: Category.objects.get(pk=node_id)
    # root_node = Category.add_root(name="StGB", slug="stgb")

    # preprocess total file count
    # Preprocess the total files count
    filecounter = 0
    for filepath in os.walk(base_dir):
        filecounter += 1

    # run main code
    #for root, dirs, files in os.walk(base_dir, topdown=True, onerror=on_error):
    for root, dirs, files in tqdm(os.walk(base_dir, topdown=True, onerror=on_error), total=filecounter, unit=" files"):

        for file in files:
            print(file)
            if file == 'Neu anzulegende Problemfelder.pdf':
                continue
            # skip files containing tilde -> git merge lefovers
            if "~" in file:
                continue

            path = os.path.join(root, file)
            html = open(path).read()
            soup = BeautifulSoup(html, "html.parser")

            print(path)
            print(get_type(soup))

            parent_dir = wiki_root_dir + "/" + "/".join(root.split("/")[2:])

            # create categories
            if "category" in get_type(soup):
                cat = {
                    "root": parent_dir,
                    "slug": root.split("/")[-1][0:50],
                    "name": soup.article.h1.text.strip(),
                    #"long_name": extract("long_name", soup),
                }

                create_category(cat)

            # create wikis
            if "problem" in get_type(soup):
                wiki = {
                    "root": parent_dir,
                    "slug": root.split("/")[-1][0:50],
                    "name": soup.article.h1.text.strip() if soup.article.h1 else '?',
                    #"long_name": extract("long_name", soup),
                    "tags": extract("tags", soup),
                    "content": extract("content", soup),
                }
                create_wiki(wiki)

            # create mct
            if "frage" in get_type(soup):
                question = {
                    "root": parent_dir,
                    "slug": root.split("/")[-1][0:50],
                    "category": "", #Category
                    #"title": extract("question", soup),
                    "answers": extract("answers", soup),
                    #"description": extract("description", soup),
                    "order": extract("order", soup),
                }

                question = create_question(question)

                question_version = {
                    "question_id": question.id,
                    "title": extract("question", soup),
                    "answers": extract("answers", soup),
                    "description": extract("description", soup),
                }

                create_question_version(question_version)

    # output
    #categories = Category.objects.all()
    return render(request, "core/categories.html", {
        "categories": [],
        "wikis": [],
        "questions": [],
    })


def scrape_redirects(request):
    # Clean
    Redirect.objects.all().delete()
    root_collection = Collection.get_first_root_node()
    redirects = root_collection.get_children().get(name='Redirects')

    rootdir = './core/scrape/@redirects'
    print(os.getcwd())
    csv = ""

    # Target Directory
    path = os.path.dirname(os.path.abspath(__file__))
    target_dir = path + "/../media/documents"

    # Make the directory
    os.makedirs(target_dir, exist_ok=True)

    for root, subdirs, files in os.walk(rootdir):
        for subdir in subdirs:
            for filename in os.listdir(os.path.join(root, subdir)):
                file_path = os.path.join(root, subdir, filename)

                with open(file_path, 'rb') as f:
                    if "newsletter-urls.txt" in file_path:
                        continue

                    html = f.read()
                    soup = BeautifulSoup(html, features="lxml")
                    print(file_path)
                    print(soup.find('a'))
                    link = soup.find('a').attrs['href'] if 'http' in soup.find('a').attrs['href'] else "https://strafrecht-online.org{}".format(soup.find('a').attrs['href'])
                    print(link)
                    redirect_name = file_path.split('/')[-1].replace('.html', '')

                    if "strafrecht-online.org/" in link or "://" not in link:
                        ext = link.split(".")[-1]
                        print(ext)
                        if ext in ("pdf", "jpeg", "jpg", "JPG", "PNG", "gif", "doc"):
                            local_file = requests.get(link, allow_redirects=True)  # target_dir)
                            print(local_file)
                            file_name = redirect_name + "." + ext
                            open(os.path.join(target_dir, file_name), 'wb').write(local_file.content)
                            link = settings.SITE_URL + "/media/documents/" + file_name.replace(" ", "%20")
                            Document(
                                title=file_name,
                                file="documents/{}".format(file_name),
                                collection=redirects,
                                tags=['redirects']
                            ).save()

                    csv += '"{}","{}"\n'.format(redirect_name, link)

                    #res = requests.get(link)
                    #if res.is_redirect:
                    #    print("Redirect: {}".format(link))

    path = os.path.dirname(os.path.abspath(__file__))
    fo = open(path + '/scrape/redirects.csv', 'w')
    fo.write(csv)
    fo.close()
    print("Import redirects with: ./manage.py import_redirects --src core/scrape/redirects.csv")

def seed_redirects(request):
    redirects = Redirect.objects.all()
    path = os.path.dirname(os.path.abspath(__file__))
    to_review_file = open(path + '/scrape/review_redirects.txt', 'a')

    for redirect in redirects:
        if "strafrecht-online.org" in redirect.link:
            if ".pdf" in redirect.link:
                # upload pdf
                pdf = upload_redirect_pdf(redirect.link)
                print(pdf)

                if pdf:
                    redirect.redirect_link = pdf.url
                    redirect.save()
            else:
                # log to file
                to_review_file.write("title: {}, link: {}\n".format(redirect.title, redirect.link))
        else:
            # do nothing
            print('')

    to_review_file.close()

def scrape_events(request):
    data = get_events_json()
    root = Collection.get_first_root_node()
    # delete event documents
    root.get_children().get(name='Events').get_children().delete()
    parent_page = EventsPage.objects.first()
    # delete all EventPage's
    EventPage.objects.all().delete()

    for event in data:
        # Variables
        title = event['title']
        date = event['date']
        semester = extract_event_semester(event['semester'])
        speaker_description = event['speaker']
        description = event['description']
        poster_pdf = upload_poster_pdf(event['poster_pdf_link']) if event['poster_pdf_link'] != '' else None
        poster_image = upload_poster_image(event['poster_image_link']) if event['poster_image_link'] != '' else None
        youtube_link = event['youtube_link']

        #collection = get_collection
        print("NEWSLETTER: {}".format(event['newsletter_link']))
        newsletter = upload_newsletter_pdf(event['newsletter_link']) if event['newsletter_link'] != '' else None

        event_page = EventPage(
            title=title,
            date=date,
            semester=semester,
            description=description,
            speaker_description=speaker_description,
            poster_pdf=poster_pdf,
            poster_image=poster_image,
            youtube_link=youtube_link,
            newsletter=newsletter
        )

        # Add ArticlePage to parent
        parent_page.add_child(instance=event_page)

        # Save ArticlePage
        event_page.save()

def extract_event_semester(semester):
    return semester.replace('Wintersemester', 'ws').replace('Sommersemester', 'sos').replace(' ', '-').split('/')[0]

def upload_poster_pdf(url):
    root_collection = Collection.get_first_root_node()

    semester = url.split('tacheles/')[1].split('/')[0]
    slug = url.split('tacheles/')[1].split('/')[1]
    filename = url.split('tacheles/')[1].split('/')[2]

    # Target Directory
    path = os.path.dirname(os.path.abspath(__file__))
    target_dir = path + "/../media/documents"
    new_filename = "Event_{semester}_{slug}_{filename}".format(
        semester=semester,
        slug=slug,
        filename=filename
    )

    try:
        local_file = requests.get(url, allow_redirects=True)  # target_dir)
        open(os.path.join(target_dir, new_filename), 'wb').write(local_file.content)

        root = Collection.get_first_root_node()
        events = root.get_children().get(name='Events')

        try:
            semester_col = events.get_children().get(name=semester)
        except:
            semester_col = events.add_child(name=semester)

        try:
            slug_col = semester_col.get_children().get(name=slug)
        except:
            slug_col = semester_col.add_child(name=slug)

        document = Document(
            title=filename,
            file="documents/{}".format(new_filename),
            collection=slug_col,
            tags=['testing']
        )

        document.save()

        return document
    except Exception as e:
        print(" ERROR - {}".format(e))
        print(" URL - {}".format(url))

def upload_poster_image(url):
    image_id = upload_image(url)

    root_collection = Collection.get_first_root_node()

    semester = url.split('tacheles/')[1].split('/')[0]
    slug = url.split('tacheles/')[1].split('/')[1]
    filename = url.split('tacheles/')[1].split('/')[2]

    root = Collection.get_first_root_node()
    events = root.get_children().get(name='Events')

    try:
        semester_col = events.get_children().get(name=semester)
    except:
        semester_col = events.add_child(name=semester)

    try:
        slug_col = semester_col.get_children().get(name=slug)
    except:
        slug_col = semester_col.add_child(name=slug)

    try:
        image = upload_poster_image_file(url, slug_col)
        return image
    except Exception as e:
        return None

def upload_poster_image_file(path, collection):
    filename = path.split('/')[-1]

    if 'strafrecht-online' in path:
        image_url = path
    else:
        image_url = "https://strafrecht-online.org/{path}".format(path=path)

    # download
    try:
        local_file = wget.download(image_url, "/tmp/images")

        image_bytes = open(local_file, "rb").read()
        image_file = ImageFile(BytesIO(image_bytes), name=filename)

        pillow_image = PIL.Image.open(local_file)
        image = PillowImage(pillow_image)
        #image = willow.Image.open(local_file)
        width, height = image.get_size()

        image_object = Image(title=filename, file=image_file, collection=collection, width=width, height=height)
        image_object.save()

        return image_object
    except Exception as error:
        print("ERROR: {}".format(error))
        return None

def upload_newsletter_pdf(url):
    print("URL: {}".format(url))
    root_collection = Collection.get_first_root_node()

    try:
        semester = url.split('newsletter/')[1].split('/')[0]
        filename = url.split('newsletter/')[1].split('/')[1]

        # Target Directory
        path = os.path.dirname(os.path.abspath(__file__))
        target_dir = path + "/../media/documents"
        new_filename = "Event_Newsletter_{semester}_{filename}".format(
            semester=semester,
            filename=filename
        )
    except Exception as e:
        return None

    try:
        local_file = requests.get(url, allow_redirects=True)  # target_dir)
        open(os.path.join(target_dir, new_filename), 'wb').write(local_file.content)

        root = Collection.get_first_root_node()
        events = root.get_children().get(name='Events')

        try:
            semester_col = events.get_children().get(name=semester)
        except:
            semester_col = events.add_child(name=semester)

        try:
            slug_col = semester_col.get_children().get(name=slug)
        except:
            slug_col = semester_col.add_child(name=slug)

        document = Document(
            title=filename,
            file="documents/{}".format(new_filename),
            collection=slug_col,
            tags=['testing']
        )

        document.save()

        return document
    except Exception as e:
        print(" ERROR - {}".format(e))
        print(" URL - {}".format(url))

def scrape_lehre(request):
    # delete articles + images
    SessionPage.objects.all().delete()
    data = get_lehre_json()
    new_data = data["1"]

    #data = dict(itertools.islice(data.items(), 60))

    for session in data.values():
        # SessionsPage
        parent_page = SessionsPage.objects.first()

        # Variables
        title = extract_title(session.get("lehre", None))

        if session.get("lehre_link"):
            slug = session.get("lehre_link").strip("/").split("/")[-1]
        else:
            slug = ""
        if session.get("semester"):
            semester = extract_semester(session.get("semester", "<p>-</p>"))
        else:
            semester = "-"
        # Information
        try:
            speaker_description = extract_session(session["informationen"])['speakers']
        except:
            speaker_description = "-"
        try:
            date = extract_session(session["informationen"])['date']
        except:
            date = "-"
        try:
            location = extract_session(session["informationen"])['location']
        except:
            location = "-"
        try:
            assessment = extract_session(session["informationen"])['assessment']
        except:
            assessment = ''

        if session.get("materialien", None):
            pdfs = extract_pdfs(
                session["lehre_link"],
                session.get("materialien")
            )
            for p in pdfs:
                for f in p["documents"]:
                    continue
                    #print(f["href"])
        else:
            pdfs = []

        #date = datetime.strptime(session['date'], '%d.%m.%Y').date()

        if title:
            # Create ArticlePage
            session_page = SessionPage(
                #slug=slug, // not compatible with RoutablePageMixin
                name=title,
                subtitle='empty',
                title=title,
                semester=semester,
                speaker_description=speaker_description,
                date=date,
                location=location,
                assessment=assessment,
            )

            # Blocks
            # for widget in article['widgets']:
            #     // check widget type and create an appropriate python dict to represent that
            #     // append to the final array

            # Widgets array
            widgets = []

            for widget in session['widgets']:
                print("LENGTH: {}".format(len(session['widgets'])))
                print(widget)
                # sidebar simple
                if widget['type'] == 'headline':
                    image_id = upload_image(widget['image'])
                    if image_id:
                        widgets.append(('sidebar_header', {
                            'image': Image.objects.get(id=image_id),
                            'title': widget['headline'],
                            'content': RichText("<p>{}</p>".format(widget['content'])),
                        }))
                    else:
                        widgets.append(('sidebar_header', {
                            'image': Image.objects.filter(title='klammer.jpg').first(),
                            'title': widget['headline'],
                            'content': RichText("<p>{}</p>".format(widget['content'])),
                        }))
                if widget['type'] == 'title':
                    widgets.append(('sidebar_title', {'content': RichText(widget['content'])}))
                if widget['type'] == 'sidebar_border':
                    widgets.append(('sidebar_border', {'content': RichText(widget['content'])}))
                if widget['type'] == 'only text':
                    widgets.append(('sidebar_border', {'content': RichText(widget['content'])}))
                # sidebar image text
                if widget['type'] == 'text + image':
                    # check if image exists
                    image_id = upload_image(widget['image'])
                    if image_id:
                        widgets.append(('sidebar_image_text',
                                        {'image': Image.objects.get(id=image_id), 'content': RichText(widget['content'])}))
                    else:
                        print("FAILED: {}".format(title))

            # Sidebar
            print("DOWN:")
            print(widgets)
            session_page.sidebar = widgets

            # Upload pdfs
            #print("SEMESTER: {}".format(semester))
            #print("SLUG: {}".format(slug))

            # RESTORE
            updated_pdfs = upload_pdfs(semester, slug, pdfs)
            # save content
            session_page.material = build_material_html(updated_pdfs)

            # Add ArticlePage to parent
            parent_page.add_child(instance=session_page)

            # Save ArticlePage
            session_page.save()

def build_material_html(pdfs):
    html = ""

    for group in pdfs:
        html += "<h3>{}</h3>\n".format(group['name'])

        for pdf in group['documents']:
            uuid = pdf['uuid'] if 'uuid' in pdf.keys() else 'ERROR-{}'.format(pdf['name'])
            html += "<a href='{}'>{}</a>\n".format(pdf['local'], pdf['name'])
        html += "\n"
    return html

def upload_redirect_pdf(link):
    root_collection = Collection.get_first_root_node()
    redirects = root_collection.get_children().get(name='Redirects')

    print("DOWNLOADING: {}".format(link))
    title = link.split('/')[-1].split('.')[0]
    filename = link.split('/')[-1].split('.')[0][0:85] + '.pdf'

    # Target Directory
    path = os.path.dirname(os.path.abspath(__file__))
    target_dir = path + "/../media/documents"

    # Make the directory
    os.makedirs(target_dir, exist_ok=True)

    try:
        local_file = requests.get(link, allow_redirects=True)  # target_dir)
        open(os.path.join(target_dir, filename), 'wb').write(local_file.content)
        document = Document(
            title=title,
            file="documents/{}".format(filename),
            collection=redirects,
            tags=['testing']
        )
        document.save()
        return document
    except Exception as e:
        print(" ERROR - {}".format(e))
        return False


def upload_pdfs(semester, slug, pdfs):
    root_collection = Collection.get_first_root_node()
    semester = semester.replace('sos', 'ss')

    for group in pdfs:
        for pdf in group['documents']:
            #print("PDF: {}".format(pdf))
            filename = pdf['href'].split('/')[-1].split('.')[0]

            # Target Directory
            path = os.path.dirname(os.path.abspath(__file__))
            target_dir = path + "/../media/documents"

            #new_filename_root = "lehre_{semester}_{slug}_{filename}".format(
            #    semester=semester,
            #    slug=slug,
            #    filename=pdf['name']
            #)

            if len(filename) <= 78:
                new_filename = "{semester}_{filename}.pdf".format(
                    semester=semester,
                    filename=filename
                )
            else:
                new_filename = "{semester}_{filename}_.pdf".format(
                    semester=semester,
                    filename=filename[0:77],
                )

            print("{}: {}".format(len(new_filename) + 10, new_filename))
            pdf['local'] = new_filename

            #if 'uuid' in pdf.keys():
            #    new_filename = "{uuid}.pdf".format(uuid=pdf['uuid'])
            #else:
            #    new_filename = "ERROR: {}.pdf".format(pdf['name'])

            # Make the directory
            os.makedirs(target_dir, exist_ok=True)

            try:
                href = pdf['href'] if '://' in pdf['href'] else 'http://strafrecht-online.org/{}'.format(pdf['href'])
                local_file = requests.get(href, allow_redirects=True) #target_dir)
                open(os.path.join(target_dir, new_filename), 'wb').write(local_file.content)

                root = Collection.get_first_root_node()
                lehre = root.get_children().get(name='Lehre')

                try:
                    semester_col = lehre.get_children().get(name=semester)
                except:
                    semester_col = lehre.add_child(name=semester)

                try:
                    slug_col = semester_col.get_children().get(name=slug)
                except:
                    slug_col = semester_col.add_child(name=slug)

                Document(
                    title=pdf['name'],
                    file="documents/{}".format(new_filename),
                    collection=slug_col,
                    tags=['testing']
                ).save()
            except Exception as e:
                print(len(pdf['name']))
                print(len("documents/{}".format(new_filename)))
                print("ERROR - {}". format(e))
                print("URL - {}".format(pdf['href']))
                print("\n\n")

    return pdfs
    #return "<h1>Testing!</h1>"

def extract_session_url(semester, slug):
    if 'ws' in semester:
        semester_param = semester.replace('ws', 'ws-')
    if 'ss' in semester:
        semester_param = semester.replace('ss', 'sos-')

    url = "https://strafrecht-online.org/lehre/{semester_param}/{slug}".format(
        semester_param=semester_param,
        slug=slug
    )

    return url


def extract_title(content):
    if content:
        html = BeautifulSoup(content, features="html.parser")
        try:
            title = html.text
            return title
        except:
            print("ERROR")
    else:
        return None

def extract_pdfs(href, content):
    soup = BeautifulSoup(content, features="html.parser")
    data = []

    # temp
    current = ""
    documents = []

    for element in soup.children:
        if element.name == "h3":
            current = element.text
        if element.name == "p":
            if element.a:
                data.append({'name': current, 'documents': [{'name': element.a.text, 'href': element.a['href']}]})

                current = ""
                documents = []

        if element.name == "ul":
            for li in element.find_all('li', recursive=False):
                if li.a:
                    pdf_url = os.path.join(href, li.a['href'])
                    documents.append({
                        'name': li.a.text,
                        'href': pdf_url,
                        'uuid': str(uuid.uuid4())
                    })
            data.append({'name': current, 'documents': documents})

            current = ""
            documents = []

    return data

def extract_semester(content):
    html = BeautifulSoup(content, features="html.parser")
    try:
        semester_string = html.find('p').text
        [semester_part, year_part] = semester_string.split(' ')[0:2]

        if semester_part == 'Wintersemester' or semester_part == 'Winter':
            semester_prefix = 'ws'
        if semester_part == 'Sommersemester':
            semester_prefix = 'ss'

        year_suffix = year_part.split('/')[0]

        semester = "{semester_prefix}{year_suffix}".format(
            semester_prefix=semester_prefix,
            year_suffix=year_suffix
        )
        semester = semester.replace("-", "").replace("ws", "ws-").replace("ss", "ss-")
        return semester
    except:
        return "-"

# Information
def extract_session(content):
    html = BeautifulSoup(content, features="html.parser")
    left = html.find(class_="infokasten").find_all(recursive=False)[0]
    right = html.find(class_="infokasten").find_all(recursive=False)[1]

    current = ''
    result = {'speakers': [], 'date': [], 'location': [], 'assessment': []}

    # Left
    for e in left.find_all(recursive=False):
        if e.name == 'h3':
            if 'Doze' in e.text:
                current = 'speakers'
            if 'Termin' in e.text:
                current = 'date'
            if 'Ort' in e.text:
                current = 'location'
        else:
            if current and e.decode_contents() != '':
                s = e.decode_contents().replace('<li>', '<p>').replace('</li>', '</p>')
                result[current].append(s)

    result['speakers'] = "<br/>".join(result['speakers'])
    result['date'] = "<br/>".join(result['date'])
    result['location'] = "<br/>".join(result['location'])

    # Right
    result['assessment'] = right.decode_contents()
    #print(result)
    return result

def scrape_newsletter(request):
    path = os.path.dirname(os.path.abspath(__file__))
    root_collection = Collection.get_first_root_node()
    newsletters_col = root_collection.get_children().get(name='Newsletters')
    newsletters_col.get_children().all().delete()

    docs = []

    with open(path + '/scrape/newsletters.json', encoding='utf-8-sig') as f:
        data = json.load(f)

    for newsletter in data:
        try:
            collection = newsletters_col.get_children().get(name=newsletter['year'])
        except:
            collection = newsletters_col.add_child(name=newsletter['year'])

        # Target Directory
        target_dir = path + "/../media/documents"
        new_filename = "{filename}".format(
            year=newsletter['year'],
            filename=newsletter['filename'].split('/')[-1]
        )

        try:
            local_file = requests.get(newsletter['href'], allow_redirects=True)  # target_dir)
            open(os.path.join(target_dir, new_filename), 'wb').write(local_file.content)

            document = Document(
                title=newsletter['filename'],
                file="documents/{}".format(new_filename),
                collection=collection,
                tags=['testing']
            )

            document.save()

            docs.append({
                "document": document,
                "link": document.url,
                "name": document.filename,
                "year": newsletter['year']
            })
        except Exception as e:
            print(" ERROR - {}".format(e))
            print(" URL - {}".format(newsletter['href']))

    docs = sorted(docs, key=lambda x: x['year'])

    s = ""
    current_year = 0

    for doc in docs:
        if doc['year'] != current_year:
            current_year = doc['year']
            s += "<h3>{}</h3>\n".format(doc['year'])
        s += "<a href='{}'>{}</a>\n".format(
            doc['link'],
            doc['name'],
        )

    f = open("./newsletter_links.html", "w")
    f.write(s)
    f.close()

    return

def scrape_news(request):
    # delete articles + images
    ArticlePage.objects.all().delete()
    Image.objects.filter(title='thumb_archiv.jpg').delete()

    data = get_news_json()
    #return data

    for index in data:
        article = data[index]
        # ArticlesPage
        parent_page = ArticlesPage.objects.first()

        users = {
            ' Von Jakob Bach ': 2,
            ' Von Roland Hefendehl ': 3,
            ' Von Marco Rehmet ': 4,
            ' Von Nicolas Emmerich ': 5,
            ' VonTitus Rehm ': 6,
            ' VonJulian Sigmund ': 7,
            ' Von Titus Rehm ': 6,
            ' Von Julian Sigmund ': 7,
            ' Gastbeitrag von Peer Stolle und Martin Heining ': 8,
            ' Von Matthias Noll ': 9,
            ' Von TG ': 10,
            ' Von JP ': 11,
            ' Von Harald Wohlfeil ': 12,
            ' Von Dominik Stahlmecke ': 13,
            ' Von Moritz Feldmann ': 14,
            ' Von LM ': 15,
            ' Von Michael Bunzel ': 16,
            ' Von Rico Maatz ': 17,
            ' Von Karsten Brandt ': 18,
            ' Von Peer Stolle ': 19,
            ' Von René Janovsky ': 20,
            ' Von Beate Hensel ': 21,
            ' Von Martin Rosenthal ': 22,
            ' Von Dr. Johanna Schulenburg ': 23,
            ' Von Nils Ströle ': 24,
        }

        # Variables
        title = article['title']
        user = User.objects.get(id=users[article['author']['author_text']])
        date = datetime.strptime(article['date'], '%d.%m.%Y').date()
        body = article['text']
        is_evaluation = False

        # Create ArticlePage
        article_page = ArticlePage(
            title=title,
            author=user,                                         # models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
            date=date,
            body=body,                                           # RichTextField(blank=True)
            is_evaluation=is_evaluation,                                 # models.BooleanField(default=False)
        )

        # Blocks
        # for wiget in article['widgets']:
        #     // check widget type and create an appropriate python dict to represent that
        #     // append to the final array

        # Widgets array
        widgets = []

        # sidebar title

        for widget in article['widgets']:
            # sidebar simple
            if widget['type'] == 'headline':
                widgets.append(('sidebar_title', {'content': RichText("<p>{}</p>".format(widget['content']))}))
            if widget['type'] == 'text only':
                widgets.append(('sidebar_simple', {'content': RichText(widget['text'])}))
            if widget['type'] == 'only text':
                widgets.append(('sidebar_simple', {'content': RichText(widget['text'])}))
            # sidebar image text
            if widget['type'] == 'text + image':
                # check if image exists
                image_id = upload_image(widget['image'])
                if image_id:
                    widgets.append(('sidebar_image_text', {'image': Image.objects.get(id=image_id), 'content': RichText(widget['text'])}))
                else:
                    print("FAILED: {}".format(article['title']))


        article_page.sidebar = widgets

        # Add ArticlePage to parent
        parent_page.add_child(instance=article_page)

        # Save ArticlePage
        article_page.save()

def scrape_abstimmungen(request):
    # delete articles + images
    #ArticlePage.objects.all().delete()
    #Image.objects.filter(title='thumb_archiv.jpg').delete()

    data = get_abstimmungen_json()
    # return data

    for index in data:
        article = data[index]
        # ArticlesPage
        parent_page = ArticlesPage.objects.first()

        users = {
            ' Von Jakob Bach ': 2,
            ' Von Roland Hefendehl ': 3,
            ' Von Marco Rehmet ': 4,
            ' Von Nicolas Emmerich ': 5,
            ' VonTitus Rehm ': 6,
            ' VonJulian Sigmund ': 7,
            ' Von Titus Rehm ': 6,
            ' Von Julian Sigmund ': 7,
            ' Gastbeitrag von Peer Stolle und Martin Heining ': 8,
            ' Von Matthias Noll ': 9,
            ' Von TG ': 10,
            ' Von JP ': 11,
            ' Von Harald Wohlfeil ': 12,
            ' Von Dominik Stahlmecke ': 13,
            ' Von Moritz Feldmann ': 14,
            ' Von LM ': 15,
            ' Von Michael Bunzel ': 16,
            ' Von Rico Maatz ': 17,
            ' Von Karsten Brandt ': 18,
            ' Von Peer Stolle ': 19,
            ' Von René Janovsky ': 20,
            ' Von Beate Hensel ': 21,
            ' Von Martin Rosenthal ': 22,
            ' Von Dr. Johanna Schulenburg ': 23,
            ' Von Nils Ströle ': 24,
        }

        # Variables
        title = article['title']
        user = User.objects.get(id=users[article['author']['author_text']])
        date = datetime.strptime(article['date'], '%d.%m.%Y').date()
        body = article['text']
        is_evaluation = True

        # Create ArticlePage
        article_page = ArticlePage(
            title=title,
            author=user,  # models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
            date=date,
            body=body,  # RichTextField(blank=True)
            is_evaluation=is_evaluation,  # models.BooleanField(default=False)
        )

        # Blocks
        # for wiget in article['widgets']:
        #     // check widget type and create an appropriate python dict to represent that
        #     // append to the final array

        # Widgets array
        widgets = []

        # sidebar title

        for widget in article['widgets']:
            # sidebar simple
            if widget['type'] == 'headline':
                widgets.append(('sidebar_title', {'content': RichText("<p>{}</p>".format(widget['content']))}))
            if widget['type'] == 'text only':
                widgets.append(('sidebar_simple', {'content': RichText(widget['text'])}))
            if widget['type'] == 'only text':
                widgets.append(('sidebar_simple', {'content': RichText(widget['text'])}))
            # sidebar image text
            if widget['type'] == 'text + image':
                # check if image exists
                image_id = upload_image(widget['image'])
                if image_id:
                    widgets.append(('sidebar_image_text',
                                    {'image': Image.objects.get(id=image_id), 'content': RichText(widget['text'])}))
                else:
                    print("FAILED: {}".format(article['title']))

        article_page.sidebar = widgets

        # Add ArticlePage to parent
        parent_page.add_child(instance=article_page)

        # Save ArticlePage
        article_page.save()

def upload_image(path):
    filename = path.split('/')[-1]

    if 'http' in path:
        image_url = path
    else:
        image_url = os.path.join("https://strafrecht-online.org/", path.lstrip(os.path.sep))

    print(image_url)

    # download if file does not exist
    try:
        if not os.path.isfile("/tmp/images/{}".format(filename)):
            local_file = wget.download(image_url, "/tmp/images")
            print("DOWNLOADING")
            print(local_file)
        else:
            local_file = "/tmp/images/{}".format(filename)

        image_bytes = open(local_file, "rb").read()
        image_file = ImageFile(BytesIO(image_bytes), name=filename)

        pillow_image = PIL.Image.open(local_file)
        image = PillowImage(pillow_image)
        #image = willow.Image.open(local_file)
        width, height = image.get_size()

        if Image.objects.filter(title=filename):
            image_object = Image.objects.filter(title=filename).first()
        else:
            image_object = Image(title=filename, file=image_file, width=width, height=height)

        image_object.save()
        return image_object.id
    except Exception as error:
        print("ERROR: {}".format(error))
        return False

def extract_session_url(semester, slug):
    if 'ws' in semester:
        semester_param = semester.replace('ws', 'ws-')
    if 'ss' in semester:
        semester_param = semester.replace('ss', 'sos-')

def traverse_ancestors(parent, slug_list):
    if len(slug_list) == 0:
        return parent
    else:
        #print("    POS: 2")
        remaining = slug_list
        up = remaining.popleft()
        #print("    UP: {}".format(up))

        try:
            children = parent.get_children()
            child = list(filter(lambda c: c.slug == up, children))

            #print("      CHILDREN: {}".format(child))

            if len(child) == 1:
                #print("        POS: 4")
                return traverse_ancestors(child[0], remaining)
            else:
                raise URLPath.DoesNotExist
        except URLPath.DoesNotExist:
            #print("      POS: 5")
            return parent

        #print("    POS: 6")
        return parent

    #print("  EXIT: traverse_ancestors()")

def create_category(wiki):
    #print("ENTER: create_category()")
    root = Article.objects.first().urlpath_set.first()
    slug_list = deque(wiki["root"].split("/")[1:])
    parent = traverse_ancestors(root, slug_list)

    #print("root: {}".format(root))
    #print("slug_list: {}".format(slug_list))
    #print("parent: {}".format(parent))

    urlpath = URLPath.create_urlpath(
        parent=parent,
        slug=wiki['slug'],
        site=None,
        title=wiki['name'],
        article_kwargs={},
        request=None,
        article_w_permissions=None,
        content="",
    )

    urlpath.save()
    #print("EXIT: create_category()")

def create_wiki(wiki):
    #print("ENTER: create_wiki()")
    root = Article.objects.first().urlpath_set.first()
    slug_list = deque(wiki["root"].split("/")[1:])
    parent = traverse_ancestors(root, slug_list)

    #print("root: {}".format(root))
    #print("slug_list: {}".format(slug_list))
    #print("parent: {}".format(parent))

    urlpath = URLPath.create_urlpath(
        parent=parent,
        slug=wiki['slug'],
        site=None,
        title=wiki['name'],
        article_kwargs={},
        request=None,
        article_w_permissions=None,
        content=wiki['content'],
    )

    #print(wiki['content'])

    urlpath.save()

def create_question(question_data):
    root = Article.objects.first().urlpath_set.first()
    slug_list = deque(question_data["root"].split("/")[1:-2])
    parent = traverse_ancestors(root, slug_list)

    question = Question(
        filepath=question_data['root'],
        slug=question_data['slug'],
        #title=question_data['title'],
        order=question_data['order'],
        #description=question_data['description'],
        category=parent.article,
    )

    # save question
    question.save()

    return question

def create_question_version(question_data):
    answers = question_data['answers']
    print(answers)

    question_version = QuestionVersion(
        question_id=question_data['question_id'],
        title=question_data['title'],
        #title="placeholder title",
        description=question_data['description'],
        #description="placeholder description"
    )

    # save answers
    for answer in answers:
        #question_version.answerversion_set.create(text=answer['text'], correct=answer['correct'])
        question_version.answers.create(text=answer['text'], correct=answer['correct'])

    question_version.save()

def get_type(soup):
    try:
        return extract("type", soup)
    except KeyError:
        return "no type defined"

def extract(field, soup):
    if field == "question":
        header = soup.find(lambda tag: tag.name == "h2")
        title = md(header.decode_contents(formatter="html").replace("\n", ""))
        return title

    if field == "answers":
        header = soup.find(lambda tag: tag.name == "h2")
        answers = [{
                'text': md(answer.decode_contents(formatter="html").replace("\n", "")),
                'correct': 'correct' in answer.attrs.values().__str__()
            } for answer in soup.find("ul").findAll("li")]
        return answers

    if field == "description":
        header = soup.find(lambda tag: tag.name == "ul")
        html = "<br>".join([str(p) for p in header.findNextSiblings("p")])
        markdown = md(html)
        description = markdown
        return description

    # [Wiki]
    if field == "tags":
        header = soup.find(lambda tag: tag.name == "h2" and "Tags" in tag.text)

        try:
            tag_list = header.findNextSibling("p").text.replace("\n", "").replace("§", " §").split(";")
            tag_list = [tag.strip() for tag in tag_list]
        except AttributeError:
            tag_list = []
        return tag_list

    #
    if field == "content":
        header = soup.article.find(lambda tag: tag.name == "h2" and ("Sachverhalt" in tag.text) or ("Problemaufriss" in tag.text) or ("Tags" in tag.text))
        if "siehe hier" in soup.prettify():
            nextNode = soup.article.find("p")
        else:
            nextNode = header
        content = ""

        while True:
            try:
                tag_name = nextNode.name
            except AttributeError:
                tag_name = "none"

            if tag_name in ["h2","p","ol","li","span", "\n", "h5"]:
                # if element has class, remove it
                if 'class' in nextNode.attrs.keys():
                    del nextNode.attrs['class']

                # if child contains class, remove it
                if nextNode.findChild("span"):
                    if 'class' in nextNode.findChild("span").attrs.keys():
                        del nextNode.findChild("span").attrs['class']

                # replace <u> with <b>
                #html = str(nextNode).replace("<u>", " <b>").replace("</u>", "</b> ").replace("<a", " <a").replace("/a>", "/a> ").replace("<span>", "").replace("</span>", "")
                # Fix 2515: remove cr and nl
                html = str(nextNode).replace("<u>", " <b>").replace("</u>", "</b> ").replace("<span>", "").replace("</span>", "").replace("<em>", "<i>").replace("</em>", "</i>").replace("<h5", "<p").replace("</h5>", "</p>").replace("\r", " ").replace("\n", " ")

                if "Fragment" in html: html = html.replace("<!--StartFragment-->", "").replace("<!--EndFragment-->", "")
                if "siehe hier" in soup.prettify():
                    html = html.replace("problemfelder", "wiki")
                markdown = md(html)
                content += markdown
            elif tag_name == "sonline-revision":
                break
            else:
                False

            try:
                nextNode = nextNode.nextSibling
            except AttributeError:
                break

        return content

    if field == "order":
        value = soup.article.attrs["data-order"]

        # if order is datetime value, return order 1000
        try:
            return value
        except:
            return "6666"

    if field == "long_name":
        return soup.article.attrs["data-short-name"]
    if field == "type":
        return soup.article.attrs["data-type"].split("/")[-1]

def on_error(e):
    raise e

def scrape_exams(request):
    import csv
    import dateutil.parser

    Exams.objects.all().delete()

    exams = []
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/exams.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        exam_type = {
            'Klausur im Falltraining': 'falltraining',
            'Examensklausur': 'exam',
            'Originalexamensklausur': 'original-exam',
            'Übungsfall': 'exercise',
            'Übungsklausur': 'exercise',
            'AG-Fall': 'tutorial',
        }
        exam_difficulty = {
            'Anfänger': 'beginner',
            'Fortgeschrittene': 'intermediate',
            'Examen': 'advanced',
        }

        for row in reader:
            if row[0]:
                date_string = "{}-01".format(row[0])
                print(repr(date_string))
                date = dateutil.parser.parse(date_string)
            else:
                date = None

            if row[1]:
                et = exam_type[row[1]]
            else:
                et = ""

            if row[2]:
                ed = exam_difficulty[row[2]]
            else:
                ed = ""

            exam = Exams.objects.create(
                date=date,
                type=et,
                difficulty=ed,
                paragraphs=row[3],
                problems=row[4],
                sachverhalt_link=row[5],
                loesung_link=row[6],
            )

            exams.append(exam)

    for exam in exams: print(exam)

    #result = Exams.objects.bulk_create(exams)
    return
