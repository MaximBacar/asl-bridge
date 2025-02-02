# ASL-Bridge
Bridge the gap between sign language and spoken communication.

## Description

ASL-Bridge is a prototype American Sign Language translator.
The project allows to record sentences in ASL and transform them into spoken english.

ASL-Bridge can understand movement, compared to many other sign language translators, allowing to potential be able to translate the entire dictionary.


## Machine Learning Usage

To detect words, a machine learning algorithm was trained on data we collected. The data consists of key points representing the hands, arms, body and head. A machine learning model was used to extract those limbs keypoints from a video stream.

The machine learning algorithm used is LSTM

## Data collection

To collect the data, a script was written to take 60 samples of each word inside the model. Due to lack of time, only 10 words were able to be learned. This is only a proof of concept.

## Usage of Generative AI

The OpenAI GPT-4 generative AI was used to transform literal ASL translation into spoken english
It allows to transform sentences like:

'NICE MEET YOU' into 'Nice to meet you' or 'I STUDENT COMPUTER ENGINEERING' into 'I am a computer engineering student'


## Other AI Usage

The Elevenlabs API was used to generate a voice from the text decoded by chatGPT, giving a potential voice to mute people having to relay on sign language to communicate

## Members

- Asmae Loulidi
- Ihana Fahmy
- Maxim Bacar

## Google Slides Presentation 
### Click on the image to see the presentation !
[![Google Slides](https://github.com/MaximBacar/asl-bridge/blob/main/image/cover%20presentation.jpg?raw=true)](https://docs.google.com/presentation/d/e/2PACX-1vSj8GB4djKmnPdvt9DNn5HWLDc4_I3yWx-Mwfdg-LWTbwnkdrAiwF0BCiAQ1XwliMOxO4khavcStFFP/embed?start=false&loop=true&delayms=5000)

