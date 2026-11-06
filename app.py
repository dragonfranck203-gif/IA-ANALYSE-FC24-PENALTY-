import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="IA Paris", layout="centered")
st.title("📊 IA Analyse Cotes & Stats")
st.write("Remplis les cotes et envoie la capture des statistiques.")

API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

st.subheader("1. Les Équipes")
equipe1 = st.text_input("Nom de l'équipe 1")
equipe2 = st.text_input("Nom de l'équipe 2")

st.subheader("2. Les Cotes (Bookmaker)")
col1, col2 = st.columns(2)
with col1:
    cote_1x2 = st.text_input("Cote 1X2")
    cote_total = st.text_input("Cote Total")
    cote_score = st.text_input("Cote Score Exact")
with col2:
    cote_total1 = st.text_input("Cote Total 1")
    cote_total2 = st.text_input("Cote Total 2")
    cote_lesdeux = st.text_input("Les deux marquent")

st.subheader("3. Capture des stats")
uploaded_file = st.file_uploader("Choisir une image", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Capture chargée", use_container_width=True)

if st.button("🚀 Lancer l'analyse"):
    if not equipe1 or not equipe2:
        st.error("Veuillez entrer le nom des deux équipes.")
    elif uploaded_file is None:
        st.error("Veuillez envoyer une capture d'écran.")
    elif not API_KEY:
        st.error("Clé API manquante dans les Secrets.")
    else:
        with st.spinner("L'IA analyse..."):
            try:
                model = genai.GenerativeModel('gemini-2.0-flash')
                prompt = f"Tu es un analyste de paris sportifs. Analyse {equipe1} contre {equipe2}. Cotes : 1X2 {cote_1x2}, Total {cote_total}, Total 1 {cote_total1}, Total 2 {cote_total2}, Score Exact {cote_score}, Les deux marquent {cote_lesdeux}. Regarde la capture des stats. Calcule les probas 1/cote. Croise avec les stats. Dis s'il y a une Value Bet. Donne une recommandation finale claire."
                response = model.generate_content([prompt, image])
                st.success("✅ Analyse terminée !")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Erreur : {e}")
