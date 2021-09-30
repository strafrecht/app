import os
import requests
from bs4 import BeautifulSoup

rootdir = '.'

for root, subdirs, files in os.walk(rootdir):

    for subdir in subdirs:
        for filename in os.listdir(os.path.join(root, subdir)):
            print(filename)
            file_path = os.path.join(root, subdir, filename)

            with open(file_path, 'rb') as f:
                html = f.read()
                soup = BeautifulSoup(html)

                link = soup.find('a').get('href')

                res = requests.get(link)

                if res.is_redirect:
                    print("Redirect: {}".format(link))

                


                # if the host url == strafrecht:
                #   check if its a pdf or image
                #       upload it
