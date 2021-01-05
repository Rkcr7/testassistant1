from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from jokeapi import Jokes # Import the Jokes class
from twilio.twiml.messaging_response import MessagingResponse
import requests
import random
import os
import smtplib
import phonenumbers
import re
########

from twilio.rest import Client

app = Flask(__name__)
count=0
list1=['airport', 'amusement_park', 'aquarium', 'art_gallery', 'atm', 'bakery', 'bank', 'bar', 'beauty_salon', 'bicycle_store', 'book_store', 'bowling', 'bus_station', 'cafe', 'campground', 'car_dealer', 'car_rental', 'car_repair', 'car_wash', 'casino', 'cemetery', ' church', 'cinema', 'city_hall', 'clothing_store', 'convenience_store', 'courthouse', 'dentist', 'department_store', 'doctor', 'electrician', 'electronics_store', 'embassy', 'fire_station', 'flowers_store', 'funeral_service','furniture_store', 'gas_station', 'government_office', 'grocery_store', 'gym', 'hairdressing_salon', 'hardware_store', 'homegoodsstore', 'hospital', 'insurance_agency', 'jewelry_store', 'laundry', 'lawyer', 'library', 'liquor_store', 'locksmith', 'lodging', 'mosque', 'museum', 'night_club', 'park', 'parking', 'pet_store', 'pharmacy', 'plumber', 'police_station', 'post_office', 'primary_school', 'rail_station', 'realestateagency', 'restaurant', 'rv_park', 'school', 'secondary_school','shoe_store', 'shopping_center', 'spa', 'stadium', 'storage', 'store', 'subway_station', 'supermarket', 'synagogue', 'taxi_stand', 'temple', 'tourist_attraction','train_station', 'transit_station', 'travel_agency', 'university', 'veterinarian', 'zoo']



#db.create_all()


lati=''
long=''
EMAIL_ADDRESS = '<your gmail address>'
EMAIL_PASSWORD = '<"your gmail pass">'


