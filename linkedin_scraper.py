import streamlit as st
import requests
import csv
import io

st.set_page_config(page_title="Export LinkedIn", page_icon="📇")
st.title("📇 Export LinkedIn - Mes Contacts")
st.write("Colle ici ton cookie `li_at` pour extraire tous tes contacts LinkedIn.")

li_at = st.text_input("🔐 Cookie LinkedIn 'li_at'", type="password")

if st.button("📥 Extraire mes contacts en CSV") and li_at:
    headers = {
        "cookie": f"li_at={li_at}",
        "User-Agent": "Mozilla/5.0",
    }

    url = "https://www.linkedin.com/voyager/api/relationships/connections"
    params = {
        "count": 100,
        "start": 0,
        "sortType": "RECENTLY_ADDED",
    }

    connections = []

    with st.spinner("⏳ Extraction en cours..."):
        while True:
            res = requests.get(url, headers=headers, params=params)
            if res.status_code != 200:
                st.error("❌ Cookie invalide ou session expirée.")
                break

            data = res.json()
            elements = data.get("elements", [])
            if not elements:
                break

            for conn in elements:
                mini = conn.get("miniProfile", {})
                connections.append({
                    "Nom": mini.get("firstName", "") + " " + mini.get("lastName", ""),
                    "Titre": mini.get("occupation", ""),
                    "URL Profil": "https://www.linkedin.com/in/" + mini.get("publicIdentifier", "")
                })

            params["start"] += 100

    if connections:
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=["Nom", "Titre", "URL Profil"])
        writer.writeheader()
        writer.writerows(connections)
        buffer.seek(0)

        st.success(f"✅ {len(connections)} contacts exportés avec succès.")
        st.download_button(
            label="📁 Télécharger le fichier CSV",
            data=buffer,
            file_name="linkedin_contacts.csv",
            mime="text/csv"
        )
