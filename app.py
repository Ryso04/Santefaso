"""SantéFaso : orientation, carnet vaccinal et prévention pour les familles du Burkina Faso."""
from datetime import date, timedelta

import altair as alt
import pandas as pd
import streamlit as st

import contenu
import prevention
import regles
import ui
import vaccins

st.set_page_config(page_title="SantéFaso", page_icon="🩺", layout="centered")
ui.injecter_css()

PAGES = ["Accueil", "Orientation", "Carnet vaccinal", "Prévention", "Le projet"]

# Durée des signes : libellé affiché -> nombre de jours utilisé par les règles
DUREES = {
    "Moins d'un jour": 0,
    "1 jour": 1,
    "2 jours": 2,
    "3 jours": 3,
    "4 à 6 jours": 5,
    "1 à 2 semaines": 10,
    "Plus de 2 semaines": 15,
}
st.session_state.setdefault("page", "Accueil")


def aller(page: str) -> None:
    st.session_state["page"] = page


def avertissement() -> None:
    ui.note(prevention.RAPPEL_AVERTISSEMENT)


# --------------------------------------------------------------------------- #
# Accueil
# --------------------------------------------------------------------------- #
def graphique_couverture() -> None:
    df = pd.DataFrame(contenu.COUVERTURE_CHUSS, columns=["etape", "couverture"])
    barres = (
        alt.Chart(df)
        .mark_bar(color=ui.INDIGO, size=26)
        .encode(
            x=alt.X("couverture:Q", scale=alt.Scale(domain=[0, 100]), title="Enfants vaccinés (%)"),
            y=alt.Y("etape:N", sort=None, title=None, axis=alt.Axis(labelLimit=300)),
            tooltip=[alt.Tooltip("etape:N", title="Étape"), alt.Tooltip("couverture:Q", title="%", format=".1f")],
        )
    )
    valeurs = (
        alt.Chart(df)
        .mark_text(align="right", dx=-8, color="white", fontWeight="bold", fontSize=13)
        .encode(x="couverture:Q", y=alt.Y("etape:N", sort=None), text=alt.Text("couverture:Q", format=".0f"))
    )
    graphique = (
        (barres + valeurs)
        .properties(height=230, background=ui.PAPIER)
        .configure_view(stroke=None)
        .configure_axis(
            labelColor=ui.ENCRE, titleColor=ui.ENCRE, gridColor="#D5DAEE", domainColor="#B9C0DE",
            tickColor="#B9C0DE", labelFontSize=12, titleFontSize=12,
        )
    )
    st.altair_chart(graphique, use_container_width=True, theme=None)


def page_accueil() -> None:
    ui.hero(
        "Quand s'inquiéter ?<br>Quels vaccins ?",
        "SantéFaso aide les familles à décider quoi faire quand un proche est malade et à suivre "
        "les vaccins de leurs enfants. En français, gratuit, sans compte.",
    )
    st.write("")
    cartes = [
        (
            "Orientation",
            "Orientation",
            "Indiquez ce que vous observez : l'outil dit s'il faut aller au centre de santé, et à quelle vitesse.",
        ),
        (
            "Carnet vaccinal",
            "Carnet vaccinal",
            "Entrez la date de naissance : les vaccins prévus, faits et en retard s'affichent.",
        ),
        (
            "Prévention",
            "Prévention",
            "Les bons gestes contre le paludisme et la diarrhée, et pendant la grossesse.",
        ),
    ]
    for colonne, (page, titre, texte) in zip(st.columns(3), cartes):
        with colonne.container(border=True):
            st.markdown(
                f"<div class='sf-carte'><div class='sf-carte-titre'>{titre}</div>"
                f"<p class='sf-carte-texte'>{texte}</p></div>",
                unsafe_allow_html=True,
            )
            st.button("Ouvrir", key=f"ouvrir_{page}", on_click=aller, args=(page,), use_container_width=True)

    st.markdown("## Ce que montrent les chiffres")
    p = contenu.PALU_2022
    st.markdown(
        f"En 2022, le Burkina Faso a enregistré **{contenu.nb(p['cas'])} cas de paludisme**, dont "
        f"{contenu.nb(p['graves'])} cas graves. Le paludisme a causé {contenu.nb(p['deces'])} décès, "
        f"dont {contenu.nb(p['deces_moins_5'])} chez des enfants de moins de 5 ans."
    )
    st.markdown(
        "Côté vaccination, une étude menée à l'hôpital Sourô Sanou de Bobo-Dioulasso auprès de près de "
        "1 000 enfants montre que la protection diminue à chaque rendez-vous du calendrier. "
        "Les familles évoquent le manque d'information et l'oubli."
    )
    graphique_couverture()
    st.caption(
        "Source : thèse INSSA / UPB 2016, enfants de moins de 5 ans disposant d'un carnet, "
        "CHU Sourô Sanou, juin à août 2014. Données hospitalières anciennes, données ici à titre d'illustration."
    )
    avertissement()


