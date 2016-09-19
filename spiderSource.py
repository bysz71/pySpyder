#-*- coding:utf-8 -*-
import re
import requests
import os

def asInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def dowmloadPic(html,keyword, start):


    pic_url = re.findall('"objURL":"(.*?)",',html,re.S)
    i = 0
    print ('找到关键词:'+keyword+'的图片，现在开始下载图片...')
    for each in pic_url:
        print ('正在下载第'+str(start*30 + i + 1)+'张图片，图片地址:'+str(each))
        try:
            pic= requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print ('【错误】当前图片无法下载')
            continue
        directory = 'D:/pythonSpider/pics/' + keyword.split(" ")[0] + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        fileName = directory + str(start*30 + i + 1) + '.jpg'
        #resolve the problem of encode, make sure that chinese name could be store
        fp = open(fileName,'wb')
        fp.write(pic.content)
        fp.close()
        i += 1

def getImageSizeTokens(size):
    sizeDict = { 'ultra': '9',
                 'large': '3',
                 'medium': '2',
                 'small': '1',
                 'all': '0'}
    if size in sizeDict:
        strSize = '&z=' + sizeDict[size]
        strW = '&width=0'
        strH = '&height=0'
    else:
        sizes = size.split('*')
        if len(sizes) == 2 and asInt(sizes[0]) and asInt(sizes[1]):
            strSize = '&z='
            strW = '&width=' + sizes[0]
            strH = '&height=' + sizes[1]
        else:
            strSize = '&z=0'
            strW = '&width=0'
            strH = '&height=0'
    return {'size': strSize,
            'h': strH,
            'w': strW}


def getImageColorToken(color):
    colorDict = {'all': '0',
                 'red': '1',
                 'orenge':'256',
                 'yellow':'2',
                 'green':'4',
                 'purple':'32',
                 'pink':'64',
                 'cyen':'8',
                 'blue':'16',
                 'brown':'128',
                 'white':'1024',
                 'black':'512',
                 'blackWhite':'2048'}
    if color in colorDict:
        strColor = '&ic='+colorDict[color]
    else:
        strColor = '0'

    return strColor
                  
def getParameters(word):
    params = word.split(" ")
    keyword = params[0].replace(","," ")
    if params[1]:
        size = params[1]
    else:
        size = "all"
    if params[2]:
        color = params[2]
    else:
        color = "all"
    return {'keyword': keyword,
            'size': size,
            'color': color}



def getUrl(word, page):
    params = getParameters(word)
    
    url = ''
    base = 'http://image.baidu.com/search/index?ct=201326592'
    url += base
    
    sizeTokens = getImageSizeTokens(params['size'])
    strSize = sizeTokens['size']
    strW = sizeTokens['w']
    strH = sizeTokens['h']
    url += strSize
    
    constantToken1 = '&tn=baiduimage&ipn=r'
    url += constantToken1

    strKey = '&word=' + params['keyword']
    url += strKey

    strPageNumber = '&pn=' + str(page * 30)
    url += strPageNumber
    
    constantToken2 = '&istype=2&ie=utf-8&oe=utf-8&cl=&lm=0&st=-1&fr=&fmq=1474063957901_R'
    url += constantToken2

    strColor = getImageColorToken(params['color'])
    url += strColor

    constantToken3 = '&se=&sme='
    url += constantToken3

    url += strW
    url += strH

    constantToken4 = '&face=0'
    url += constantToken4

    print(url)
    return url
            
        

if __name__ == '__main__':
    word = input("Input key word: ")
    max = 10
    for num in range(0,max):
        url = getUrl(word, num)
        result = requests.get(url)
        dowmloadPic(result.text,word, num)
