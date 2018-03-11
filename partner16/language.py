import os, sys

from .models import (
    Statement, Reply, Communication, Statement_Flow, Reply_Set,
)

def parsing(text):
    parsing_order = 0
    statement_flows = Statement_Flow.objects.filter(flow_order=parsing_order)

    for row in statement_flows:
        try:
            tmpIndex = text.index(row.statement.statement_text)
            sub_text = text[tmpIndex + len(row.statement.statement_text):]
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
    for row in statement_flows:
        try:
            tmpIndex = text.index(row.statement.statement_text)
            sub_text = text[tmpIndex + len(row.statement.statement_text):]
            return parsingRecursive(sub_text, parsing_order + 1, row.communication)
        except ValueError:
            continue

    return None


#def motionResponse(text):

#def personRecognition():

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
            tmpStatementList = Statement.objects.filter(statement_text=keyWord)
            if (len(tmpStatementList) < 1):
                tmpStatement = Statement.objects.create(statement_text=keyWord)
            else:
                tmpStatement = tmpStatementList[0]
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
            tmpStatementList = Statement.objects.filter(statement_text=keyWord)
            if (len(tmpStatementList) < 1):
                tmpStatement = Statement.objects.create(statement_text=keyWord)
            else:
                tmpStatement = tmpStatementList[0]
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

    return tmpCommunication
