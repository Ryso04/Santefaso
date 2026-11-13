"""Règles d'orientation des symptômes de SantéFaso.

IMPORTANT : ce module est une aide à la décision, pas un diagnostic médical.
Les règles s'inspirent des « signes généraux de danger » de la prise en charge
intégrée des maladies de l'enfant (PCIME / IMCI) de l'OMS. En cas de doute, la
règle choisit toujours le niveau le plus prudent.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# --- Niveaux d'alerte -------------------------------------------------------
URGENCE = "urgence"
RAPIDE = "rapide"
SURVEILLER = "surveiller"

ORDRE = {SURVEILLER: 0, RAPIDE: 1, URGENCE: 2}

# --- Tranches d'âge ---------------------------------------------------------
MOINS_3_MOIS = "moins_3_mois"
ENFANT_PETIT = "3_mois_5_ans"
ENFANT = "5_15_ans"
ADULTE = "adulte"

TRANCHES_AGE = {
    MOINS_3_MOIS: "Moins de 3 mois",
    ENFANT_PETIT: "3 mois à 5 ans",
    ENFANT: "5 à 15 ans",
    ADULTE: "Adulte (plus de 15 ans)",
}

# --- Signes de danger : un seul suffit pour déclencher l'urgence -----------
SIGNES_DANGER = {
    "convulsions": "Convulsions (tremblements avec perte de connaissance)",
    "somnolence": "Très endormi, difficile à réveiller ou inconscient",
    "ne_peut_pas_boire": "Ne peut pas boire, manger ou téter",
    "vomit_tout": "Vomit tout ce qu'il ou elle absorbe",
    "respiration": "Respiration difficile ou très rapide",
    "raideur_nuque": "Raideur de la nuque",
    "saignement": "Saignement anormal",
    "pale_jaune": "Très pâle ou peau/yeux jaunes",
}

# --- Autres symptômes -------------------------------------------------------
SYMPTOMES = {
    "frissons": "Frissons",
    "maux_tete": "Maux de tête",
    "courbatures": "Courbatures, douleurs du corps",
    "vomissements": "Vomissements",
    "diarrhee": "Diarrhée",
    "sang_selles": "Sang dans les selles",
    "toux": "Toux",
    "eruption": "Éruption sur la peau",
}

SYMPTOMES_PALU = {"frissons", "maux_tete", "courbatures", "vomissements"}


@dataclass
class Entree:
    """Réponses saisies par l'utilisateur."""

    age: str = ENFANT_PETIT
    fievre: bool = False
    duree_jours: int = 0
    symptomes: set[str] = field(default_factory=set)
    signes_danger: set[str] = field(default_factory=set)
    enceinte: bool = False


@dataclass
class Resultat:
    niveau: str
    titre: str
    raisons: list[str]
    conseils: list[str]
    paludisme_possible: bool = False


def _monter(actuel: str, nouveau: str) -> str:
    """Retourne le niveau le plus élevé des deux."""
    return nouveau if ORDRE[nouveau] > ORDRE[actuel] else actuel


