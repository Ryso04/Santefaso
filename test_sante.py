from datetime import date, timedelta

import regles
import vaccins
from regles import Entree, evaluer


# --- Orientation des symptômes ---------------------------------------------
def test_signe_de_danger_donne_urgence():
    r = evaluer(Entree(age=regles.ADULTE, signes_danger={"convulsions"}))
    assert r.niveau == regles.URGENCE


def test_fievre_nourrisson_moins_3_mois_est_urgence():
    r = evaluer(Entree(age=regles.MOINS_3_MOIS, fievre=True))
    assert r.niveau == regles.URGENCE


def test_fievre_enfant_petit_a_consulter_rapidement_et_paludisme():
    r = evaluer(Entree(age=regles.ENFANT_PETIT, fievre=True, duree_jours=1))
    assert r.niveau == regles.RAPIDE
    assert r.paludisme_possible


def test_fievre_adulte_depuis_3_jours_a_consulter():
    r = evaluer(Entree(age=regles.ADULTE, fievre=True, duree_jours=3))
    assert r.niveau == regles.RAPIDE


def test_fievre_adulte_recente_sans_autre_signe_a_surveiller():
    r = evaluer(Entree(age=regles.ADULTE, fievre=True, duree_jours=1))
    assert r.niveau == regles.SURVEILLER
    assert not r.paludisme_possible


def test_fievre_adulte_avec_frissons_a_consulter():
    r = evaluer(Entree(age=regles.ADULTE, fievre=True, duree_jours=1, symptomes={"frissons"}))
    assert r.niveau == regles.RAPIDE


def test_fievre_femme_enceinte_a_consulter():
    r = evaluer(Entree(age=regles.ADULTE, fievre=True, duree_jours=1, enceinte=True))
    assert r.niveau == regles.RAPIDE


def test_diarrhee_jeune_enfant_a_consulter_avec_sro():
    r = evaluer(Entree(age=regles.ENFANT_PETIT, symptomes={"diarrhee"}))
    assert r.niveau == regles.RAPIDE
    assert any("SRO" in c for c in r.conseils)


def test_sang_dans_les_selles_a_consulter():
    r = evaluer(Entree(age=regles.ADULTE, symptomes={"sang_selles"}))
    assert r.niveau == regles.RAPIDE


def test_toux_prolongee_a_consulter():
    r = evaluer(Entree(age=regles.ADULTE, symptomes={"toux"}, duree_jours=15))
    assert r.niveau == regles.RAPIDE


def test_aucun_symptome_a_surveiller():
    r = evaluer(Entree(age=regles.ADULTE))
    assert r.niveau == regles.SURVEILLER
    assert r.raisons


def test_niveau_ne_descend_jamais_avec_un_signe_de_danger():
    r = evaluer(Entree(age=regles.ADULTE, fievre=True, duree_jours=1, signes_danger={"somnolence"}))
    assert r.niveau == regles.URGENCE


# --- Carnet vaccinal --------------------------------------------------------
def test_ajouter_mois_fin_de_mois():
    assert vaccins.ajouter_mois(date(2026, 1, 31), 1) == date(2026, 2, 28)
    assert vaccins.ajouter_mois(date(2024, 1, 31), 1) == date(2024, 2, 29)
    assert vaccins.ajouter_mois(date(2026, 11, 12), 9) == date(2027, 8, 12)


def test_dates_prevues_en_semaines():
    naissance = date(2026, 1, 1)
    ids = {e.id: vaccins.date_prevue(e, naissance) for e in vaccins.CALENDRIER}
    assert ids["naissance"] == date(2026, 1, 1)
    assert ids["contact_2"] == date(2026, 2, 26)  # +8 semaines
    assert ids["mois_9"] == date(2026, 10, 1)


def test_nouveau_ne_naissance_a_faire_et_reste_a_venir():
    jour = date(2026, 11, 12)
    lignes = {l.etape.id: l for l in vaccins.planning(jour, jour)}
    assert lignes["naissance"].statut == vaccins.A_FAIRE
    assert lignes["contact_2"].statut == vaccins.A_VENIR


def test_retard_detecte_puis_fait():
    naissance = date(2026, 1, 1)
    aujourdhui = date(2026, 6, 1)
    lignes = {l.etape.id: l for l in vaccins.planning(naissance, aujourdhui)}
    assert lignes["contact_2"].statut == vaccins.EN_RETARD
    lignes = {l.etape.id: l for l in vaccins.planning(naissance, aujourdhui, {"contact_2"})}
    assert lignes["contact_2"].statut == vaccins.FAIT


def test_tolerance_avant_de_parler_de_retard():
    naissance = date(2026, 1, 1)
    prevue = vaccins.date_prevue(vaccins.CALENDRIER[1], naissance)
    lignes = {l.etape.id: l for l in vaccins.planning(naissance, prevue + timedelta(days=5))}
    assert lignes["contact_2"].statut == vaccins.A_FAIRE


def test_prochaine_etape_ignore_les_faites():
    naissance = date(2026, 1, 1)
    lignes = vaccins.planning(naissance, date(2026, 1, 2), {"naissance"})
    suivante = vaccins.prochaine_etape(lignes)
    assert suivante.etape.id == "contact_2"


def test_progression():
    naissance = date(2026, 1, 1)
    lignes = vaccins.planning(naissance, date(2026, 6, 1), {"naissance", "contact_2"})
    faits, total = vaccins.progression(lignes)
    assert faits == 2
    assert total == len(vaccins.CALENDRIER)


def test_contenus_sources_et_donnees():
    import contenu

    assert contenu.nb(11_656_675) == "11 656 675"
    assert all(url.startswith("https://") for _, url in contenu.SOURCES)
    assert all(0 < valeur <= 100 for _, valeur in contenu.COUVERTURE_CHUSS)
    # la couverture baisse au fil du calendrier
    valeurs = [v for _, v in contenu.COUVERTURE_CHUSS]
    assert valeurs == sorted(valeurs, reverse=True)


def test_age_en_texte():
    assert vaccins.age_en_texte(date(2026, 11, 1), date(2026, 11, 12)) == "11 jour(s)"
    assert vaccins.age_en_texte(date(2026, 8, 12), date(2026, 11, 12)) == "3 mois"
    assert vaccins.age_en_texte(date(2023, 11, 12), date(2026, 11, 12)) == "3 ans"
