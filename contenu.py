"""Contenus factuels et textes de présentation de SantéFaso.

Les chiffres viennent de sources publiques citées dans SOURCES. Rien n'est inventé :
quand une donnée est ancienne ou limitée à un hôpital, le texte le dit.
"""

# Paludisme au Burkina Faso, année 2022 (Gavi, d'après les données nationales)
PALU_2022 = {"cas": 11_656_675, "graves": 539_488, "deces": 4_243, "deces_moins_5": 2_925}

# Couverture vaccinale par étape, enfants de moins de 5 ans disposant d'un carnet,
# CHU Sourô Sanou de Bobo-Dioulasso, étude du 1er juin au 31 août 2014 (thèse INSSA 2016).
COUVERTURE_CHUSS = [
    ("Naissance : BCG, polio 0", 96.38),
    ("2 mois : 1res doses", 94.62),
    ("3 mois : 2es doses", 91.77),
    ("4 mois : 3es doses", 86.64),
    ("9 mois : rougeole, fièvre jaune", 78.31),
]

# Le calendrier évolue : raison pour laquelle il est stocké comme des données.
JALONS_PEV = [
    ("Fin 2013", "Le vaccin contre le pneumocoque et celui contre le rotavirus entrent dans le calendrier de routine."),
    ("26 avril 2022", "Le vaccin contre le papillomavirus humain (cancer du col de l'utérus) est introduit."),
    ("5 février 2024", "Début du vaccin antipaludique RTS,S, dans certaines régions."),
    ("15 août 2025", "Passage à l'échelle avec le vaccin antipaludique R21, pour les enfants de 5 à 23 mois."),
]

FAQ = [
    (
        "Mon enfant a de la fièvre. Dois-je attendre ?",
        "Non. Chez un enfant de moins de 5 ans, toute fièvre doit être vue dans un centre de santé, "
        "où un test rapide permet de savoir s'il s'agit du paludisme. Si l'enfant convulse, ne boit plus "
        "ou est très endormi, c'est une urgence.",
    ),
    (
        "Mon enfant a pris du retard dans ses vaccins. Faut-il tout recommencer ?",
        "En général non. Les doses manquantes sont données au plus tôt, sans reprendre depuis le début. "
        "Présentez-vous au centre de santé avec le carnet.",
    ),
    (
        "Que faire si je n'ai plus le carnet de santé ?",
        "Allez au centre de santé où l'enfant a été vacciné : le registre du centre peut permettre "
        "de retrouver les vaccins déjà reçus. Dans l'étude de l'hôpital de Bobo-Dioulasso, un enfant sur "
        "deux n'avait pas son carnet : le garder en lieu sûr change beaucoup de choses.",
    ),
    (
        "Une petite fièvre après un vaccin est-elle normale ?",
        "Oui, une fièvre légère ou une douleur à l'endroit de l'injection est fréquente. "
        "Si la réaction est importante ou dure, consultez.",
    ),
    (
        "Le vaccin contre le paludisme remplace-t-il la moustiquaire ?",
        "Non. Les agents de santé insistent sur le fait que le vaccin s'ajoute aux autres moyens de "
        "prévention : moustiquaire imprégnée, chimioprévention saisonnière, suppression des eaux stagnantes.",
    ),
]