def evaluer(e: Entree) -> Resultat:
    niveau = SURVEILLER
    raisons: list[str] = []
    paludisme = False

    # 1. Signes de danger -> urgence immédiate
    if e.signes_danger:
        niveau = _monter(niveau, URGENCE)
        for cle in sorted(e.signes_danger):
            raisons.append(f"Signe de danger : {SIGNES_DANGER.get(cle, cle).lower()}")

    # 2. Nourrisson de moins de 3 mois avec fièvre -> urgence
    if e.age == MOINS_3_MOIS and e.fievre:
        niveau = _monter(niveau, URGENCE)
        raisons.append("Fièvre chez un nourrisson de moins de 3 mois : risque d'infection grave.")

    # 3. Fièvre
    if e.fievre:
        paludisme = True
        niveau = _monter(niveau, RAPIDE)
        raisons.append(
            "Toute fièvre doit être testée pour le paludisme (test de diagnostic rapide) "
            "dans un centre de santé."
        )
        if e.age == ENFANT_PETIT:
            raisons.append("Fièvre chez un enfant de moins de 5 ans : il faut consulter sans tarder.")
        if e.enceinte:
            raisons.append("Fièvre chez une femme enceinte : le paludisme est plus grave pendant la grossesse.")
        if e.duree_jours >= 2:
            raisons.append(f"Fièvre depuis {e.duree_jours} jours : ce n'est plus à surveiller seul à la maison.")
        if e.symptomes & SYMPTOMES_PALU:
            raisons.append("Fièvre associée à des signes évocateurs du paludisme (frissons, maux de tête, courbatures, vomissements).")
        # Fièvre récente, adulte ou grand enfant, sans autre signe : on peut surveiller
        elif (
            e.age in (ENFANT, ADULTE)
            and e.duree_jours < 2
            and not e.enceinte
            and not e.signes_danger
            and not e.symptomes
        ):
            niveau = SURVEILLER
            paludisme = False
            raisons = [
                "Fièvre récente (moins de 2 jours) sans autre signe : à surveiller de près. "
                "Consultez si elle persiste ou si d'autres signes apparaissent."
            ]

    # 4. Diarrhée
    if "sang_selles" in e.symptomes:
        niveau = _monter(niveau, RAPIDE)
        raisons.append("Sang dans les selles : il faut consulter.")
    if "diarrhee" in e.symptomes:
        if e.age in (MOINS_3_MOIS, ENFANT_PETIT):
            niveau = _monter(niveau, RAPIDE)
            raisons.append("Diarrhée chez un jeune enfant : risque de déshydratation rapide.")
        elif e.duree_jours >= 3:
            niveau = _monter(niveau, RAPIDE)
            raisons.append(f"Diarrhée depuis {e.duree_jours} jours : il faut consulter.")

    # 5. Toux prolongée
    if "toux" in e.symptomes and e.duree_jours >= 14:
        niveau = _monter(niveau, RAPIDE)
        raisons.append("Toux depuis plus de 2 semaines : il faut la faire examiner.")

    # 6. Éruption avec fièvre
    if "eruption" in e.symptomes and e.fievre:
        niveau = _monter(niveau, RAPIDE)
        raisons.append("Éruption avec fièvre : il faut consulter (la rougeole est possible).")

    # Titre et conseils selon le niveau
    if niveau == URGENCE:
        titre = "Urgence : rendez-vous immédiatement dans un centre de santé"
        conseils = [
            "Ne perdez pas de temps : allez au centre de santé ou à l'hôpital le plus proche, ou appelez les secours.",
            "Si la personne convulse ou est inconsciente, ne lui donnez rien à boire ni à manger.",
            "Emportez le carnet de santé et notez depuis quand les signes sont apparus.",
        ]
    elif niveau == RAPIDE:
        titre = "À consulter rapidement (aujourd'hui ou dans les 24 heures)"
        conseils = [
            "Rendez-vous dans un centre de santé : un agent de santé pourra faire un test et vous orienter.",
            "Faites boire souvent (eau propre) et continuez l'allaitement ou l'alimentation.",
            "Ne prenez pas de médicaments sans avis d'un agent de santé.",
        ]
        if "diarrhee" in e.symptomes:
            conseils.append("En cas de diarrhée : donnez des solutions de réhydratation orale (SRO) disponibles au centre de santé ou en pharmacie.")
    else:
        titre = "À surveiller à la maison"
        conseils = [
            "Reposez-vous et buvez suffisamment d'eau propre.",
            "Surveillez l'évolution pendant 24 à 48 heures.",
            "Consultez si de la fièvre apparaît, si les symptômes durent ou s'aggravent.",
        ]
        if not raisons:
            raisons.append("Aucun signe de gravité détecté dans les réponses fournies.")

    return Resultat(
        niveau=niveau,
        titre=titre,
        raisons=raisons,
        conseils=conseils,
        paludisme_possible=paludisme,
    )
