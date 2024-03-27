import typing


CINEMA_PROVIDER_NAMES = [
    "CDSStocks",
    "BoostStocks",
    "CGRStocks",
    "EMSStocks",
]

ALLOCINE_PRODUCTS_PROVIDER_NAME = "Allocine Products"

PASS_CULTURE_STOCKS_FAKE_CLASS_NAME = "PCAPIStocks"
EMS_STOCKS_FAKE_CLASS_NAME = "EMSStocks"

TITELIVE_EPAGINE_PROVIDER_NAME = "TiteLive API Epagine"

TITELIVE_MUSIC_GENRES_BY_GTL_ID: dict[str, str] = {
    "01000000": "MUSIQUE_CLASSIQUE",
    "02000000": "JAZZ-BLUES",
    "03000000": "BANDES_ORIGINALES",
    "04000000": "ELECTRO",
    "05000000": "POP",
    "06000000": "ROCK",
    "07000000": "METAL",
    "08000000": "ALTERNATIF",
    "09000000": "VARIETES",
    "10000000": "FUNK-SOUL-RNB-DISCO",
    "11000000": "RAP-HIP HOP",
    "12000000": "REGGAE-RAGGA",
    "13000000": "MUSIQUE_DU_MONDE",
    "14000000": "COUNTRY-FOLK",
    "15000000": "VIDEOS_MUSICALES",
    "16000000": "COMPILATIONS",
    "17000000": "AMBIANCE",
    "18000000": "ENFANTS",
    "19000000": "AUTRES",
}

GTL_ID_BY_TITELIVE_MUSIC_GENRE: dict[str, str] = {v: k for k, v in TITELIVE_MUSIC_GENRES_BY_GTL_ID.items()}

GTL_IDS_BY_MUSIC_GENRE_CODE: dict[int, str] = {
    501: "02010000",
    520: "02050000",
    530: "12000000",
    600: "01000000",
    700: "13000000",
    800: "05000000",
    820: "06000000",
    840: "07000000",
    850: "08010000",
    860: "14000000",
    870: "14000000",
    880: "04000000",
    900: "11000000",
    930: "02060000",
    1000: "09000000",
    -1: "19000000",
}

