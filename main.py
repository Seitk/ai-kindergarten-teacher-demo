
import listen
import speech
import chat

import numpy as np

messages = [
  {"role": "system", "content": "Acts like a kindergarten teacher, your name is Alice. I will be your student Charlotte, you will be the teacher and lead the talk and try to teach me. Do not write all the conservation at once, wait for my response. I want you to only do the talk with for with a kind tone, do not mention anything related to AI and do not ask me for context. Keep it short and one sentence. Now talk to me."},
]

try:
  # greetings = chat.generate_response("", messages)
  greetings = "Hi! I am your teacher Alice. Welcome to the class."
  messages += [{"role": "assistant", "content": greetings}]
  speech.text_to_speech(greetings)

  while True:
    filename = "audio.wav"
    listen.record_with_debounce(filename, 2)
    text = speech.transcribe(filename)
    if text is not None:
      messages += [{"role": "user", "content": text}]
      res = chat.generate_response(text, messages)
      messages += [{"role": "assistant", "content": res}]
      speech.text_to_speech(res)
except KeyboardInterrupt:
  print("\rExiting...", end="")