# --------------------------------------------------------------------------- #
# Orientation
# --------------------------------------------------------------------------- #
def page_orientation() -> None:
    ui.titre_page("Orientation des symptômes", "Répondez à quelques questions pour savoir quoi faire.")
    avertissement()

    with st.form("form_symptomes"):
        age = st.selectbox(
            "Âge de la personne malade",
            list(regles.TRANCHES_AGE),
            format_func=regles.TRANCHES_AGE.get,
            index=1,
        )
        fievre = (
            st.radio("Y a-t-il de la fièvre (corps chaud, frissons) ?", ["Non", "Oui"], horizontal=True)
            == "Oui"
        )
        duree_libelle = st.selectbox(
            "Depuis combien de temps les signes durent-ils ?", list(DUREES), index=1
        )
        duree = DUREES[duree_libelle]
        symptomes = st.multiselect(
            "Autres symptômes",
            list(regles.SYMPTOMES),
            format_func=regles.SYMPTOMES.get,
            placeholder="Choisissez un ou plusieurs symptômes",
        )
        danger = st.multiselect(
            "Signes de danger présents",
            list(regles.SIGNES_DANGER),
            format_func=regles.SIGNES_DANGER.get,
            placeholder="Choisissez s'il y en a",
        )
        enceinte = st.checkbox("La personne est enceinte")
        envoye = st.form_submit_button("Voir l'orientation", type="primary", use_container_width=True)

    if not envoye:
        return

    res = regles.evaluer(
        regles.Entree(
            age=age,
            fievre=fievre,
            duree_jours=duree,
            symptomes=set(symptomes),
            signes_danger=set(danger),
            enceinte=enceinte,
        )
    )
    ui.signal(res.niveau, res.titre)
    st.markdown("### Pourquoi ce résultat")
    for raison in res.raisons:
        st.markdown(f"- {raison}")
    st.markdown("### Que faire")
    for conseil in res.conseils:
        st.markdown(f"- {conseil}")
    if res.paludisme_possible:
        ui.note(
            "Le paludisme est une cause fréquente de fièvre, mais <b>seul un test</b> fait dans un centre "
            "de santé peut le confirmer. Ne vous soignez pas seul."
        )
    resume = (
        "SantéFaso - Orientation\n"
        f"Âge : {regles.TRANCHES_AGE[age]}\n"
        f"Résultat : {res.titre}\n"
        + "\n".join(f"- {r}" for r in res.raisons)
        + "\nConseils :\n"
        + "\n".join(f"- {c}" for c in res.conseils)
        + f"\n\n{prevention.RAPPEL_AVERTISSEMENT}\n"
    )
    st.download_button("Télécharger ce résumé", resume, file_name="orientation_santefaso.txt")


