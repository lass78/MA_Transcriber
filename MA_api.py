import os
import requests
import json

username = os.environ.get("DR_USERNAME")
password = os.environ.get("DR_PW")

def get_mp4_url(item):
    
    videos = item['media_object_group'][0]['media_object'][0]['mob_instance']

    url = None
    for video in videos:
        if video['min_fmt_mime_type'] == 'mp4':
            url = video['min_location_url']
    return url         

def get_mp4_as_bytes(url):
    r = requests.get(url)
    return r.content
       
def get_mp3_as_bytes(url):
    r = requests.get(url)
    return r.content
       

def get_mp3_url(item):
    sounds = item['media_object_group'][0]['media_object'][0]['mob_instance']

    url = None
    for sound in sounds:
        if sound['min_fmt_mime_type'] == 'mp3':
            url = sound['min_location_url']
    return url 

def get_item(id):
    baseurl = "http://mawsc:8000/ma/api/items/"
    url = baseurl + id
    response = requests.get(url, auth=(username, password))
    response.encoding ='utf-8'

    return json.loads(response.text)

def search(string):
    baseurl = "http://mawsc:8000/ma/api/search?q="
    url = baseurl + string + "&pageSize=100"
    response = requests.get(url, auth=(username, password))
    response.encoding ='utf-8'

    return json.loads(response.text)
    

if __name__ == '__main__':

    id = "12307995"
    podcast = "12567911"

    tvavisen = "00122241430"

    item = (get_item(podcast))
    mp3url = get_mp3_url(item)
    print (mp3url)

    # result = search(tvavisen)
    # for item in result['Items']:
    #     if item['itm_has_material']:
    #         print (item['itm_title'])


    # print (len(result['Items']))
    # # print(result)

    # # with open("example.json", "w") as f:
    # #     f.write(search(tvavisen))




    # with open('tmp_item.json', 'w') as f:
    #     f.write(item)    


