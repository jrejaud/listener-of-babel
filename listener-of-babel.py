#Babel Finder
#Uses speech recognition to find the phrase that the user said in the library of babel website
#A silly project written by Jordan Rejaud

import speech_recognition as sr
import requests, webbrowser, os
from bs4 import BeautifulSoup

babel_search = "https://libraryofbabel.info/search.html"
babel_search_cgi = "https://libraryofbabel.info/search.cgi"
babel_base_url =  "https://libraryofbabel.info/book.cgi?"

print("Babel Finder")

#Get Audio from Microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak human!")
    audio = r.listen(source)

#Recognize speech using Google Speech Recognition
try:
    text = r.recognize_google(audio)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

#TODO filter the text, remove any punctuation or caps, or w/e is not compatible with the library of babel

print("You said: " + text)

#Search the library of babel for this text
payload = {"find":text, "methinp":"method"}
r = requests.post(babel_search_cgi, data=payload) #Omg, this actually works!

#I will make the most beautiful soup for you!
soup = BeautifulSoup(r.text, 'html.parser')

#The div we care about is the third one
story_container = soup.find_all("div",class_="preview")[2]

storyAttributes = story_container['onclick']

storyURLParts = storyAttributes.split('\'')

storyLoc = storyURLParts[1]
w = storyURLParts[3]
s = storyURLParts[5]
v = storyURLParts[7]
page = storyURLParts[9]

storyURL = babel_base_url+storyLoc+"-w"+w+"-s"+s+"-v"+v+":"+page

webbrowser.open(storyURL)

#TODO Next, need to highlight the text in question... (Use a weird span trick, like it does "originally")
