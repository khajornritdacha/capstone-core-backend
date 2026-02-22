from gtts import gTTS
text = "Why Learn Chinese?\nGlobal Importance: Spoken by over 1 billion people. Cultural Richness: Access to a millennia-old civilization. Business Opportunities: Growing economic ties worldwide. Cognitive Benefits: Enhances memory and problem-solving skills. Travel Experience: Deepen your understanding of China."
tts = gTTS(text, lang='en')
tts.save('hello.mp3')