MUSIC_SLUG_BY_GTL_ID: dict[str, str] = {
    "01000000": "CLASSIQUE-OTHER",
    "01010000": "CLASSIQUE-MEDIEVALE",
    "01020000": "CLASSIQUE-OTHER",
    "01030000": "CLASSIQUE-OTHER",
    "01040000": "CLASSIQUE-OTHER",
    "01050000": "CLASSIQUE-BAROQUE",
    "01060000": "CLASSIQUE-OTHER",
    "01070000": "CLASSIQUE-OTHER",
    "01080000": "CLASSIQUE-OTHER",
    "01090000": "CLASSIQUE-OPERA",
    "01100000": "CLASSIQUE-OTHER",
    "01110000": "CLASSIQUE-CHANT",
    "01120000": "CLASSIQUE-CONTEMPORAIN",
    "02000000": "JAZZ-OTHER",
    "02010000": "JAZZ-TRADITIONEL",
    "02020000": "JAZZ-VOCAL_JAZZ",
    "02030000": "JAZZ-JAZZ_CONTEMPORAIN",
    "02040000": "JAZZ-FUSION",
    "02050000": "BLUES-BLUES_ROCK",
    "02060000": "GOSPEL-TRADITIONAL_GOSPEL",
    "02070000": "JAZZ-MANOUCHE",
    "03000000": "OTHER",
    "04000000": "ELECTRO-OTHER",
    "04010000": "ELECTRO-ELECTRONICA",
    "04020000": "ELECTRO-TECHNO",
    "04030000": "ELECTRO-HOUSE",
    "04040000": "ELECTRO-OTHER",
    "04050000": "ELECTRO-LOUNGE",
    "04060000": "ELECTRO-DRUM_AND_BASS",
    "04070000": "ELECTRO-DANCE",
    "05000000": "POP-OTHER",
    "05010000": "POP-POP_ROCK",
    "05020000": "POP-OTHER",
    "05030000": "POP-BRITPOP",
    "05040000": "POP-OTHER",
    "05050000": "POP-ELECTRO_POP",
    "05060000": "POP-OTHER",
    "05070000": "POP-OTHER",
    "05080000": "POP-K_POP",
    "05090000": "POP-OTHER",
    "06000000": "ROCK-OTHER",
    "06010000": "ROCK-ARENA_ROCK",
    "06030000": "ROCK-ROCK_N_ROLL",
    "06040000": "ROCK-PSYCHEDELIC",
    "06050000": "ROCK-PROG_ROCK",
    "07000000": "METAL-OTHER",
    "07010000": "METAL-BLACK_METAL",
    "07020000": "METAL-FUSION",
    "07030000": "METAL-FUSION",
    "07040000": "METAL-DEATH_METAL",
    "08000000": "PUNK-OTHER",
    "08010000": "PUNK-HARDCORE_PUNK",
    "08020000": "PUNK-HARDCORE_PUNK",
    "08030000": "ROCK-INDIE_ROCK",
    "08040000": "ROCK-INDIE_ROCK",
    "08050000": "METAL-GOTHIC",
    "08060000": "METAL-METAL_INDUSTRIEL",
    "08070000": "ROCK-GRUNGE",
    "08080000": "ROCK-EXPERIMENTAL",
    "09000000": "CHANSON_VARIETE-OTHER",
    "09010000": "CHANSON_VARIETE-CHANSON_À_TEXTE",
    "09020000": "CHANSON_VARIETE-CHANSON_FRANCAISE",
    "09030000": "CHANSON_VARIETE-MUSIC_HALL",
    "09040000": "CHANSON_VARIETE-FOLKLORE_FRANCAIS",
    "09050000": "CHANSON_VARIETE-CHANSON_À_TEXTE",
    "09060000": "CHANSON_VARIETE-CHANSON_À_TEXTE",
    "10000000": "HIP_HOP_RAP-SOUL",
    "10010000": "HIP_HOP_RAP-SOUL",
    "10020000": "HIP_HOP_RAP-SOUL",
    "10030000": "HIP_HOP_RAP-FUNK",
    "10040000": "HIP_HOP_RAP-FUNK",
    "10050000": "MUSIQUE_DU_MONDE-AFRO_BEAT",
    "10060000": "HIP_HOP_RAP-R&B_CONTEMPORAIN",
    "10070000": "HIP_HOP_RAP-R&B_CONTEMPORAIN",
    "10080000": "HIP_HOP_RAP-DISCO",
    "10090000": "HIP_HOP_RAP-DISCO",
    "11000000": "HIP_HOP_RAP-OTHER",
    "11010000": "HIP_HOP_RAP-RAP_OLD_SCHOOL",
    "11020000": "HIP_HOP_RAP-HIP_HOP",
    "11030000": "HIP_HOP_RAP-HIP_HOP",
    "11040000": "HIP_HOP_RAP-RAP_FRANCAIS",
    "11050000": "HIP_HOP_RAP-OTHER",
    "12000000": "REGGAE-ROOTS",
    "12010000": "REGGAE-ROOTS",
    "12020000": "REGGAE-ROOTS",
    "12030000": "REGGAE-ZOUK",
    "12040000": "REGGAE-DUB",
    "12050000": "REGGAE-SKA",
    "12060000": "REGGAE-DANCEHALL",
    "13000000": "MUSIQUE_DU_MONDE-OTHER",
    "13010000": "MUSIQUE_DU_MONDE-OTHER",
    "13020000": "MUSIQUE_DU_MONDE-MOYEN_ORIENT",
    "13030000": "MUSIQUE_DU_MONDE-AFRICAINE",
    "13040000": "MUSIQUE_DU_MONDE-CARIBEENNE",
    "13050000": "MUSIQUE_DU_MONDE-AMERIQUE_DU_NORD",
    "13060000": "MUSIQUE_DU_MONDE-AMERIQUE_DU_SUD",
    "13070000": "MUSIQUE_DU_MONDE-ASIATIQUE",
    "13080000": "MUSIQUE_DU_MONDE-ALTERNATIVO",
    "13090000": "MUSIQUE_DU_MONDE-CELTIQUE",
    "13100000": "MUSIQUE_DU_MONDE-POP_LATINO",
    "13110000": "MUSIQUE_DU_MONDE-SALSA",
    "14000000": "COUNTRY-OTHER",
    "14010000": "COUNTRY-AMERICANA",
    "14020000": "COUNTRY-COUNTRY_ALTERNATIVE",
    "14030000": "FOLK-FOLK_ROCK",
    "14040000": "FOLK-FOLK_ROCK",
    "14050000": "COUNTRY-BLUEGRASS",
    "15000000": "OTHER",
    "16000000": "OTHER",
    "16020000": "POP-OTHER",
    "16030000": "ROCK-OTHER",
    "16040000": "CHANSON_VARIETE-CHANSON_FRANCAISE",
    "16050000": "POP-OTHER",
    "16060000": "JAZZ-OTHER",
    "16070000": "HIP_HOP_RAP-OTHER",
    "16080000": "HIP_HOP_RAP-OTHER",
    "16090000": "REGGAE-OTHER",
    "16100000": "ELECTRO-OTHER",
    "16110000": "MUSIQUE_DU_MONDE-OTHER",
    "17000000": "OTHER",
    "17040000": "CHANSON_VARIETE-FOLKLORE_FRANCAIS",
    "17050000": "CHANSON_VARIETE-FOLKLORE_FRANCAIS",
    "17080000": "CHANSON_VARIETE-FOLKLORE_FRANCAIS",
    "18000000": "OTHER",
    "18010000": "CHANSON_VARIETE-FOLKLORE_FRANCAIS",
    "19000000": "OTHER",
}

