"""Calendrier vaccinal de l'enfant (Programme élargi de vaccination du Burkina Faso).

Le calendrier est volontairement stocké comme de simples données (liste CALENDRIER)
pour qu'il soit facile à mettre à jour si le Ministère de la Santé le modifie.

Sources consultées : thèse INSSA/UPB 2016 (calendrier de routine du PEV), plan pluriannuel
du PEV, presse nationale (introduction des vaccins contre le paludisme RTS,S puis R21).
Plusieurs documents donnent des âges légèrement différents (8/12/16 semaines ou
6/10/14 semaines pour les trois contacts du nourrisson) : le carnet de santé de l'enfant
et l'agent de santé restent la référence.
"""
from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, timedelta

# Statuts d'une étape
FAIT = "fait"
EN_RETARD = "en_retard"
A_FAIRE = "a_faire"
BIENTOT = "bientot"
A_VENIR = "a_venir"

DELAI_TOLERANCE_JOURS = 14  # marge avant de parler de « retard »
DELAI_BIENTOT_JOURS = 14  # étape annoncée « bientôt » dans les 14 jours


@dataclass(frozen=True)
class Etape:
    id: str
    libelle: str
    vaccins: tuple[str, ...]
    maladies: str
    semaines: int | None = None
    mois: int | None = None
    a_confirmer: bool = False


CALENDRIER: list[Etape] = [
    Etape(
        "naissance",
        "Naissance",
        ("BCG", "Polio oral 0"),
        "Tuberculose, poliomyélite",
        semaines=0,
    ),
    Etape(
        "contact_2",
        "8 semaines (2 mois)",
        ("Pentavalent 1", "Polio oral 1", "Pneumocoque 1", "Rotavirus 1"),
        "Diphtérie, tétanos, coqueluche, hépatite B, Hib, poliomyélite, pneumonie, diarrhée à rotavirus",
        semaines=8,
    ),
    Etape(
        "contact_3",
        "12 semaines (3 mois)",
        ("Pentavalent 2", "Polio oral 2", "Pneumocoque 2", "Rotavirus 2"),
        "Diphtérie, tétanos, coqueluche, hépatite B, Hib, poliomyélite, pneumonie, diarrhée à rotavirus",
        semaines=12,
    ),
    Etape(
        "contact_4",
        "16 semaines (4 mois)",
        ("Pentavalent 3", "Polio oral 3", "Pneumocoque 3", "Rotavirus 3"),
        "Diphtérie, tétanos, coqueluche, hépatite B, Hib, poliomyélite, pneumonie, diarrhée à rotavirus",
        semaines=16,
    ),
    Etape(
        "palu_1",
        "5 mois : paludisme (1re dose)",
        ("Vaccin antipaludique R21 (dose 1)",),
        "Paludisme",
        mois=5,
        a_confirmer=True,
    ),
    Etape(
        "palu_2",
        "6 mois : paludisme (2e dose)",
        ("Vaccin antipaludique R21 (dose 2)",),
        "Paludisme",
        mois=6,
        a_confirmer=True,
    ),
    Etape(
        "palu_3",
        "7 mois : paludisme (3e dose)",
        ("Vaccin antipaludique R21 (dose 3)",),
        "Paludisme (la 4e dose est donnée plus tard, selon l'agent de santé)",
        mois=7,
        a_confirmer=True,
    ),
    Etape(
        "mois_9",
        "9 mois",
        ("Rougeole (VAR)", "Fièvre jaune (VAA)"),
        "Rougeole, fièvre jaune",
        mois=9,
    ),
    Etape(
        "mois_15",
        "15 mois",
        ("Rougeole-Rubéole (RR)",),
        "Rougeole, rubéole",
        mois=15,
    ),
]


def ajouter_mois(d: date, n: int) -> date:
    """Ajoute n mois à une date en gardant un jour valide (31 janv. + 1 mois = 28/29 févr.)."""
    index = d.month - 1 + n
    annee = d.year + index // 12
    mois = index % 12 + 1
    jour = min(d.day, calendar.monthrange(annee, mois)[1])
    return date(annee, mois, jour)


def date_prevue(etape: Etape, naissance: date) -> date:
    if etape.semaines is not None:
        return naissance + timedelta(weeks=etape.semaines)
    if etape.mois is not None:
        return ajouter_mois(naissance, etape.mois)
    raise ValueError(f"Étape sans âge défini : {etape.id}")


@dataclass(frozen=True)
class LigneCarnet:
    etape: Etape
    date_prevue: date
    statut: str
    jours_ecart: int  # >0 : jours de retard ; <0 : jours restants


def _statut(prevue: date, aujourdhui: date, fait: bool) -> tuple[str, int]:
    ecart = (aujourdhui - prevue).days
    if fait:
        return FAIT, ecart
    if ecart > DELAI_TOLERANCE_JOURS:
        return EN_RETARD, ecart
    if ecart >= 0:
        return A_FAIRE, ecart
    if -ecart <= DELAI_BIENTOT_JOURS:
        return BIENTOT, ecart
    return A_VENIR, ecart


def planning(naissance: date, aujourdhui: date, faits: set[str] | None = None) -> list[LigneCarnet]:
    """Construit le carnet vaccinal prévisionnel d'un enfant."""
    faits = faits or set()
    lignes = []
    for etape in CALENDRIER:
        prevue = date_prevue(etape, naissance)
        statut, ecart = _statut(prevue, aujourdhui, etape.id in faits)
        lignes.append(LigneCarnet(etape, prevue, statut, ecart))
    lignes.sort(key=lambda l: l.date_prevue)
    return lignes


def prochaine_etape(lignes: list[LigneCarnet]) -> LigneCarnet | None:
    """Première étape non faite (en retard, à faire maintenant ou à venir)."""
    for ligne in lignes:
        if ligne.statut != FAIT:
            return ligne
    return None


def progression(lignes: list[LigneCarnet]) -> tuple[int, int]:
    """Retourne (nombre d'étapes faites, nombre total d'étapes)."""
    return sum(1 for l in lignes if l.statut == FAIT), len(lignes)


def age_en_texte(naissance: date, aujourdhui: date) -> str:
    jours = (aujourdhui - naissance).days
    if jours < 0:
        return "date de naissance dans le futur"
    if jours < 14:
        return f"{jours} jour(s)"
    if jours < 60:
        return f"{jours // 7} semaines"
    mois = (aujourdhui.year - naissance.year) * 12 + aujourdhui.month - naissance.month
    if aujourdhui.day < naissance.day:
        mois -= 1
    if mois < 24:
        return f"{mois} mois"
    return f"{mois // 12} ans"
