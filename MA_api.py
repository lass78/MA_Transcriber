import os
import requests
import json

username = os.environ.get("DR_USERNAME")
password = os.environ.get("DR_PW")

print (username)
print (password)

prodn = "00102200330"



def get_mp4(item):
    
    videos = item['media_object_group'][0]['media_object'][0]['mob_instance']

    url = ''
    for video in videos:
        if video['min_fmt_mime_type'] == 'mp4':
            url = video['min_location_url']
         
    
    return url
    r = requests.get(url)
    

    with open('video.mp4', 'wb') as f:  # use `"b"` to open in `bytes mode`
        print("downloading")
        f.write(r.content)
        return f
        print("finished downloading")




    # return (item['media_object_group'][0]['media_object'][0]['mob_instance'])    

def get_item(id):
    baseurl = "http://mawsc:8000/ma/api/items/"
    url = baseurl + id
    response = requests.get(url, auth=(username, password))
    response.encoding ='utf-8'

    return json.loads(response.text)

id = "12307995"

# with open("example.json", "w") as f:
#     f.write(response.text)


def search(string):
    baseurl = "http://mawsc:8000/ma/api/search?q="
    url = baseurl + string + "&pageSize=100"
    response = requests.get(url, auth=(username, password))
    response.encoding ='utf-8'

    return json.loads(response.text)
    

tvavisen = "00122241430"


result = search(tvavisen)
for item in result['Items']:
    if item['itm_has_material']:
        print (item['itm_title'])


print (len(result['Items']))
# print(result)

# with open("example.json", "w") as f:
#     f.write(search(tvavisen))


item = get_item(id)
print(type(item))

print (get_mp4(item))

# with open('tmp_item.json', 'w') as f:
#     f.write(item)    

