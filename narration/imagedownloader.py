import time  
import sys  
import os
import argparse
from urllib.request import Request, urlopen
from urllib.request import URLError, HTTPError
import random
from PIL import Image

                
class Downloader(object):
    
    def download_page(self , url):
        import urllib.request
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    

    def _images_get_next_item(self , s):
        start_line = s.find('rg_di')
        if start_line == -1: 
            end_quote = 0
            link = "no_links"
            return link, end_quote
        else:
            start_line = s.find('"class="rg_meta"')
            start_content = s.find('"ou"', start_line + 1)
            end_content = s.find(',"ow"', start_content + 1)
            content_raw = str(s[start_content + 6:end_content - 1])
            return content_raw, end_content

    def _images_get_all_items(self , page):
        items = []
        mn = 0
        while mn<5:
            item, end_content = self._images_get_next_item(page)
            if item == "no_links":
                break
            else:
                items.append(item)
                time.sleep(0.1) 
                page = page[end_content:]
                mn = mn + 1
        return items

    def Download(self ,keywords):
        itemis = []
        print(keywords)
        for i, keyword in enumerate(keywords):
            if keyword != '':   
                print('finding url for', keyword)
                items = []
                search_term = keyword
                search_term = search_term.replace('#', '%23')
                search = search_term.replace(' ', '%20')
                url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch'
                raw_html = (self.download_page(url))
                time.sleep(0.1)
                items = items + (self._images_get_all_items(raw_html))
                
                x = 0
                for k, item in enumerate(items):
                    image_name = str(item[(item.rfind('/'))+1:])
                    if ".png" in image_name or ".svg" in image_name or ".jpg" not in image_name:
                        x = k+1
                    else:
                        break

                itemi= items[x]
                print(itemi)
                itemis.append(itemi)
                img_name = keyword 
                self.get_image(item=itemi, position=i, name = img_name)
    def get_image(self, item, position=0, dir_name = 'narration/photos', name = 'default_image'):
        try:
            req = Request(item, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req, None, 15)
            #image_name = str(item[(item.rfind('/'))+1:])
            #if '?' in image_name:
             #   image_name = image_name[:image_name.find('?')]
            #if ".jpg" in image_name or ".png" in image_name or ".jpeg" in image_name or ".svg" in image_name:
             #   output_file = open(dir_name + "/" + image_name +str() + ". " + image_name, 'wb')
            #else:
            image_name = name + ".jpg"
            output_file = open(dir_name + "/" + image_name, 'wb')
            
            data = response.read()
            output_file.write(data)
            response.close()
            output_file.close()

            path = dir_name + "/" + image_name
            im = Image.open(path)
            size = 500, 500
            im.resize((600,600), Image.ANTIALIAS)
            im.save(path, 'JPEG')
        except IOError:
            print("IOError on image ")


        except HTTPError as e:  # If there is any HTTPError
            print("HTTPError")
        
        except URLError as e:
            print("URLError ")
 






