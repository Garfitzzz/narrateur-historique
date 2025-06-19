import streamlit as st
import requests
import os

# Configuration
st.set_page_config(page_title="Narrateur Historique", layout="centered")
st.title("🎙️ Générateur vocal historique")

# Entrée utilisateur
theme = st.text_input("🔎 Entrez un personnage, un thème ou un événement historique")
voice_choice = st.selectbox("🎤 Choisissez une voix", [
    "Rachel", "Antoni", "Elli", "Josh", "Bella"
])

if theme:
    st.markdown(f"📚 Recherche d'images pour **{theme}**...")

    # API Pixabay (nécessite une clé API dans les variables d'environnement)
    api_key = os.getenv("PIXABAY_API_KEY")
    if api_key:
        res = requests.get(
            f"https://pixabay.com/api/?key={api_key}&q={theme}&image_type=photo&lang=fr&per_page=5"
        )
        if res.status_code == 200:
            data = res.json()
            for hit in data.get("hits", []):
                st.image(hit["webformatURL"], width=500)
        else:
            st.error("Erreur lors de la récupération des images.")
    else:
        st.warning("Clé API Pixabay manquante (PIXABAY_API_KEY).")

    texte = st.text_area("📝 Texte à lire")
    if st.button("🔊 Générer la voix") and texte:
        eleven_api_key = os.getenv("ELEVENLABS_API_KEY")
        voice_id = {
            "Rachel": "21m00Tcm4TlvDq8ikWAM",
            "Antoni": "ErXwobaYiN019PkySvjV",
            "Elli": "MF3mGyEYCl7XYWbV9V6O",
            "Josh": "TxGEqnHWrfWFTfGW9XjX",
            "Bella": "EXAVITQu4vr4xnSDxMaL"
        }.get(voice_choice, "EXAVITQu4vr4xnSDxMaL")

        if eleven_api_key:
            headers = {
                "xi-api-key": eleven_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": texte,
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
            }
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers=headers,
                json=payload
            )
            if response.ok:
                audio_path = "audio.mp3"
                with open(audio_path, "wb") as f:
                    f.write(response.content)
                st.audio(audio_path)
                st.success("Audio généré avec succès !")
            else:
                st.error("Erreur lors de la génération audio.")
        else:
            st.warning("Clé API ElevenLabs manquante (ELEVENLABS_API_KEY).")
