from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

import os, sys, random, partner16.language

from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from .models import (
    Statement, Reply, Communication,
)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print('MacTest: message = ' + event.message.text)

    reply_message = None
    org_text = event.message.text
    if org_text[0:10] == '16 iammac ':
        # handle admin command
        print('into handle admin command area')
        communication = partner16.language.handleAdminCommand(org_text[10:])
        if communication != None:
            reply_message = 'Execute successful, communication_id = ' \
                    + str(communication.id)
    elif org_text[0:3] == '16 ':
        communication = partner16.language.parsing(org_text[3:])
        if communication != None:
            randomList = []
            replys = communication.reply_set_set.all()
            for tmpReply in replys:
                randomList.append(tmpReply.reply.reply_text)
            reply_message = randomList[random.randint(0, len(randomList) - 1)]
    elif org_text[0:2] == '16':
        # handle personRecognition
        print('into handle personRecognition')
    else:
        # handle motionResponse
        print('into handle motionResponse')

    if reply_message != None:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

@handler.default()
def default(event):
    print(event)

# 用於防範 CSRF
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        #print('MacTest: body = ' + body)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def index(request):
    return HttpResponse('OK')