# Page de présentation du projet (soutenance)
PROJET = [
    {
        "titre": "Le problème",
        "paragraphes": [
            "Le paludisme reste une cause majeure de maladie chez les jeunes enfants : en 2022, le Burkina Faso "
            "a enregistré plus de 11,6 millions de cas, dont plus de 539 000 cas graves, et 4 243 décès dont "
            "2 925 enfants de moins de 5 ans.",
            "Côté vaccination, l'étude menée à l'hôpital Sourô Sanou de Bobo-Dioulasso montre que la protection "
            "diminue à chaque étape du calendrier : de 96 % à la naissance à 78 % à 9 mois. Les familles citent "
            "le manque d'information, l'oubli, l'état de santé de l'enfant et l'accueil dans les centres.",
        ],
    },
    {
        "titre": "La solution",
        "puces": [
            "**Orientation des symptômes** : un questionnaire court dit s'il faut aller en urgence, consulter vite "
            "ou surveiller, avec les raisons et les gestes à faire.",
            "**Carnet vaccinal** : à partir de la date de naissance, les dates prévues, les retards et la prochaine "
            "étape sont calculés automatiquement.",
            "**Prévention** : des conseils clairs pour le paludisme, l'eau, la diarrhée, la vaccination et la grossesse.",
        ],
    },
    {
        "titre": "Ce qui rend le projet différent",
        "puces": [
            "Orientation et suivi vaccinal réunis dans un seul outil gratuit, en français, sans compte à créer.",
            "Des règles écrites en clair, testées automatiquement, qui choisissent toujours le niveau le plus prudent.",
            "Un calendrier vaccinal stocké comme des données : quand le programme change, une ligne suffit "
            "(le vaccin R21 a par exemple été étendu à l'échelle en août 2025).",
            "Aucune donnée personnelle enregistrée : l'outil fonctionne sans base de données.",
        ],
    },
    {
        "titre": "À qui il s'adresse",
        "puces": [
            "Parents et futurs parents.",
            "Femmes enceintes.",
            "Relais communautaires et agents de santé, comme aide-mémoire pour accompagner les familles.",
        ],
    },
    {
        "titre": "Limites et responsabilité",
        "puces": [
            "SantéFaso ne pose aucun diagnostic et ne remplace pas une consultation.",
            "Les âges du calendrier doivent être validés avec le Programme élargi de vaccination : les sources "
            "consultées donnent 8, 12 et 16 semaines ou 6, 10 et 14 semaines selon les documents.",
            "L'outil n'a pas encore été testé auprès de familles ni relu par un professionnel de santé.",
        ],
    },
    {
        "titre": "Feuille de route",
        "puces": [
            "**Avant tout déploiement** : relecture des règles par un médecin ou un infirmier, test auprès d'une "
            "dizaine de parents.",
            "**Ensuite** : versions en dioula, mooré et fulfuldé, avec lecture audio pour les personnes qui lisent peu.",
            "**Puis** : rappels par SMS, annuaire des centres de santé par commune, partenariat avec un district sanitaire.",
        ],
    },
    {
        "titre": "Choix techniques",
        "puces": [
            "Python et Streamlit : une application web qui s'ouvre sur un téléphone, sans installation.",
            "Logique séparée de l'interface (règles, calendrier, contenus) et 20 tests automatiques.",
            "Déploiement gratuit sur Streamlit Community Cloud.",
        ],
    },
]

SOURCES = [
    (
        "Gavi : comment le vaccin RTS,S transforme la lutte contre le paludisme au Burkina Faso",
        "https://www.gavi.org/fr/vaccineswork/comment-vaccin-rtss-transforme-lutte-paludisme-burkina-faso",
    ),
    (
        "Thèse INSSA / UPB 2016 : couverture vaccinale du PEV des enfants de 2 à 60 mois au CHU Sourô Sanou",
        "https://beep.ird.fr/collect/upb/index/assoc/INSSA-2016-TAG-ETU/INSSA-2016-TAG-ETU.pdf",
    ),
    (
        "Sidwaya (10 novembre 2025) : le vaccin R21, un nouveau rempart pour les nourrissons",
        "https://www.sidwaya.info/2025/11/10/lutte-contre-le-paludisme-le-r21-un-nouveau-rempart-pour-les-nourrissons/",
    ),
    (
        "Gavi : le Burkina Faso engagé pour vaincre le cancer du col de l'utérus",
        "https://www.gavi.org/fr/vaccineswork/burkina-faso-engage-vaincre-cancer-col-uterus",
    ),
    (
        "OMS Afrique : introduction des vaccins Rotateq et PCV13 dans le PEV (2013)",
        "https://www.afro.who.int/node/4606",
    ),
]


def nb(n: int) -> str:
    """Formate un entier à la française : 11 656 675."""
    return f"{n:,}".replace(",", " ")
