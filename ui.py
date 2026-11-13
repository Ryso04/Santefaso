"""Identité visuelle et petits composants HTML de SantéFaso.

Choix de design (propres au sujet) :
- Palette tirée du Faso Dan Fani, le cotonnade tissée en bandes du Burkina :
  indigo profond, jaune mil, rouge kola, blanc coton.
- Titres en Bricolage Grotesque, texte en Atkinson Hyperlegible (police conçue pour la
  lisibilité, utile sur de petits écrans et pour les lecteurs peu à l'aise).
- Le « tissage » (bande rayée) est le seul motif décoratif ; le reste reste sobre.
- Les statuts ne reposent jamais sur la couleur seule : toujours un mot ou un symbole.
"""
from __future__ import annotations

import streamlit as st

import vaccins

INDIGO = "#1B2559"
MILLET = "#E0A526"
KOLA = "#B4372A"
FEUILLE = "#2E7D4F"
AMBRE = "#9A5B00"
ENCRE = "#1A1D2B"
PAPIER = "#F7F8FB"
BRUME = "#E8EBF7"

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&display=swap');

:root {
  --indigo: %INDIGO%; --millet: %MILLET%; --kola: %KOLA%; --feuille: %FEUILLE%;
  --ambre: %AMBRE%; --encre: %ENCRE%; --papier: %PAPIER%; --brume: %BRUME%;
}

.stApp, .stApp [data-testid="stAppViewContainer"] {
  background: var(--papier);
  color: var(--encre);
  font-family: 'Atkinson Hyperlegible', system-ui, -apple-system, 'Segoe UI', sans-serif;
}
.stApp .block-container { max-width: 820px; padding-top: 1.4rem; padding-bottom: 4rem; }
.stApp #MainMenu, .stApp footer { visibility: hidden; }

.stApp h1, .stApp h2, .stApp h3 {
  font-family: 'Bricolage Grotesque', 'Atkinson Hyperlegible', system-ui, sans-serif;
  color: var(--indigo);
  letter-spacing: -0.01em;
}
.stApp h2 { font-size: 1.6rem; margin-top: 2.2rem; }
.stApp p, .stApp li { line-height: 1.6; }
.stApp .stMarkdown p { max-width: 68ch; }

.stApp :focus-visible { outline: 3px solid var(--millet); outline-offset: 2px; }