from twilio.rest import Client
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, World!"
#You can call to anyone by typing there no in whatsapp with country code
@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body').lower()
    sms_reply.ph = request.form.get("From")
    lat, lon = request.form.get('Latitude'), request.form.get('Longitude')
    global lati, long
    global count
    # Create reply
    sms_reply.resp = MessagingResponse()
    twiml = VoiceResponse()
    print('What user Typed:',msg)



    #resp.message("You said: {}".format(msg))
    if len(msg) == 12:
        print("first count")
        count += 1

        sms_reply.z = phonenumbers.parse(msg, "IN")
        if (phonenumbers.is_valid_number(sms_reply.z)) is True:
            print("valid:", sms_reply.z)

            sms_reply.sms = msg
            print(sms_reply.sms)
            sms_reply.id = str(random.randint(1000, 9999))
            print(sms_reply.id)
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_='whatsapp:+<your twilio number>',
                body=(sms_reply.id),
                to='whatsapp:+' + sms_reply.sms
            )

            print(message.sid)

    elif count in range(1, 999999) and msg == sms_reply.id:

        print("count:", count)
        import requests
        requests.get('<Your ngrok or server link>/dial/' + sms_reply.sms)


    elif any(c in msg for c in list1):
        import requests


        url = "https://trueway-places.p.rapidapi.com/FindPlacesNearby"

        querystring = {"location": lati+","+long, "type": msg, "radius": "1200", "language": "en"}

        headers = {
            'x-rapidapi-key': "<your TrueWay Places rapid api key>",
            'x-rapidapi-host': "trueway-places.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        ids = data['results']
        for i in range(0, len(ids)-1):

            location=str(ids[i]["location"]["lat"])+","+str(ids[i]["location"]["lng"])
            link="http://maps.google.com/maps?q="+location
            name=" *_Name:_* "+ids[i]["name"]+"\n *_Address:_* "+(response.json()["results"][i]["address"])+"\n *_Distance (Approx):_* "+str(ids[i]["distance"])+"mt"+"\n\n *_Location:_* "+link
            print(name)

            #print("Distance:", ids[i]['distance'],)
            sms_reply.resp.message(name)
            #sms_reply.resp.message(ids[i]['address'])

            #sms_reply.resp.message(str(ids[i]['distance']))
        return str(sms_reply.resp)


    elif 'user1' in msg:
        match = re.search(r'[\w\.-]+@[\w\.-]+', msg)
        l=(match.group(0))
        sms_reply.to=l
        print(l)


    elif 'subject1' in msg:
        sms_reply.subject=msg
        print('subject is:',sms_reply.subject)
    elif 'body1' in msg:
        sms_reply.body= msg
        print('body is:',sms_reply.body)
    elif 'send1' in msg:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = sms_reply.subject
            body = sms_reply.body
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(EMAIL_PASSWORD, sms_reply.to, msg)
            sms_reply.resp.message('send succesfully')
            print('send succesfully')
        print("To:",sms_reply.to)
        print("Subject:",sms_reply.subject)
        print("Body:",sms_reply.body)

    elif "my email" in msg:
        match = re.search(r'[\w\.-]+@[\w\.-]+', msg)
        s=(match.group(0))
        print("Your email:",s)

    elif "email" in msg:
        print("its email")
        sms_reply.resp.message("OK so you want to send an e-mail\n\n"
                     "1.)Firstly You have to enter email to which you want to send and click send\n\n"
                     "2.)Then type 'subject1' before entering your subject in the same line and click send\n\n"
                     "3.)And for body write 'body1' before writing mssg in the same line and click send\n\n"
                     "4.) After typing all the details types 'send1' and its done")

    else:
        print("no phone number")

    return str(sms_reply.resp)

account_sid = '<Twilio account sid>'
auth_token = '<Twilio auth_token>'

@app.route("/dial/<int:phone_number>")
def dial(phone_number):
    """Dials an outbound phone call to the number in the URL. Just
    as a heads up you will never want to leave a URL like this exposed
    without authentication and further phone number format verification.
    phone_number should be just the digits with the country code first,
    for example 14155559812."""
    client = Client(account_sid, auth_token)


    call = client.calls.create(

        url=' <your ngrok or your server link>/incoming',
        to='+{}'.format(phone_number),
        from_='<your twilio phone number>'
    )
    print(call.sid)
    return "dialing +{}. call SID is: {}".format(phone_number, call.sid)

response = requests.get('https://gofugly.in/api/content/5')
loop=data=response.json()['result']


jokearr=["joke",'jokes','funny']
endcallarr=['end','call','hangup','hung','hungup','disconnect','disconnected','cut the call']
chatarr=['chat','talk']

import requests


#To handle incoming or outgoing call
@app.route("/incoming", methods=['GET', 'POST'])
def voice():
    twiml = VoiceResponse()


    gather = Gather(action="callback",input="speech",partial_result_callback='/partial',speechTimeout="auto",language="en-IN",hints='end the call')

    gather.say("welcome to voice assistant,Give me command",voice="Polly.Raveena", language="en-IN")


    twiml.append(gather)
    twiml.redirect('/incoming')
    return str(twiml)

#To handle POST from <gather> action read out final result
@app.route("/callback",methods=['GET','POST'])
def callback():

    speech_result = request.values.get("SpeechResult",None).lower()
    resp = MessagingResponse()
    resp.message(speech_result)
    sms_reply.resp.message(speech_result)


    print ('SpeechResult:'+ speech_result)
    print(sms_reply.z)

    twiml = VoiceResponse()
    if any(c in speech_result for c in endcallarr):




        twiml.say("ok i will end the call now",voice="Polly.Raveena", language="en-IN")
        twiml.redirect('/hangup')
    elif any(c in speech_result for c in jokearr):
        gather = Gather(action="joke", input="speech", partial_result_callback='/partial', speechTimeout="auto",
                        language="en-IN", hints='hindi,english')

        gather.say("hindi or english", voice="Polly.Aditi", language="en-IN")
        twiml.append(gather)
        twiml.redirect('/incoming')
        return str(twiml)

    elif any(c in speech_result for c in chatarr):

        #gather = Gather(action="chat", input="speech", partial_result_callback='/partial', speechTimeout="auto",
                        #language="en-IN", hints='chat')

        twiml.say("Now you are transfered to chatting", voice="Polly.Aditi", language="en-IN")
        #twiml.append(gather)
        twiml.redirect('/chat')
        return str(twiml)

    elif "monkey" in speech_result:
        twiml.say("secret code detected")
        twiml.redirect("/resultone")


    else:
        twiml.say('i could not understand what are you saying Please repeat it.', voice="Polly.Aditi", language="en-IN")



    twiml.redirect('/incoming')



    #twiml.say('You Said' + speech_result, voice="Polly.Aditi", language="en-IN")
    return str(twiml)

@app.route("/partial",methods=['GET','POST'])
def partial():
    print ("SequenceNumber:" + request.values.get('SequenceNumber',None))
    print("UnstableSpeechResult:" + request.values.get('UnstableSpeechResult', None))
    print("StableSpeechResult:" + request.values.get('StableSpeechResult', None))
    return ("OK")

@app.route("/hangup",methods=['GET','POST'])
def hangup():

    speech_result = request.values.get("SpeechResult",None)

    twiml = VoiceResponse()
    twiml.say("thanks for being a nice support", voice="Polly.Raveena", language="en-IN")




    #twiml.say('You Said' + speech_result, voice="Polly.Aditi", language="en-IN")
    return str(twiml)

@app.route("/joke",methods=['GET','POST'])
def joke():

    speech_result = request.values.get("SpeechResult", None).lower()
    print ('SpeechResult:'+ speech_result)
    twiml = VoiceResponse()
    if 'hindi' in speech_result:
        s = random.randint(0, len(loop) - 1)
        joke = data = response.json()['result'][s]['joke']
        twiml.say(joke, voice="Polly.Aditi", language="hi-IN")
        twiml.say('चुटकुले ख़तम', voice="Polly.Aditi", language="hi-IN", rate='90%')
        print(joke)
        print(sms_reply.z)

    elif 'english' in speech_result:
        j = Jokes()
        joke = j.get_joke()
        if joke["type"] == "single":
            twiml.pause(length=1)
            twiml.say(joke["joke"], voice="Polly.Aditi", language="en-IN",rate='95%')  # Print the joke
            print(joke["joke"])
        else:
            twiml.pause(length=1)
            twiml.say(joke["setup"], voice="Polly.Aditi", language="en-IN",rate='85%')
            twiml.pause(length=1)
            twiml.say(joke["delivery"], voice="Polly.Aditi", language="en-IN",rate='85%')
            print(joke["setup"])
            print(joke["delivery"])



    twiml.redirect('/incoming')



    #twiml.say('You Said' + speech_result, voice="Polly.Aditi", language="en-IN")
    return str(twiml)

@app.route("/chat",methods=['GET','POST'])
def chat():
    twiml = VoiceResponse()


    gather = Gather(action='live', input="speech", partial_result_callback='/partial', speechTimeout="auto",
                    language="en-IN", hints='hindi,english')

    gather.say("your turn", voice="Polly.Aditi", language="en-IN",rate="75%")
    twiml.append(gather)
    twiml.redirect('/chat')



    #twiml.say('You Said' + speech_result, voice="Polly.Aditi", language="en-IN")
    return str(twiml)
@app.route("/live",methods=['GET','POST'])
def live():
    twiml = VoiceResponse()

    speech_result = request.values.get("SpeechResult", None).lower()
    print ('SpeechResult:'+ speech_result)
    if any(c in speech_result for c in endcallarr):




        twiml.say("ok i will end the call now",voice="Polly.Raveena", language="en-IN")
        twiml.redirect('/hangup')
    elif 'return' in speech_result:
        twiml.say("ok", voice="Polly.Raveena", language="en-IN",rate='75%')
        twiml.redirect('/incoming')

    twiml.pause(length=1)
    ai = requests.get('http://api.brainshop.ai/get?bid=154407&key=EH62f6jeFRu7e6RO&uid=2&msg=' + speech_result)
    data = ai.json()['cnt']
    print(data)
    twiml.say(data, voice="Polly.Aditi", language="en-IN",)

    twiml.redirect('/chat')
    #twiml.say('You Said' + speech_result, voice="Polly.Aditi", language="en-IN")
    return str(twiml)

@app.route("/resultone",methods=['GET','POST'])
def resultone():
    print("in twiml")
    twiml = VoiceResponse()
    gather = Gather(action="result", input="speech", partial_result_callback='/partial', speechTimeout="5",anguage="en-IN", hints='end the call')
    twiml.say("OK so now after count down to 1 anything you speak will be send it to you.",voice="Polly.Raveena", language="en-IN",rate="90%")
    gather.say(" three  two  one", voice="Polly.Raveena", language="en-IN",rate="65%")

    twiml.append(gather)

    twiml.redirect('/result')
    return str(twiml)


@app.route("/result",methods=['GET','POST'])
def result():
    twiml = VoiceResponse()
    speech_result = request.values.get("SpeechResult", None).lower()

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=speech_result,
        from_='whatsapp:+<twilio number>',
        to='whatsapp:+<sunscribed no>' #user should be subscribed to recieve message
    )

    print(message.sid)
    print("send successfully")



    twiml.redirect('/hangup')



    #twiml.say('You Said' + speech_result, voice="Polly.Aditi", language="en-IN")
    return str(twiml)



if __name__ == "__main__":
    app.run(debug=True)