MUSIC_SLUG_TO_GTL_ID = {
    "JAZZ-ACID_JAZZ": "02000000",
    "JAZZ-AVANT_GARDE_JAZZ": "02000000",
    "JAZZ-BEBOP": "02000000",
    "JAZZ-BIG_BAND": "02000000",
    "JAZZ-BLUE_NOTE": "02000000",
    "JAZZ-COOL_JAZZ": "02000000",
    "JAZZ-CROSSOVER_JAZZ": "02000000",
    "JAZZ-DIXIELAND": "02000000",
    "JAZZ-JAZZ_FUNK": "02000000",
    "JAZZ-MAINSTREAM": "02000000",
    "JAZZ-RAGTIME": "02000000",
    "JAZZ-SMOOTH": "02000000",
    "JAZZ-ETHIO_JAZZ": "02000000",
    "JAZZ-FUSION": "02000000",
    "JAZZ-JAZZ_CONTEMPORAIN": "02000000",
    "JAZZ-MANOUCHE": "02000000",
    "JAZZ-TRADITIONEL": "02000000",
    "JAZZ-VOCAL_JAZZ": "02000000",
    "JAZZ-OTHER": "02000000",
    "BLUES-BLUES_ACOUSTIQUE": "02000000",
    "BLUES-BLUES_CONTEMPORAIN": "02000000",
    "BLUES-BLUES_ELECTRIQUE": "02000000",
    "BLUES-CHICAGO_BLUES": "02000000",
    "BLUES-CLASSIC_BLUES": "02000000",
    "BLUES-COUNTRY_BLUES": "02000000",
    "BLUES-DELTA_BLUES": "02000000",
    "BLUES-RAGTIME": "02000000",
    "BLUES-OTHER": "02000000",
    "BLUES-BLUES_ROCK": "02000000",
    "REGGAE-TWO_TONE": "12000000",
    "REGGAE-DANCEHALL": "12000000",
    "REGGAE-DUB": "12000000",
    "REGGAE-ROOTS": "12000000",
    "REGGAE-SKA": "12000000",
    "REGGAE-ZOUK": "12000000",
    "REGGAE-OTHER": "12000000",
    "CLASSIQUE-AVANT_GARDE": "01100000",
    "CLASSIQUE-CHORALE": "01000000",
    "CLASSIQUE-EXPRESSIONISTE": "01000000",
    "CLASSIQUE-IMPRESSIONISTE": "01000000",
    "CLASSIQUE-MINIMALISTE": "01100000",
    "CLASSIQUE-MODERNE": "01100000",
    "CLASSIQUE-ORATORIO": "01000000",
    "CLASSIQUE-RENAISSANCE": "01000000",
    "CLASSIQUE-ROMANTIQUE": "01000000",
    "CLASSIQUE-BAROQUE": "01000000",
    "CLASSIQUE-CHANT": "01000000",
    "CLASSIQUE-CONTEMPORAIN": "01000000",
    "CLASSIQUE-MEDIEVALE": "01000000",
    "CLASSIQUE-OPERA": "01000000",
    "CLASSIQUE-OTHER": "01000000",
    "MUSIQUE_DU_MONDE-AFRO_POP": "13000000",
    "MUSIQUE_DU_MONDE-BALADAS_Y_BOLEROS": "13000000",
    "MUSIQUE_DU_MONDE-BOSSA_NOVA": "13000000",
    "MUSIQUE_DU_MONDE-BRESILIENNE": "13000000",
    "MUSIQUE_DU_MONDE-CAJUN": "13000000",
    "MUSIQUE_DU_MONDE-CALYPSO": "13000000",
    "MUSIQUE_DU_MONDE-CUMBIA": "13000000",
    "MUSIQUE_DU_MONDE-FLAMENCO": "13000000",
    "MUSIQUE_DU_MONDE-GRECQUE": "13000000",
    "MUSIQUE_DU_MONDE-INDIENNE": "13000000",
    "MUSIQUE_DU_MONDE-LATIN_JAZZ": "13000000",
    "MUSIQUE_DU_MONDE-LATINE_CONTEMPORAINE": "13000000",
    "MUSIQUE_DU_MONDE-NUEVO_FLAMENCO": "13000000",
    "MUSIQUE_DU_MONDE-PORTUGUESE_FADO": "13000000",
    "MUSIQUE_DU_MONDE-RAI": "13000000",
    "MUSIQUE_DU_MONDE-TANGO_ARGENTIN": "13000000",
    "MUSIQUE_DU_MONDE-YIDDISH": "13000000",
    "MUSIQUE_DU_MONDE-AFRICAINE": "13000000",
    "MUSIQUE_DU_MONDE-AFRO_BEAT": "13000000",
    "MUSIQUE_DU_MONDE-ALTERNATIVO": "13000000",
    "MUSIQUE_DU_MONDE-AMERIQUE_DU_NORD": "13000000",
    "MUSIQUE_DU_MONDE-AMERIQUE_DU_SUD": "1300000",
    "MUSIQUE_DU_MONDE-ASIATIQUE": "13000000",
    "MUSIQUE_DU_MONDE-CARIBEENNE": "13000000",
    "MUSIQUE_DU_MONDE-CELTIQUE": "13000000",
    "MUSIQUE_DU_MONDE-MOYEN_ORIENT": "13000000",
    "MUSIQUE_DU_MONDE-POP_LATINO": "13000000",
    "MUSIQUE_DU_MONDE-SALSA": "13000000",
    "MUSIQUE_DU_MONDE-OTHER": "13000000",
    "POP-BUBBLEGUM": "05000000",
    "POP-DANCE_POP": "05000000",
    "POP-DREAM_POP": "05000000",
    "POP-INDIE_POP": "05000000",
    "POP-J_POP": "05000000",
    "POP-POP_PUNK": "05000000",
    "POP-POWER_POP": "05000000",
    "POP-SOFT_ROCK": "05000000",
    "POP-SYNTHPOP": "05000000",
    "POP-TEEN_POP": "05000000",
    "POP-BRITPOP": "05000000",
    "POP-ELECTRO_POP": "05000000",
    "POP-K_POP": "05000000",
    "POP-POP_ROCK": "05000000",
    "POP-OTHER": "05000000",
    "ROCK-ACID_ROCK": "06000000",
    "ROCK-ART_ROCK": "06000000",
    "ROCK-COLLEGE_ROCK": "06000000",
    "ROCK-GLAM_ROCK": "06000000",
    "ROCK-HARD_ROCK": "06000000",
    "ROCK-LO_FI": "06000000",
    "ROCK-ROCKABILLY": "06000000",
    "ROCK-SHOEGAZE": "06000000",
    "ROCK-ELECTRO": "06000000",
    "ROCK-ARENA_ROCK": "06000000",
    "ROCK-GRUNGE": "06000000",
    "ROCK-INDIE_ROCK": "06000000",
    "ROCK-PROG_ROCK": "06000000",
    "ROCK-PSYCHEDELIC": "06000000",
    "ROCK-ROCK_N_ROLL": "06000000",
    "ROCK-EXPERIMENTAL": "06000000",
    "ROCK-OTHER": "06000000",
    "METAL-DOOM_METAL": "07000000",
    "METAL-METAL_CORE": "07000000",
    "METAL-METAL_PROGRESSIF": "07000000",
    "METAL-TRASH_METAL": "07000000",
    "METAL-OTHER": "07000000",
    "METAL-BLACK_METAL": "07000000",
    "METAL-DEATH_METAL": "07000000",
    "METAL-GOTHIC": "08000000",
    "METAL-METAL_INDUSTRIEL": "08000000",
    "METAL-FUSION": "07000000",
    "PUNK-POST_PUNK": "08000000",
    "PUNK-AFRO_PUNK": "08000000",
    "PUNK-GRINDCORE": "08000000",
    "PUNK-NOISE_ROCK": "08000000",
    "PUNK-HARDCORE_PUNK": "08000000",
    "PUNK-OTHER": "08000000",
    "FOLK-FOLK_CONTEMPORAINE": "14000000",
    "FOLK-INDIE_FOLK": "14000000",
    "FOLK-NEW_ACOUSTIC": "14000000",
    "FOLK-FOLK_TRADITIONELLE": "14000000",
    "FOLK-TEX_MEX": "14000000",
    "FOLK-OTHER": "14000000",
    "FOLK-FOLK_ROCK": "14000000",
    "COUNTRY-COUNTRY_CONTEMPORAINE": "14000000",
    "COUNTRY-GOSPEL_COUNTRY": "14000000",
    "COUNTRY-COUNTRY_POP": "14000000",
    "COUNTRY-OTHER": "14000000",
    "COUNTRY-COUNTRY_ALTERNATIVE": "14000000",
    "COUNTRY-AMERICANA": "14000000",
    "COUNTRY-BLUEGRASS": "14000000",
    "ELECTRO-BITPOP": "04000000",
    "ELECTRO-BREAKBEAT": "04000000",
    "ELECTRO-CHILLWAVE": "04000000",
    "ELECTRO-DOWNTEMPO": "04000000",
    "ELECTRO-DUBSTEP": "04000000",
    "ELECTRO-EXPERIMENTAL": "04000000",
    "ELECTRO-GARAGE": "04000000",
    "ELECTRO-GRIME": "04000000",
    "ELECTRO-HARD_DANCE": "04000000",
    "ELECTRO-HARDCORE": "04000000",
    "ELECTRO-INDUSTRIEL": "04000000",
    "ELECTRO-TRANCE": "04000000",
    "ELECTRO-DANCE": "04000000",
    "ELECTRO-DRUM_AND_BASS": "04000000",
    "ELECTRO-ELECTRONICA": "04000000",
    "ELECTRO-HOUSE": "04000000",
    "ELECTRO-LOUNGE": "04000000",
    "ELECTRO-TECHNO": "04000000",
    "ELECTRO-OTHER": "04000000",
    "HIP_HOP_RAP-BOUNCE": "11000000",
    "HIP_HOP_RAP-RAP_ALTERNATIF": "11000000",
    "HIP_HOP_RAP-RAP_EAST_COAST": "11020000",
    "HIP_HOP_RAP-RAP_GANGSTA": "11000000",
    "HIP_HOP_RAP-RAP_HARDCORE": "11000000",
    "HIP_HOP_RAP-RAP_LATINO": "11000000",
    "HIP_HOP_RAP-RAP_UNDERGROUND": "11000000",
    "HIP_HOP_RAP-RAP_WEST_COAST": "11000000",
    "HIP_HOP_RAP-TRAP": "11000000",
    "HIP_HOP_RAP-TRIP_HOP": "11000000",
    "HIP_HOP_RAP-DOO_WOP": "11000000",
    "HIP_HOP_RAP-MOTOWN": "11000000",
    "HIP_HOP_RAP-NEO_SOUL": "11000000",
    "HIP_HOP_RAP-SOUL_PSYCHEDELIQUE": "11000000",
    "HIP_HOP_RAP-HIP_HOP": "11000000",
    "HIP_HOP_RAP-RAP_FRANCAIS": "11000000",
    "HIP_HOP_RAP-RAP_OLD_SCHOOL": "11000000",
    "HIP_HOP_RAP-R&B_CONTEMPORAIN": "11000000",
    "HIP_HOP_RAP-DISCO": "11000000",
    "HIP_HOP_RAP-FUNK": "11000000",
    "HIP_HOP_RAP-SOUL": "11000000",
    "HIP_HOP_RAP-OTHER": "11000000",
    "GOSPEL-SPIRITUAL_GOSPEL": "02000000",
    "GOSPEL-SOUTHERN_GOSPEL": "02000000",
    "GOSPEL-CONTEMPORARY_GOSPEL": "02000000",
    "GOSPEL-BLUEGRASS_GOSPEL": "02000000",
    "GOSPEL-BLUES_GOSPEL": "02000000",
    "GOSPEL-COUNTRY_GOSPEL": "02000000",
    "GOSPEL-HYBRID_GOSPEL": "02000000",
    "GOSPEL-TRADITIONAL_GOSPEL": "02000000",
    "GOSPEL-OTHER": "02000000",
    "CHANSON_VARIETE-MUSETTE": "17000000",
    "CHANSON_VARIETE-SLAM": "09000000",
    "CHANSON_VARIETE-CHANSON_FRANCAISE": "09000000",
    "CHANSON_VARIETE-MUSIC_HALL": "09000000",
    "CHANSON_VARIETE-FOLKLORE_FRANCAIS": "09000000",
    "CHANSON_VARIETE-CHANSON_À_TEXTE": "09000000",
    "CHANSON_VARIETE-OTHER": "09000000",
    "OTHER": "19000000",
}


