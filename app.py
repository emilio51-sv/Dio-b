import streamlit as st
import openai
from langchain.llms import OpenAI

# Recupero dell'API key (assumendo di averla messa nei secrets)
openai.api_key = st.secrets["openai_api_key"]

st.title("Generatore di Blog Post con Agenti LLM")

topic = st.text_input("Inserisci un topic del blogpost:", value="Le ultime tendenze dell'intelligenza artificiale")

# Definiamo l'LLM di base
llm = OpenAI(
    temperature=0.7,
    openai_api_key=openai.api_key,
    model_name="gpt-4"  # Puoi usare anche "gpt-3.5-turbo"
)

# Agente Ricercatore: ottiene informazioni sul topic
def agente_ricercatore(topic):
    prompt = f"""
    Sei un ricercatore esperto. Raccogli informazioni chiave e aggiornate sul seguente topic:
    {topic}
    
    Fornisci un riassunto chiaro e conciso di circa 100-150 parole, includendo punti salienti e dati rilevanti.
    """
    return llm(prompt)

# Agente Scrittore: crea una bozza del blog post
def agente_scrittore(ricerca):
    prompt = f"""
    Sei un copywriter esperto. Hai a disposizione queste informazioni di ricerca:

    {ricerca}

    Sulla base di queste informazioni, scrivi una bozza di un breve blog post (circa 200-300 parole).
    Organizza il contenuto in introduzione, corpo e conclusione provvisoria.
    Mantieni uno stile chiaro e coinvolgente.
    """
    return llm(prompt)

# Agente Editor: revisiona il testo e aggiunge rifiniture
def agente_editor(bozza):
    prompt = f"""
    Sei un editor professionista. Hai di fronte questa bozza di blog post:

    {bozza}

    Rivedila per migliorare scorrevolezza, chiarezza e aggiungi una conclusione più incisiva.
    Mantieni le informazioni chiave, ma rendi il testo più accattivante. 
    Circa 250-300 parole finali.
    """
    return llm(prompt)

if st.button("Genera Blog Post"):
    with st.spinner("Generazione in corso..."):
        ricerca = agente_ricercatore(topic)
        bozza = agente_scrittore(ricerca)
        post_finale = agente_editor(bozza)
    st.subheader("Blog Post Generato")
    st.write(post_finale)
