import openai
import streamlit as st
import pyaudio
import wave
import os

# Set your OpenAI API key
# openai.api_key = ''
# Audio recording parameters
RATE = 16000
CHUNK = 1024

def record_audio(file_path, record_seconds=5):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio_with_whisper(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language="te"
        )
    return response['text']

def translate_text(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following text from Telugu to English:\n\n{input_text}",
        max_tokens=150
    )
    translated_text = response.choices[0].text.strip()
    return translated_text

def main():
    st.title("Telugu Speech to English Translator")

    if st.button("Record and Transcribe"):
        audio_file_path = "output.wav"
        st.write("Recording...")
        record_audio(audio_file_path)
        st.write("Transcribing...")
        transcribed_text = transcribe_audio_with_whisper(audio_file_path)
        st.write("Transcription: ", transcribed_text)
        st.session_state.transcribed_text = transcribed_text
        os.remove(audio_file_path)  # Clean up the audio file after transcription

    if "transcribed_text" in st.session_state:
        if st.button("Translate"):
            input_text = st.session_state.transcribed_text
            translated_text = translate_text(input_text)
            st.write("Translation: ", translated_text)

if __name__ == "__main__":
    main()
