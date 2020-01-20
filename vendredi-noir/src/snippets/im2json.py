import cv2
import numpy as np
import base64
import json

"""
画像 <-> json スクリプト例
@author: wakame-tech
"""

def im2json(filename):
    with open(filename, 'rb') as f:
        raw = base64.b64encode(f.read())

    print(f'L: {len(raw)}')

    return json.dumps({'img': raw.decode('utf-8') })

def json2im(j):
    raw = json.loads(j)['img']
    img_data = base64.b64decode(raw)
    img_np = np.fromstring(img_data, np.uint8)
    src = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

    return src

j = im2json('path/to/image')
im = json2im(j)
cv2.imshow('result', im)
cv2.waitKey(0)