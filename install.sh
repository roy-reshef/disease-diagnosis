#!/usr/bin/env bash

pip install spacy
python -m spacy validate
python -m spacy download en_core_web_sm
pip install pandas
pip install SpeechRecognition
sudo apt-get install -y python-pyaudio python3-pyaudio portaudio19-dev
pip install pyaudio

