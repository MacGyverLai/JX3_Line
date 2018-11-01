import os, sys

from .models import (
    LineUser, Statement, Reply, Communication, KeyWord, Statement_Flow, Reply_Set,
)

def sortStatement(target):
    keyWordList = target.statement.keyword_set.all()
    currentBig = 0
    for keyWord in keyWordList:
        if len(keyWord.word) > currentBig:
            currentBig = len(keyWord.word)

    return currentBig


def parsing(text):
    parsing_order = 0
    statement_flows = Statement_Flow.objects.filter(flow_order=parsing_order)

    for row in sorted(statement_flows, key=sortStatement, reverse=True):
        keyWordList = row.statement.keyword_set.all()
        for keyWord in keyWordList:
            try:
                tmpIndex = text.index(keyWord.word)
                sub_text = text[tmpIndex + len(keyWord.word):]
                rtnObj = parsingRecursive(sub_text, parsing_order + 1, row.communication)
                if rtnObj != None:
                    return rtnObj
            except ValueError:
                continue

    return None

def parsingRecursive(text, parsing_order, communication):
    statement_flows = Statement_Flow.objects.filter( \
            communication_id=communication.id, flow_order=parsing_order)

    if len(statement_flows) < 1:
        return communication
    for row in sorted(statement_flows, key=sortStatement, reverse=True):
        keyWordList = row.statement.keyword_set.all()
        for keyWord in keyWordList:
            try:
                tmpIndex = text.index(keyWord.word)
                sub_text = text[tmpIndex + len(keyWord.word):]
                return parsingRecursive(sub_text, parsing_order + 1, row.communication)
            except ValueError:
                continue

    return None


def motionResponse(text):
    try:
        if ('哈哈哈哈' in text) or ('XDDD' in text) or ('呵呵呵' in text):
            return 'XDDDD'
        elif '666' in text:
            return '真這麽666'
    except ValueError:
        return None


# 'U1ed1b508268a0e1fc8c302e8894994d8'
def getLineUser(userId):
    user = LineUser.objects.filter(line_id=userId)
    if len(user) > 0:
        return user[0]

def personRecognition(user):
    print('into personRecognition....')

    tailMessage = '！你想問我什麽，也許換個問法試試？\n' + \
            '也可以喊『16 幫幫我』我會給你提問範例~\n' + \
            '目前五毒、唐門、明教、丐幫、長歌、霸刀的資料建制中'
    if user == None:
        return '你好啊，大兄弟' + tailMessage
    elif user.nickname == '芋頭':
        return '芋~~頭~~~~~~~~~(開心' + tailMessage
    else:
        return '哈嘍~ ' + user.nickname + tailMessage

def handleUserCommand(text, userId):
    if text[0:11] == 'rememberMe ':
        nameList = text[11:].split(';')
        fullName = None
        nickName = None
        if len(nameList) > 1:
            fullName = nameList[0]
            nickName = nameList[1]
        else:
            nickName = nameList[0]

        user = LineUser.objects.filter(line_id=userId)
        if len(user) > 0:
            if fullName != None:
                user.full_name = fullName
            if nickName != None:
                user.nickname = nickName
            user.save()
        else:
            LineUser.objects.create(line_id=userId, full_name=fullName, \
                    nickname=nickName)


def handleAdminCommand(text):
    tmpCommunication = None

    if text[0:8] == 'addComm ':
        # ex. addComm 門派|哪些;純陽,少林|七秀,唐門
        print('into add communication....')
        commandList = text[8:].split(';')
        keyWordList = commandList[0].split('|')
        keyAnswerList = commandList[1].split('|')
        tmpCommunication = Communication.objects.create()

        flowOrder = 0
        for keyWord in keyWordList:
            tmpKeyWordList = KeyWord.objects.filter(word=keyWord)
            if (len(tmpKeyWordList) < 1):
                tmpStatement = Statement.objects.create()
                tmpKeyWord = KeyWord.objects.create(word=keyWord, statement=tmpStatement)
            else:
                tmpStatement = tmpKeyWordList[0].statement
            Statement_Flow.objects.create(statement=tmpStatement, \
                    communication=tmpCommunication, flow_order=flowOrder)
            flowOrder = flowOrder + 1

        for keyAnswer in keyAnswerList:
            tmpReply = Reply.objects.create(reply_text=keyAnswer)
            Reply_Set.objects.create(reply=tmpReply, communication=tmpCommunication)

    elif text[0:9] == 'addState ':
        # ex. addState 什麼|門派;31
        print('into add statement....')
        commandList = text[9:].split(';')
        keyWordList = commandList[0].split('|')
        tmpCommunication = Communication.objects.get(id=commandList[1])

        flowOrder = 0
        for keyWord in keyWordList:
            tmpKeyWordList = KeyWord.objects.filter(word=keyWord)
            if (len(tmpKeyWordList) < 1):
                tmpStatement = Statement.objects.create()
                tmpKeyWord = KeyWord.objects.create(word=keyWord, statement=tmpStatement)
            else:
                tmpStatement = tmpKeyWordList[0].statement
            Statement_Flow.objects.create(statement=tmpStatement, \
                    communication=tmpCommunication, flow_order=flowOrder)
            flowOrder = flowOrder + 1

    elif text[0:9] == 'addReply ':
        # addReply 我也不知道...|可能吧～;31
        print('into add reply....')
        commandList = text[9:].split(';')
        keyAnswerList = commandList[0].split('|')
        tmpCommunication = Communication.objects.get(id=commandList[1])

        for keyAnswer in keyAnswerList:
            tmpReply = Reply.objects.create(reply_text=keyAnswer)
            Reply_Set.objects.create(reply=tmpReply, communication=tmpCommunication)

    elif text[0:11] == 'addKeyword ':
        # addKeyword 氣純|紫霞功
        print('into add keyword....')
        keywordList = text[11:].split('|')

        tmpStatement = None
        for keyword in keywordList:
            tmpKeyword = KeyWord.objects.filter(word=keyword)
            if len(tmpKeyword) > 0:
                tmpStatement = tmpKeyword[0].statement
        if tmpStatement == None:
            tmpStatement = Statement.objects.create()

        for keyword in keywordList:
            KeyWord.objects.create(word=keyword, statement=tmpStatement)

    return tmpCommunication
