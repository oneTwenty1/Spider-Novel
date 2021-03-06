#-*- coding:UTF-8 -*-
__author__ = 'winter'

from time import ctime,sleep
import os

from utils.urlTools import UrlTools
from utils.fileTools import FileTools
from utils.logTools import  Log
from code import systemCode


novelsNo = ['167_167729', '27_27047', '167_167732', '167_167728', '167_167714',  '167_167715',
            '167_167711', '167_167708',]


# from parse.shenxuParse import ShenXuParse  python 3.5
from parse.biXiaWenXueParse import BiXiaWenXueParse
from bean.novel.downloadnovelItem import DownLoadNovelItem

class SpiderMannager(object):
    def __init__(self):
        pass

    def getNovelListFromConfig(self):
        Log.info("getNovelListFromConfig")
        fileTools = FileTools(systemCode.downloadNovelsInfoFile)
        allNovelNos = fileTools.readFile()
        Log.info("download file info "+allNovelNos)
        novels = []
        if allNovelNos != " ":
            list = allNovelNos.split('\r\n')
            list = novelsNo
            for index, raw in enumerate(list):
                if raw != "":
                    baseUrl = systemCode.baseUrl
                    novelUrl = baseUrl +u'/'+raw+u'/'
                    item = DownLoadNovelItem(baseUrl, novelUrl)
                    novels.append(item)
                    Log.info("DownInfo is baseUrl[ %s ] novelUrl[ %s ] "%(baseUrl, novelUrl))
                else:
                    Log.error("DownInfo raw is null")
        else:
            Log.waring("DownInfo is null!")
        return novels

    def manager(self):
        novels = []
        i = 1
        while True:
            novels = self.getNovelListFromConfig()
            Log.info("updateNovel " + str(novels))
            if len(novels) > 0:
                for  index, novel in enumerate(novels):
                    if systemCode.baseUrl in novel.baseUrl():  ## 陛下文学网
                        print(u"download source page "+systemCode.baseUrl)
                        Log.info(u"download source page "+systemCode.baseUrl)
                        self.analysisNovelInfo(self.getNovel(novel), novel)
                        print(u"parse source page "+systemCode.baseUrl)
                        Log.info(u"parse source page "+systemCode.baseUrl)
                        novelUrl = novel.novelUrl()
                        fileName = novel.fileName()
                        novelNo = novel.novelNo()
                        localFolder = novel.localFolder()
                        fileTools = FileTools(localFolder + u'/' + fileName)
                        content = fileTools.readFile()
                        bixiaParse = BiXiaWenXueParse(content)
                        bixiaParse.setUrl(novelUrl)
                        bixiaParse.setLocalFolder(localFolder)
                        bixiaParse.setNovelNo(novelNo) ##novelNo
                        bixiaParse.parse()
                    else:
                        Log.error("now unsupport this network "+novel)
                print("no %s all over %s" %(i,ctime()))
                Log.info("no %s all over %s" %(i,ctime()))
                i = i + 1
            sleep(60*3600*12)


    def getNovel(self,novel):
        url = novel.novelUrl()
        fileName = novel.fileName()
        localFolder = novel.localFolder()
        print(localFolder)
        Log.info("getNovel local [ %s ] fileName [ %s ] novelUrl [ %s ] "%(localFolder, fileName, url))
        if not os.path.exists(localFolder):
            os.mkdir(localFolder)
        urlTools = UrlTools(url);
        header, content = urlTools.getUrlContent()
        fileTools = FileTools(localFolder+ u'/' +fileName);
        fileTools.writeNewFile(content)
        return content


    def updateNovel(self):
        novels = self.getNovelListFromConfig()
        Log.info("updateNovel " + str(novels))
        if len(novels) > 0:
            for  index, novel in enumerate(novels):
                if systemCode.baseUrl in novel.baseUrl():  ## 陛下文学网
                    print(u"download source page ")
                    Log.info(u"download source page ")
                    self.analysisNovelInfo(self.getNovel(novel), novel)
                    print(u"parse source page ")
                    Log.info(u"parse source page ")
                    novelUrl = novel.baseUrl()
                    fileName = novel.fileName()
                    localFolder = novel.localFolder()
                    novelNo = novel.novelNo()
                    fileTools = FileTools(localFolder + u'/' + fileName)
                    content = fileTools.readFile()
                    bixiaParse = BiXiaWenXueParse(content)
                    bixiaParse.setUrl(novelUrl)
                    bixiaParse.setLocalFolder(localFolder)
                    bixiaParse.setNovelNo(novelNo) ##novelNo
                    bixiaParse.parse()
                else:
                    Log.error("now unsupport this network "+novel)
            Log.info("all over %s" %(ctime()))

    ##   no#name#url#author#imageurl#lashUpdateTime#lastUpdateChapter
    def analysisNovelInfo(self, content, novel):
        Log.info("analysisNovelInfo start")
        split= str(systemCode.fileContentSplit)
        novelNo=novel.novelNo()
        name = ''
        url = novel.novelUrl()
        author = ''
        imageurl = ''
        lashUpdateTime = ''
        lastUpdateChapter = ''
        novelinfo = ''
        contentList = content.decode('utf-8').split('\r\n')
        for index, raw in enumerate(contentList):
            if '<h1>' in raw :
                name = raw.split('<h1>')[1].replace('</h1>', '')
            if '<p>作&nbsp;&nbsp;者：' in raw :
                author = raw.split('者：')[1].replace('</p>', '')
            if '<img alt' in raw :
                imageurl = systemCode.baseUrl+raw.split('src="')[1].split('" width')[0]
            if '<p>最后更新：' in raw :
                lashUpdateTime = raw.split('更新：')[1].replace('</p>', '')
            if ' <p>最新更新：' in raw :
                lastUpdateChapter = raw.split('">')[1].replace('</a></p>', '')
        novelinfo = str(novelNo)+split+str(name)+ split +str(url)+ split +str(author)+ split \
                    +str(imageurl)+ split +str(lashUpdateTime)+ split +str(lastUpdateChapter)
        Log.info(novelinfo)

        fileTools = FileTools(systemCode.baseFolder+ u'/SourceUrlFile/'+systemCode.allNovelsNameInfoFile)
        allNovels = fileTools.readFile()
        # if allNovels != "":
        if novelNo not in allNovels:
            fileTools1 = FileTools(systemCode.baseFolder+ u'/SourceUrlFile/'+systemCode.allNovelsNameInfoFile)
            fileTools1.fileWriteAppend(novelinfo)
        else:
            Log.info("analysisNovelInfo [%s]  is already exist!"%(novelinfo))
            # allNovelsList = allNovels.split('\r\n')
            # for index,raw in enumerate(allNovelsList):
            #     if name in raw:
            #         tmpAllNovels += novelinfo+'\r\n';
            #     else:
            #         tmpAllNovels += raw+'\r\n';
        # else:
        tmpAllNovels = novelinfo+'\r\n';

        Log.info("analysisNovelInfo end")

