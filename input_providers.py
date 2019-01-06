import abc

import speech_recognition as sr
from speech_recognition import AudioData


class Provider(object):
    @abc.abstractmethod
    def get(self, prompt: str) -> str:
        pass


class Speech(Provider):

    def __init__(self):
        print("running speech recognition version:", sr.__version__)
        print("say 'bye' whenever you want to quit")

    def get(self, prompt: str) -> str:
        r = sr.Recognizer()
        mic = sr.Microphone()

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        print(prompt)
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio: AudioData = r.listen(source)

            try:
                response["transcription"] = r.recognize_google(audio)
            except sr.RequestError:
                # API was unreachable or unresponsive
                response["success"] = False
                response["error"] = "API unavailable"
            except sr.UnknownValueError:
                # speech was unintelligible
                response["error"] = "Unable to recognize speech"

        # TODO: check for errors
        user_input = response["transcription"]
        if user_input == "bye":
            return None
        else:
            return user_input


class Terminal(Provider):

    def __init__(self):
        print("type 'bye' whenever you want to quit")

    def get(self, prompt: str) -> str:
        user_input = input(prompt)
        if user_input == "bye":
            return None
        else:
            return user_input
