from django.http import HttpResponse
from .models import Stats,Tweets
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from textblob import TextBlob
import pickle

@csrf_exempt
def index(request,clickdate=None):
    template = 'visual/index.html'
    currencyList = [x.title() for x in pickle.load(open('/home/sahaj/Desktop/UG-2/NLPAndMachineL/CryptoCoinProject/automateScripts/curr_currencies.p','rb'))]
    context = {'currencies':currencyList,'currencyData':[],'currencyTweets':[],'currencyname':'','sentiment':[[],[],[]],'wordCloud':{}}
    if request.method == 'POST' or clickdate is not None:

        if clickdate is not None:
            currency = clickdate.split('_')[0].lower()
            clickdate = clickdate.split('_')[1]
            start_date = end_date = datetime.datetime.strptime(clickdate,'%a %b %d %Y 00:00:00 GMT')
        else: 
            start_date = datetime.datetime.strptime(request.POST.get('start'),'%m/%d/%Y')
            end_date = datetime.datetime.strptime(request.POST.get('end'),'%m/%d/%Y')
            currency = request.POST.get('currency').lower()
        
        currdata = Stats.objects(currname=currency)
        currtweets = Tweets.objects(currname=currency)
        
        wordCloud = {}
        for var in currtweets:
            if datetime.datetime.strptime(var['created'],'%a %b %d %H:%M:%S +0000 %Y').date() >= start_date.date() and datetime.datetime.strptime(var['created'],'%a %b %d %H:%M:%S +0000 %Y' ).date() <= end_date.date():
                blob = TextBlob(var['tweetText'])
                sentiment = blob.sentiment.polarity
                date = datetime.datetime.strptime(var['created'],'%a %b %d %H:%M:%S +0000 %Y').strftime('%d/%m/%Y') 
                try:
                    if wordCloud[date]:
                        pass
                except:
                    wordCloud[date] = {}

                for words in blob.word_counts.keys():
                    try:
                        wordCloud[date][words] += blob.word_counts[words]
                    except: 
                        wordCloud[date][words] = blob.word_counts[words] 
                
                if sentiment > 0:
                    context['sentiment'][0].append([datetime.datetime.strptime(var['created'],'%a %b %d %H:%M:%S +0000 %Y').strftime('%d %b %Y'),sentiment])
                elif sentiment < 0:
                    context['sentiment'][2].append([datetime.datetime.strptime(var['created'],'%a %b %d %H:%M:%S +0000 %Y').strftime('%d %b %Y'),sentiment])
                else:
                    context['sentiment'][1].append([datetime.datetime.strptime(var['created'],'%a %b %d %H:%M:%S +0000 %Y').strftime('%d %b %Y'),sentiment])

                context['currencyTweets'].append([var,sentiment])

        context['wordCloud'] = wordCloud
        context['currencyname'] = currency.title()
        
        for var in currdata:
            if datetime.datetime.strptime(var['Date'],'%Y-%m-%d') >= start_date and datetime.datetime.strptime(var['Date'],'%Y-%m-%d') <= end_date:
                context['currencyData'].append(var)

    return render(request,template,context)