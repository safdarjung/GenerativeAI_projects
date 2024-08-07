import os

from groq import Groq
import yt_dlp
import uuid

client = Groq(
    # api_key=os.environ.get("GROQ_API_KEY"),
    api_key="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"
)
youtube_url=input("provide the youtube video link  >")
filename = str(uuid.uuid4())
# filename = 'yt.mp4'
print("Downlaoding the Youtube Video.............")
ydl_opts={"outtmpl": f"{filename}.mkv"}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(youtube_url)

import assemblyai as aai

aai.settings.api_key = "b4a601b8964b40aeae1d4c8fdb7627c1"
transcriber = aai.Transcriber()
print("Transcribing the video .....................")
# transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
transcript = transcriber.transcribe(f"./{filename}.mkv")
ttext = transcript.text

max_transcript_length = 2000  # Adjust as needed
ttext = ttext[:max_transcript_length]

messages = [{
    "role": "system",
    "content": f"you are a chatbot that takes youtube video transcript and answers questions about it. You give answers\
          that are exact and precise based on the information context from the youtube transcript. <youtube_transcript>{ttext}</youtube_transcript> ",

}]
while True:
    user_input = input(" >>>>> ")

    max_length = 4096  # Set this to the maximum allowed length by the API

    # Combine all message contents to check the total length
    total_length = sum(len(msg['content']) for msg in messages)

    if total_length + len(user_input) > max_length:
        # Truncate the oldest messages if necessary
        while total_length + len(user_input) > max_length and messages:
            total_length -= len(messages.pop(0)['content'])

    messages.append({
        "role": "user",
        "content": user_input,
    })
    print("calling LLama3...........................")
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )

    assistant_mes = chat_completion.choices[0].message.content
    print(assistant_mes)

    messages.append({
        "role":"assistant",
        "content": assistant_mes
    })