/* --- Barre latérale ------------------------------------------------------ */
.stApp [data-testid="stSidebar"] { background: var(--brume); border-right: 1px solid #CDD3EA; }
.sf-marque {
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 1.6rem;
  color: var(--indigo); margin: .2rem 0 .5rem 0;
}

/* --- Tissage (bande rayée du Faso Dan Fani) ------------------------------ */
.sf-tissage {
  height: 12px;
  background: repeating-linear-gradient(90deg,
    var(--indigo) 0 22px, #FFFFFF 22px 26px, var(--millet) 26px 34px, #FFFFFF 34px 38px,
    var(--kola) 38px 46px, #FFFFFF 46px 50px, var(--indigo) 50px 72px);
}
.sf-marque + .sf-tissage { margin-bottom: 1.1rem; }
.stApp .sf-hero .sf-tissage {
  height: 14px;
  background: repeating-linear-gradient(90deg,
    #3B4A9C 0 22px, #FFFFFF 22px 26px, var(--millet) 26px 34px, #FFFFFF 34px 38px,
    var(--kola) 38px 46px, #FFFFFF 46px 50px, #3B4A9C 50px 72px);
}

/* --- Bannière d'accueil -------------------------------------------------- */
.stApp .sf-hero { background: var(--indigo); border-radius: 4px; padding: 2.4rem 2rem 0 2rem; overflow: hidden; }
.stApp .sf-hero h1 {
  color: #FFFFFF; font-weight: 800; font-size: clamp(2.1rem, 7vw, 3.4rem);
  line-height: 1.04; margin: 0 0 1rem 0; padding: 0;
}
.stApp .sf-hero p { color: #DCE1F5; font-size: 1.12rem; max-width: 34rem; margin: 0 0 2rem 0; }
.stApp .sf-hero .sf-tissage { margin: 0 -2rem; }

/* --- Titre de page ------------------------------------------------------- */
.stApp .sf-titre { font-size: clamp(1.8rem, 5vw, 2.4rem); font-weight: 800; margin: .2rem 0 .2rem 0; }
.stApp .sf-soustitre { color: #4A5070; font-size: 1.05rem; margin: 0 0 1rem 0; }

/* --- Boutons ------------------------------------------------------------- */
.stApp .stButton > button, .stApp .stDownloadButton > button {
  border-radius: 4px; border: 2px solid var(--indigo); background: #FFFFFF; color: var(--indigo);
  font-weight: 700; min-height: 3rem; font-family: inherit;
}
.stApp .stButton > button:hover, .stApp .stDownloadButton > button:hover {
  background: var(--indigo); color: #FFFFFF; border-color: var(--indigo);
}
.stApp .stFormSubmitButton > button, .stApp .stButton > button[kind="primary"] {
  background: var(--indigo); color: #FFFFFF; min-height: 3.2rem; font-size: 1.05rem;
}
.stApp .stFormSubmitButton > button:hover { background: var(--millet); color: var(--encre); border-color: var(--millet); }

/* --- Formulaire ---------------------------------------------------------- */
.stApp [data-testid="stForm"] { background: #FFFFFF; border: 1px solid #CDD3EA; border-radius: 4px; padding: 1.4rem; }

/* --- Résultat d'orientation --------------------------------------------- */
.sf-signal { display: flex; gap: 1rem; align-items: center; background: #FFFFFF; border: 2px solid; border-radius: 4px; padding: 1.2rem 1.4rem; margin: 1rem 0; }
.sf-signal .sf-pastille { flex: 0 0 auto; width: 26px; height: 26px; border-radius: 50%; }
.sf-signal .sf-signal-titre { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 1.35rem; line-height: 1.2; }
.sf-urgence { border-color: var(--kola); } .sf-urgence .sf-pastille { background: var(--kola); } .sf-urgence .sf-signal-titre { color: var(--kola); }
.sf-rapide  { border-color: var(--ambre); } .sf-rapide .sf-pastille { background: var(--millet); } .sf-rapide .sf-signal-titre { color: var(--ambre); }
.sf-calme   { border-color: var(--feuille); } .sf-calme .sf-pastille { background: var(--feuille); } .sf-calme .sf-signal-titre { color: var(--feuille); }

/* --- Note --------------------------------------------------------------- */
.sf-note { background: #FFFFFF; border-left: 5px solid var(--millet); padding: .8rem 1.1rem; margin: 1rem 0; font-size: .98rem; }

/* --- Frise vaccinale ----------------------------------------------------- */
.sf-frise { border-left: 3px solid #CDD3EA; margin: 1rem 0 1rem .6rem; padding-left: 1.5rem; }
.sf-etape { position: relative; padding: 0 0 1.4rem 0; }
.sf-etape::before {
  content: ""; position: absolute; left: calc(-1.5rem - 1.5px); top: .3rem; width: 16px; height: 16px;
  border-radius: 50%; background: var(--c); transform: translateX(-50%); border: 3px solid var(--papier);
}
.sf-etape .sf-etape-titre { font-weight: 700; font-size: 1.08rem; color: var(--encre); }
.sf-etape .sf-etape-statut { font-weight: 700; color: var(--c); }
.sf-etape .sf-etape-detail { color: #3B4160; }
.sf-etape small { color: #5A6080; display: block; margin-top: .15rem; }

/* --- Prochaine étape ----------------------------------------------------- */
.sf-prochaine { background: #FFFFFF; border: 2px solid var(--indigo); border-radius: 4px; padding: 1rem 1.3rem; margin: 1rem 0; }
.sf-prochaine .sf-prochaine-titre { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 1.3rem; color: var(--indigo); }

/* --- Jalons -------------------------------------------------------------- */
.sf-jalon { display: grid; grid-template-columns: 7.5rem 1fr; gap: 1rem; padding: .7rem 0; border-top: 1px solid #CDD3EA; }
.sf-jalon:last-child { border-bottom: 1px solid #CDD3EA; }
.sf-jalon .sf-date { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; color: var(--indigo); }

/* ==========================================================================
   Robustesse : même rendu quel que soit le thème (clair ou sombre) de l'appareil.
   Sans cela, un téléphone en mode sombre affiche du texte clair sur fond clair.
   ========================================================================== */
html, body { color-scheme: light; background: var(--papier); }
.stApp [data-testid="stHeader"] { background: var(--papier) !important; }
.stApp [data-testid="stHeader"] * { color: var(--indigo) !important; }
.stApp [data-testid="stToolbar"], .stApp .stAppDeployButton, .stApp [data-testid="stDecoration"] { display: none !important; }
.stApp [data-testid="stSidebar"], .stApp [data-testid="stSidebarContent"] { background: var(--brume) !important; }
.stApp [data-testid="stSidebar"] * { color: var(--encre); }
.stApp [data-testid="stSidebar"] .sf-marque { color: var(--indigo); }
.stApp [data-testid="stSidebarCollapseButton"] *, .stApp [data-testid="stExpandSidebarButton"] * { color: var(--indigo) !important; }

/* Libellés des champs et du menu */
.stApp label p, .stApp [data-testid="stWidgetLabel"] p, .stApp [data-testid="stWidgetLabel"] label {
  color: var(--encre) !important; font-size: 1rem;
}
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p { color: #4A5070 !important; }

/* Menu de navigation */
.stApp [data-testid="stSidebar"] [data-testid="stRadio"] label { padding: .35rem .2rem; }
.stApp [data-testid="stSidebar"] [data-testid="stRadio"] label p { font-size: 1.05rem; }
.stApp [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p { color: var(--indigo) !important; font-weight: 700; }

/* Boutons radio et cases à cocher */
.stApp [data-testid="stRadioOption"] > div > div:first-child,
.stApp [data-testid="stCheckbox"] label > div:not([data-testid]) {
  background-color: #FFFFFF !important; border: 2px solid #7C86B5 !important; box-sizing: border-box;
}
.stApp [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child,
.stApp [data-testid="stCheckbox"] label:has(input:checked) > div:not([data-testid]) {
  background-color: var(--indigo) !important; border-color: var(--indigo) !important;
}

/* Listes déroulantes, champs, calendrier */
.stApp [data-testid="stSelectbox"] [role="group"], .stApp [data-testid="stMultiSelect"] [role="group"],
.stApp [data-testid="stDateInputField"] {
  background-color: var(--brume) !important; border: 1px solid #B9C0DE !important; border-radius: 4px;
}
.stApp [data-testid="stSelectbox"] input, .stApp [data-testid="stMultiSelect"] input, .stApp [data-testid="stDateInput"] input {
  color: var(--encre) !important; -webkit-text-fill-color: var(--encre);
}
.stApp [data-testid="stSelectbox"] input::placeholder, .stApp [data-testid="stMultiSelect"] input::placeholder { color: #5A6080 !important; opacity: 1; -webkit-text-fill-color: #5A6080; }
.stApp [data-testid="stSelectbox"] svg, .stApp [data-testid="stMultiSelect"] svg, .stApp [data-testid="stDateInputCalendarButton"] svg {
  color: var(--indigo) !important; fill: var(--indigo) !important;
}
.stApp [data-testid="stDateInputField"] * { color: var(--encre); }
[role="listbox"], [role="listbox"] [role="option"] { background-color: #FFFFFF !important; color: var(--encre) !important; }
[role="listbox"] [role="option"] * { color: var(--encre) !important; }
[role="listbox"] [role="option"]:hover, [role="listbox"] [role="option"][data-focused="true"],
[role="listbox"] [role="option"][aria-selected="true"] { background-color: var(--brume) !important; }

/* Barre de progression, alertes, déroulants, cartes */
.stApp [data-testid="stProgress"] [role="progressbar"] { background-color: #D5DAEE !important; }
.stApp [data-testid="stProgressBarTrack"] { background-color: transparent !important; }
.stApp [data-testid="stProgressBarTrack"] > div { background-color: var(--feuille) !important; }
.stApp [data-testid="stAlert"] { background-color: #E6F2EA !important; border: 1px solid var(--feuille); }
.stApp [data-testid="stAlert"] * { color: var(--encre) !important; }
.stApp [data-testid="stExpander"] details { background: #FFFFFF !important; border: 1px solid #CDD3EA !important; border-radius: 4px; }
.stApp [data-testid="stExpander"] summary, .stApp [data-testid="stExpander"] summary * { color: var(--encre) !important; font-weight: 700; }
.stApp [data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"] .sf-carte) {
  background: #FFFFFF; border: 1px solid #CDD3EA !important; border-radius: 4px;
}
.stApp .sf-carte-titre { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 1.25rem; color: var(--indigo); margin: 0 0 .3rem 0; }
.stApp .sf-carte-texte { color: #3B4160; font-size: .98rem; margin: 0 0 .8rem 0; min-height: 6.4rem; }
.stApp .stButton > button p, .stApp .stDownloadButton > button p, .stApp .stFormSubmitButton > button p { font-size: 1rem; }
.stApp .stButton > button p, .stApp .stDownloadButton > button p, .stApp .stFormSubmitButton > button p { color: inherit !important; }
.stApp .stButton > button, .stApp .stDownloadButton > button { color: var(--indigo); }
.stApp .stFormSubmitButton > button { color: #FFFFFF; border-color: var(--indigo); }

/* Calendrier du sélecteur de date */
[data-testid="stDateInputCalendar"] { background-color: #FFFFFF !important; color: var(--encre) !important; border: 1px solid #B9C0DE; }
[data-testid="stDateInputCalendar"] * { color: var(--encre) !important; }
[data-testid="stDateInputCalendar"] svg path[fill="none"] { fill: none !important; }
[data-testid="stDateInputCalendar"] svg path:not([fill="none"]) { fill: var(--encre) !important; }
[data-testid="stDateInputCalendar"] header button, [data-testid="stDateInputCalendar"] header div { background-color: transparent !important; }
.stApp [data-testid="stCaptionContainer"] { opacity: 1 !important; }
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p { color: #4A5070 !important; }
[data-testid="stDateInputCalendar"] [role="gridcell"] > div, [data-testid="stDateInputCalendar"] [role="gridcell"] > span { background-color: transparent !important; }
[data-testid="stDateInputCalendar"] [role="gridcell"][aria-selected="true"] *,
[data-testid="stDateInputCalendar"] [role="gridcell"] [aria-selected="true"],
[data-testid="stDateInputCalendar"] [role="gridcell"] [data-selected="true"] { background-color: var(--indigo) !important; color: #FFFFFF !important; }
[data-testid="stDateInputCalendar"] [aria-disabled="true"], [data-testid="stDateInputCalendar"] [data-disabled="true"] { opacity: .4; }

@media (max-width: 560px) {
  .stApp .sf-hero { padding: 1.8rem 1.2rem 0 1.2rem; }
  .stApp .sf-hero .sf-tissage { margin: 0 -1.2rem; }
  .sf-jalon { grid-template-columns: 1fr; gap: .1rem; }
  .stApp .sf-carte-texte { min-height: 0; }
}
</style>
"""


def injecter_css() -> None:
    css = (
        _CSS.replace("%INDIGO%", INDIGO)
        .replace("%MILLET%", MILLET)
        .replace("%KOLA%", KOLA)
        .replace("%FEUILLE%", FEUILLE)
        .replace("%AMBRE%", AMBRE)
        .replace("%ENCRE%", ENCRE)
        .replace("%PAPIER%", PAPIER)
        .replace("%BRUME%", BRUME)
    )
    st.markdown(css, unsafe_allow_html=True)


def marque() -> None:
    st.markdown(
        "<div class='sf-marque'>SantéFaso</div><div class='sf-tissage'></div>",
        unsafe_allow_html=True,
    )


def hero(titre_html: str, texte: str) -> None:
    st.markdown(
        f"<div class='sf-hero'><h1>{titre_html}</h1><p>{texte}</p><div class='sf-tissage'></div></div>",
        unsafe_allow_html=True,
    )


def titre_page(titre: str, sous_titre: str = "") -> None:
    st.markdown(f"<h1 class='sf-titre'>{titre}</h1>", unsafe_allow_html=True)
    if sous_titre:
        st.markdown(f"<p class='sf-soustitre'>{sous_titre}</p>", unsafe_allow_html=True)


def note(texte: str) -> None:
    st.markdown(f"<div class='sf-note'>{texte}</div>", unsafe_allow_html=True)


def signal(niveau: str, titre: str) -> None:
    classe = {"urgence": "sf-urgence", "rapide": "sf-rapide", "surveiller": "sf-calme"}[niveau]
    st.markdown(
        f"<div class='sf-signal {classe}'><div class='sf-pastille'></div>"
        f"<div class='sf-signal-titre'>{titre}</div></div>",
        unsafe_allow_html=True,
    )


# Statut du carnet -> (libellé avec symbole, couleur)
STATUTS = {
    vaccins.FAIT: ("✓ Fait", FEUILLE),
    vaccins.EN_RETARD: ("! En retard", KOLA),
    vaccins.A_FAIRE: ("À faire maintenant", AMBRE),
    vaccins.BIENTOT: ("Bientôt", AMBRE),
    vaccins.A_VENIR: ("À venir", "#5A6080"),
}


def frise(lignes) -> None:
    blocs = []
    for l in lignes:
        libelle, couleur = STATUTS[l.statut]
        confirmer = "<small>À confirmer au centre de santé</small>" if l.etape.a_confirmer else ""
        blocs.append(
            f"<div class='sf-etape' style='--c:{couleur}'>"
            f"<div class='sf-etape-titre'>{l.etape.libelle}</div>"
            f"<div class='sf-etape-statut'>{libelle}</div>"
            f"<div class='sf-etape-detail'>Prévu le {l.date_prevue.strftime('%d/%m/%Y')} : "
            f"{', '.join(l.etape.vaccins)}</div>"
            f"<small>Protège contre : {l.etape.maladies}</small>{confirmer}</div>"
        )
    st.markdown(f"<div class='sf-frise'>{''.join(blocs)}</div>", unsafe_allow_html=True)


def prochaine(ligne) -> None:
    libelle, _ = STATUTS[ligne.statut]
    st.markdown(
        f"<div class='sf-prochaine'><div class='sf-prochaine-titre'>{ligne.etape.libelle}</div>"
        f"Prévu le {ligne.date_prevue.strftime('%d/%m/%Y')} ({libelle.lstrip('!✓ ').lower()}) : "
        f"{', '.join(ligne.etape.vaccins)}</div>",
        unsafe_allow_html=True,
    )


def jalons(liste) -> None:
    lignes = "".join(
        f"<div class='sf-jalon'><div class='sf-date'>{d}</div><div>{t}</div></div>" for d, t in liste
    )
    st.markdown(f"<div>{lignes}</div>", unsafe_allow_html=True)
