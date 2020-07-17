import os,sys
import requests
from bs4 import BeautifulSoup
from tqdm import trange

answer_url = input('知乎问答链接: ')
headers = {"User-Agent": "Chrome/84.0.4147.89 Safari/537.36"}

bs = BeautifulSoup(requests.get(answer_url, headers = headers).text, 'lxml')

output_dir = bs.select_one('h1[class="QuestionHeader-title"]').text

if output_dir[-1] in ['?', '？']: output_dir = output_dir[:-1]

if not os.path.exists(output_dir): os.mkdir(output_dir)

print("Save to directory: %s" % output_dir)

figures = bs.select_one('div[class="Card AnswerCard"]').select_one('div[class="RichContent-inner"]').select('figure')
imgs = [f.img for f in figures if 'origin_image' in f.img.get('class')]

n = len(imgs)
for i in trange(n, ncols = 60):
    img = imgs[i]
    url = img.get('data-original')
    size = '{}x{}'.format(img.get('data-rawwidth'), img.get('data-rawheight'))
    file = url.split('?')[0].split('/')[-1]
    file_base = file.split('-')[1].split('_')[0]
    file_type = file.split('.')[-1]
    fn = '{}_{}.{}'.format(file_base, size, file_type)
    fp = os.path.join(output_dir, fn)
    if os.path.exists(fp): continue
    with open(fp, 'wb') as w: 
        w.write(requests.get(url, headers = headers).content)