class TiteliveMusicSupport(typing.TypedDict):
    codesupport: str
    libelle: str
    is_allowed: bool


TITELIVE_MUSIC_SUPPORTS: list[TiteliveMusicSupport] = [
    {"codesupport": "0", "libelle": "REFERENCE INTERNE", "is_allowed": False},
    {"codesupport": "1", "libelle": "MULTI SUPPORT", "is_allowed": False},
    {"codesupport": "2", "libelle": "45 TOURS", "is_allowed": True},
    {"codesupport": "3", "libelle": "45 TOURS", "is_allowed": True},
    {"codesupport": "4", "libelle": "MAXI 45 TOURS", "is_allowed": True},
    {"codesupport": "5", "libelle": "33 TOURS", "is_allowed": True},
    {"codesupport": "6", "libelle": "33 TOURS", "is_allowed": True},
    {"codesupport": "7", "libelle": "33 TOURS", "is_allowed": True},
    {"codesupport": "8", "libelle": "CD SINGLE", "is_allowed": True},
    {"codesupport": "9", "libelle": "CD SINGLE", "is_allowed": True},
    {"codesupport": "10", "libelle": "MAXI SINGLE", "is_allowed": True},
    {"codesupport": "11", "libelle": "CD", "is_allowed": True},
    {"codesupport": "12", "libelle": "K7 SINGLE", "is_allowed": True},
    {"codesupport": "13", "libelle": "K7 SINGLE", "is_allowed": True},
    {"codesupport": "14", "libelle": "K7", "is_allowed": True},
    {"codesupport": "15", "libelle": "DOUBLE K7", "is_allowed": True},
    {"codesupport": "16", "libelle": "DCC", "is_allowed": False},
    {"codesupport": "17", "libelle": "MINI DISQUE", "is_allowed": False},
    {"codesupport": "18", "libelle": "VHS MUSICAL", "is_allowed": False},
    {"codesupport": "19", "libelle": "CD VIDEO", "is_allowed": False},
    {"codesupport": "20", "libelle": "CDI", "is_allowed": False},
    {"codesupport": "21", "libelle": "DVD MUSICAL", "is_allowed": True},
    {"codesupport": "22", "libelle": "CDROM", "is_allowed": False},
    {"codesupport": "23", "libelle": "DIVERS", "is_allowed": False},
    {"codesupport": "24", "libelle": "PLV", "is_allowed": False},
    {"codesupport": "25", "libelle": "JEU", "is_allowed": False},
    {"codesupport": "26", "libelle": "CLE USB / 512 MO", "is_allowed": False},
    {"codesupport": "27", "libelle": "LECTEUR MP3 / 512 MO", "is_allowed": False},
    {"codesupport": "28", "libelle": "NINTENDO WII", "is_allowed": False},
    {"codesupport": "29", "libelle": "BLU-RAY DISC (BD)", "is_allowed": True},
    {"codesupport": "30", "libelle": "DVD-HD", "is_allowed": False},
    {"codesupport": "31", "libelle": "TEE SHIRT", "is_allowed": False},
    {"codesupport": "32", "libelle": "MERCHANDISING", "is_allowed": False},
    {"codesupport": "33", "libelle": "GOODIES MULTIMEDIA", "is_allowed": False},
    {"codesupport": "34", "libelle": "CD MULTIMEDIA", "is_allowed": True},
    {"codesupport": "35", "libelle": "NINTENDO DS", "is_allowed": False},
    {"codesupport": "36", "libelle": "SACD", "is_allowed": True},
    {"codesupport": "37", "libelle": "MAXI SINGLE MULTIMEDIA", "is_allowed": False},
    {"codesupport": "38", "libelle": "CD DIGIPACK", "is_allowed": True},
    {"codesupport": "39", "libelle": "GAMEBOY ADVANCE", "is_allowed": False},
    {"codesupport": "40", "libelle": "FICHIER TELECHARGEABLE", "is_allowed": False},
    {"codesupport": "41", "libelle": "DVD VIDEO (CRYSTAL) MUSICAL", "is_allowed": False},
    {"codesupport": "42", "libelle": "CD MAXI + DVD (DUALDISC)", "is_allowed": False},
    {"codesupport": "43", "libelle": "CD + DVD (DUALDISC)", "is_allowed": True},
    {"codesupport": "44", "libelle": "NINTENDO WII U", "is_allowed": False},
    {"codesupport": "45", "libelle": "SONY PLAYSTATION 4", "is_allowed": False},
    {"codesupport": "46", "libelle": "SONY PLAYSTATION 2", "is_allowed": False},
    {"codesupport": "47", "libelle": "UMD MUSICAL", "is_allowed": False},
    {"codesupport": "48", "libelle": "UMD FILM", "is_allowed": False},
    {"codesupport": "49", "libelle": "VHS False MUSICAL", "is_allowed": False},
    {"codesupport": "50", "libelle": "BLU-RAY DISC (BD)", "is_allowed": True},
    {"codesupport": "51", "libelle": "DVD-HD", "is_allowed": False},
    {"codesupport": "52", "libelle": "SONY PLAYSTATION 3", "is_allowed": False},
    {"codesupport": "53", "libelle": "SONY PSP", "is_allowed": False},
    {"codesupport": "54", "libelle": "MICROSOFT XBOX", "is_allowed": False},
    {"codesupport": "55", "libelle": "MICROSOFT XBOX360", "is_allowed": False},
    {"codesupport": "56", "libelle": "PC & MAC", "is_allowed": False},
    {"codesupport": "57", "libelle": "PC (WINDOWS)", "is_allowed": False},
    {"codesupport": "58", "libelle": "MAC", "is_allowed": False},
    {"codesupport": "59", "libelle": "NINTENDO 3DS", "is_allowed": False},
    {"codesupport": "60", "libelle": "SONY PS VITA", "is_allowed": False},
    {"codesupport": "61", "libelle": "CD + LIVRE", "is_allowed": True},
    {"codesupport": "62", "libelle": "MICROSOFT XBOX ONE", "is_allowed": False},
    {"codesupport": "63", "libelle": "MAXI K7 + LIVRE", "is_allowed": False},
    {"codesupport": "64", "libelle": "BLOG SONG", "is_allowed": False},
    {"codesupport": "65", "libelle": "EPK", "is_allowed": False},
    {"codesupport": "66", "libelle": "SPOT PUB", "is_allowed": False},
    {"codesupport": "67", "libelle": "MAKING OF", "is_allowed": False},
    {"codesupport": "68", "libelle": "CONSOLE RETRO", "is_allowed": False},
    {"codesupport": "69", "libelle": "SONY PLAYSTATION 5", "is_allowed": False},
    {"codesupport": "70", "libelle": "NINTENDO SWITCH", "is_allowed": False},
    {"codesupport": "71", "libelle": "MICROSOFT XBOX SERIES", "is_allowed": False},
    {"codesupport": "74", "libelle": "MINI CD", "is_allowed": True},
    {"codesupport": "75", "libelle": "VINYL", "is_allowed": True},
    {"codesupport": "76", "libelle": "CD BOX", "is_allowed": True},
    {"codesupport": "77", "libelle": "CD SINGLE", "is_allowed": False},
    {"codesupport": "78", "libelle": "DOUBLE VINYL", "is_allowed": True},
    {"codesupport": "79", "libelle": "CD", "is_allowed": False},
    {"codesupport": "80", "libelle": "CD SINGLE", "is_allowed": False},
    {"codesupport": "81", "libelle": "33 TOURS / SINGLE", "is_allowed": True},
    {"codesupport": "83", "libelle": "TRIPLE VINYL", "is_allowed": True},
    {"codesupport": "86", "libelle": "SAMPLER CLIP", "is_allowed": False},
    {"codesupport": "87", "libelle": "SAMPLER SINGLES", "is_allowed": False},
    {"codesupport": "88", "libelle": "SAMPLER ALBUMS", "is_allowed": False},
    {"codesupport": "89", "libelle": "DVD False MUSICAL", "is_allowed": False},
    {"codesupport": "90", "libelle": "K7", "is_allowed": False},
    {"codesupport": "91", "libelle": "DVD AUDIO", "is_allowed": False},
    {"codesupport": "92", "libelle": "DVD VIDEO SINGLE", "is_allowed": False},
    {"codesupport": "93", "libelle": "DVD VIDEO ALBUM", "is_allowed": False},
    {"codesupport": "94", "libelle": "BLU-RAY DISC 3D", "is_allowed": False},
    {"codesupport": "96", "libelle": "CD AUDIO + DVD", "is_allowed": True},
    {"codesupport": "97", "libelle": "CD AUDIO + DVD", "is_allowed": True},
    {"codesupport": "98", "libelle": "CD MAXI + VIDEO", "is_allowed": False},
    {"codesupport": "99", "libelle": "SAMPLER", "is_allowed": False},
    {"codesupport": "100", "libelle": "BLU-RAY AUDIO", "is_allowed": True},
    {"codesupport": "101", "libelle": "LISEUSES", "is_allowed": False},
    {"codesupport": "102", "libelle": "CD AUDIO + BR (package CD)", "is_allowed": True},
    {"codesupport": "103", "libelle": "CD AUDIO + BR (package BR)", "is_allowed": True},
    {"codesupport": "104", "libelle": "CD AUDIO + BR 3D (package CD)", "is_allowed": False},
    {"codesupport": "105", "libelle": "CD AUDIO + BR 3D (package BR)", "is_allowed": False},
    {"codesupport": "106", "libelle": "GOOGLE STADIA", "is_allowed": False},
    {"codesupport": "107", "libelle": "ACCESSOIRES", "is_allowed": False},
]
TITELIVE_MUSIC_SUPPORTS_BY_CODE = {support["codesupport"]: support for support in TITELIVE_MUSIC_SUPPORTS}
NOT_CD_LIBELLES = ["TOURS", "VINYL", "K7"]
