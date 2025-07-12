import streamlit as st
import speech_recognition as sr

# Function to transcribe speech
def transcribe_speech(api, language="en-US"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        st.info("Speak now...")
        audio_text = r.listen(source)
        st.info("Transcribing...")

    try:
        if api == "Google":
            return r.recognize_google(audio_text, language=language)
        elif api == "Sphinx":
            return r.recognize_sphinx(audio_text, language=language)
        else:
            return "Unsupported API selected."
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"API request failed: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Main function to build the UI
def main():
    st.title("Improved Speech Recognition App")
    st.write("Click on the microphone to start speaking. Select options below:")

    # API selection
    api_choice = st.selectbox(
        "Choose Speech Recognition API",
        ["Google", "Sphinx"]
    )

    # Language selection
    language = st.selectbox(
        "Choose Language",
        ["en-US", "fr-FR", "sw-KE"]
    )

    # Simple list to hold multiple segments if user wants to record multiple times
    transcription_segments = []

    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, language)
        transcription_segments.append(text)
        st.success("Transcription completed.")
        st.write("Transcription:")
        st.write(text)

        # Save transcription option
        if text and "Sorry" not in text and "Could not" not in text:
            if st.button("Save Transcription to File"):
                with open("transcription.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                st.success("Transcription saved to 'transcription.txt'.")

if __name__ == "__main__":
    main()
