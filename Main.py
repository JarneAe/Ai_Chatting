import os
from gtts import gTTS
import openai
import speech_recognition as sr
import webbrowser
import playsound
from dotenv import load_dotenv

load_dotenv()

API_key = os.getenv('OPENAI_API_KEY')

openai.api_key = API_key

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "



def recordAudio():
    global UserText
    # Obtain audio from the microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print('>')
        audio = recognizer.listen(source)

    # Recognize speech using Google Speech Recognition
    try:
        print("I think you said: " + recognizer.recognize_google(audio, language="en-ph"))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        recordAudio()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        exit()

    # Concatenate the words good and morning once triggered
    if recognizer.recognize_google(audio, language="en-ph").lower() == "good morning":
        inputUser = "goodmorning"
        UserText = inputUser
    else:
        inputUser = recognizer.recognize_google(audio, language="en-ph").lower()
        UserText = inputUser

    return inputUser

def ask(question):
    prompt_text = question
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt_text,
    temperature=0,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    story = response['choices'][0]['text']
    return str(story)
    

while True:
    recordAudio()
    session_prompt = f"The following is a conversation with a friend. The friend is angry, resentful, clever, and very mad.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: Hey remember how we were best friends for 15 years?\nAI: Yes, but we didn't talk for 5 years. That's not nice.\nHuman: I don't care. I'm here now you should be happy\nAI: I hate you for leaving me.\nHuman: oh come on don't be a baby\nAI: You are the baby here!\nHuman: Why do you hate me\n\nAI:\n\nYou left me when I needed you the most.\nHuman:{UserText}"
    
    
    print(UserText)
    output = ask(session_prompt)
    print(output)

    mytext = 'Welcome to geeksforgeeks!'
  
    language = 'en'
    
    myobj = gTTS(text=output, lang=language, slow=False)
    
    myobj.save("AI.mp3")

    playsound.playsound("AI.mp3")
    os.remove('AI.mp3')
    

    