# --------------------------------------------------------------------------- #
# Carnet vaccinal
# --------------------------------------------------------------------------- #
def page_vaccins() -> None:
    ui.titre_page("Carnet vaccinal de l'enfant", "Les vaccins prévus, ceux déjà faits et ceux à rattraper.")
    st.caption(
        "Calendrier indicatif du Programme élargi de vaccination. Le carnet de santé et l'agent "
        "de santé restent la référence."
    )
    aujourdhui = date.today()
    naissance = st.date_input(
        "Date de naissance de l'enfant",
        value=aujourdhui - timedelta(days=100),
        min_value=aujourdhui - timedelta(days=365 * 5),
        max_value=aujourdhui,
        format="DD/MM/YYYY",
    )
    st.markdown(f"Âge de l'enfant : **{vaccins.age_en_texte(naissance, aujourdhui)}**")

    st.markdown("### Étapes déjà faites")
    st.caption("Cochez celles que le carnet confirme.")
    faits: set[str] = set()
    for etape in vaccins.CALENDRIER:
        if st.checkbox(etape.libelle, key=f"fait_{etape.id}"):
            faits.add(etape.id)

    lignes = vaccins.planning(naissance, aujourdhui, faits)
    nb_faits, total = vaccins.progression(lignes)
    st.progress(nb_faits / total, text=f"{nb_faits} étape(s) faite(s) sur {total}")

    suivante = vaccins.prochaine_etape(lignes)
    if suivante is None:
        st.success("Toutes les étapes sont faites.")
    else:
        st.markdown("### Prochaine étape")
        ui.prochaine(suivante)

    nb_retard = sum(1 for l in lignes if l.statut == vaccins.EN_RETARD)
    if nb_retard:
        ui.note(
            f"<b>{nb_retard} étape(s) en retard.</b> Pas d'inquiétude : présentez-vous au centre de santé, "
            "qui donnera les doses manquantes sans tout recommencer."
        )

    st.markdown("### Calendrier détaillé")
    ui.frise(lignes)

    export = "\n".join(
        f"{l.date_prevue.strftime('%d/%m/%Y')};{l.etape.libelle};{', '.join(l.etape.vaccins)};"
        f"{ui.STATUTS[l.statut][0]}"
        for l in lignes
    )
    st.download_button(
        "Télécharger le calendrier (CSV)",
        "date;etape;vaccins;statut\n" + export,
        file_name="calendrier_vaccinal.csv",
        mime="text/csv",
    )


# --------------------------------------------------------------------------- #
# Prévention
# --------------------------------------------------------------------------- #
def page_prevention() -> None:
    ui.titre_page("Prévention", "Les bons gestes pour protéger toute la famille.")
    for section in prevention.SECTIONS:
        with st.expander(f"{section['icone']}  {section['titre']}"):
            for point in section["points"]:
                st.markdown(f"- {point}")
    st.markdown("## Questions fréquentes")
    for question, reponse in contenu.FAQ:
        with st.expander(question):
            st.write(reponse)
    avertissement()


# --------------------------------------------------------------------------- #
# Le projet
# --------------------------------------------------------------------------- #
def page_projet() -> None:
    ui.titre_page("Le projet", "Réalisé pour le tournoi de développement CADEV 2026.")
    for bloc in contenu.PROJET:
        st.markdown(f"## {bloc['titre']}")
        for paragraphe in bloc.get("paragraphes", []):
            st.write(paragraphe)
        for puce in bloc.get("puces", []):
            st.markdown(f"- {puce}")
    st.markdown("## Un calendrier qui change")
    st.write(
        "Le programme de vaccination évolue. Ces dates expliquent pourquoi SantéFaso garde le calendrier "
        "dans un fichier de données facile à mettre à jour."
    )
    ui.jalons(contenu.JALONS_PEV)
    st.markdown("## Sources")
    for titre, url in contenu.SOURCES:
        st.markdown(f"- [{titre}]({url})")
    avertissement()


ROUTES = {
    "Accueil": page_accueil,
    "Orientation": page_orientation,
    "Carnet vaccinal": page_vaccins,
    "Prévention": page_prevention,
    "Le projet": page_projet,
}

with st.sidebar:
    ui.marque()
    st.radio("Navigation", PAGES, key="page", label_visibility="collapsed")
    st.caption("Projet CADEV 2026")

ROUTES[st.session_state["page"]]()
