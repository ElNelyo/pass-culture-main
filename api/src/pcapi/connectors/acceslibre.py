"""
A client for API Acceslibre.
Documentation of the API: https://acceslibre.beta.gouv.fr/api/docs/
Further explanations at: https://schema.data.gouv.fr/MTES-MCT/acceslibre-schema/0.0.14/documentation.html
"""

from datetime import datetime
import enum
import json
import logging
from typing import TypedDict
import uuid

from dateutil import parser
import pydantic.v1 as pydantic_v1
from rapidfuzz import fuzz

from pcapi import settings
from pcapi.utils import module_loading
from pcapi.utils import requests


logger = logging.getLogger(__name__)

ACCESLIBRE_REQUEST_TIMEOUT = 3
REQUEST_PAGE_SIZE = 50
ADDRESS_MATCHING_RATIO = 80
NAME_MATCHING_RATIO = 45


class AcceslibreActivity(enum.Enum):
    """
    The following are Acceslibre activities that we can use in our matching algorithm
    """

    ADMINISTRATION_PUBLIQUE = "administration-publique"
    AQUARIUM = "aquarium"
    ART = "art"
    ARTISANAT = "artisanat"
    ASSOCIATION = "association"
    BIBLIOTHEQUE = "bibliotheque-mediatheque"
    CENTRE_CULTUREL = "centre-culturel"
    CHATEAU = "chateau"
    CINEMA = "cinema"
    COLLECTIVITE_TERRITORIALE = "collectivite-territoriale"
    CONSERVATOIRE_ET_ECOLE_DE_MUSIQUE = "conservatoire-et-ecole-de-musique"
    DISQUAIRE = "disquaire"
    ECOLE_DE_DANSE = "ecole-de-danse"
    ENCADREUR_ENLUMINEUR = "encadreur-enlumineur"
    EVENEMENT_CULTUREL = "evenement-culturel"
    GALERIE_D_ART = "salle-dexposition"
    GYMNASE = "gymnase"
    INSTRUMENT_ET_MATERIEL_DE_MUSIQUE = "instruments-et-materiel-de-musique"
    JARDIN_BOTANIQUE_ETOU_ZOOLOGIQUE = "jardin-botanique-etou-zoologique"
    LIBRAIRIE = "librairie"
    LIEU_DE_VISITE = "lieu-de-visite"
    LOISIRS_CREATIFS = "loisirs-creatifs"
    MENUISERIE = "menuiserie-ebenisterie"
    MONUMENT_HISTORIQUE = "monument-historique"
    MUSEE = "musee"
    MUSIQUE = "musique"
    OFFICE_DU_TOURISME = "office-du-tourisme"
    OPERA = "opera"
    PAPETERIE_PRESSE_JOURNAUX = "papeterie-presse-journaux"
    PARC_DES_EXPOSITIONS = "parc-des-expositions"
    SALLE_DE_CONCERT = "salle-de-concert"
    SALLE_DE_DANSE = "salle-de-danse"
    SALLE_DES_FETES = "salle-des-fetes"
    SALLE_DE_SPECTACLE = "salle-de-spectacle"
    THEATRE = "theatre"


class ExpectedFieldsEnum(enum.Enum):
    UNKNOWN = "Non renseigné"
    PARKING_ADAPTED = "Stationnement adapté dans l'établissement"
    PARKING_NEARBY = "Stationnement adapté à proximité"
    PARKING_UNAVAILABLE = "Pas de stationnement adapté à proximité"
    EXTERIOR_ONE_LEVEL = "Chemin d'accès de plain pied"
    EXTERIOR_ACCESS_RAMP = "Chemin rendu accessible (rampe)"
    EXTERIOR_ACCESS_ELEVATOR = "Chemin rendu accessible (ascenseur)"
    EXTERIOR_ACCESS_HAS_DIFFICULTIES = "Difficulté sur le chemin d'accès"
    ENTRANCE_ONE_LEVEL = "Entrée de plain pied"
    ENTRANCE_ONE_LEVEL_NARROW = "Entrée de plain pied mais étroite"
    ENTRANCE_NOT_ONE_LEVEL = "L'entrée n'est pas de plain-pied"
    ENTRANCE_HUMAN_HELP = "L'entrée n'est pas de plain-pied\n Aide humaine possible"
    ENTRANCE_ELEVATOR = "Accès à l'entrée par ascenseur"
    ENTRANCE_ELEVATOR_NARROW = "Entrée rendue accessible par ascenseur mais étroite"
    ENTRANCE_RAMP = "Accès à l'entrée par une rampe"
    ENTRANCE_RAMP_NARROW = "Entrée rendue accessible par rampe mais étroite"
    ENTRANCE_PRM = "Entrée spécifique PMR"
    PERSONNEL_MISSING = "Aucun personnel"
    PERSONNEL_UNTRAINED = "Personnel non formé"
    PERSONNEL_TRAINED = "Personnel sensibilisé / formé"
    SOUND_BEACON = "Balise sonore"
    DEAF_AND_HARD_OF_HEARING_FIXED_INDUCTION_LOOP = "boucle à induction magnétique fixe"
    DEAF_AND_HARD_OF_HEARING_PORTABLE_INDUCTION_LOOP = "boucle à induction magnétique portative"
    DEAF_AND_HARD_OF_HEARING_SIGN_LANGUAGE = "langue des signes française (LSF)"
    DEAF_AND_HARD_OF_HEARING_CUED_SPEECH = "langue française parlée complétée (LFPC)"
    DEAF_AND_HARD_OF_HEARING_SUBTITLE = "sous-titrage ou transcription simultanée"
    DEAF_AND_HARD_OF_HEARING_OTHER = "autres"
    FACILITIES_ADAPTED = "Sanitaire adapté"
    FACILITIES_UNADAPTED = "Sanitaire non adapté"
    AUDIODESCRIPTION_PERMANENT = "avec équipement permanent, casques et boîtiers disponibles à l’accueil"
    AUDIODESCRIPTION_PERMANENT_SMARTPHONE = (
        "avec équipement permanent nécessitant le téléchargement d'une application sur smartphone"
    )
    AUDIODESCRIPTION_OCCASIONAL = "avec équipement occasionnel selon la programmation"
    AUDIODESCRIPTION_NO_DEVICE = "sans équipement, audiodescription audible par toute la salle (selon la programmation)"

    @classmethod
    def find_enum_from_string(cls, input_string: str) -> list:
        """
        Acceslibre may return a combinaison of several fields, comma separated
        """
        # FIXME: ogeber 03.04.2024 I've ask acceslibre to return fields in a list instead of a comma separated string
        # When done, we can delete this method and use `if label not in [item.value for item in ExpectedFieldsEnum]` instead
        enum_list: list[ExpectedFieldsEnum] = []
        for enum_option in cls:
            if enum_option.value in input_string:
                enum_list.append(enum_option)
        # Reorder enum_list according to its order in the input_string
        enum_indexes = {
            enum_option: input_string.index(enum_option.value)
            for enum_option in enum_list
            if enum_option.value in input_string
        }
        sorted_enum_list = sorted(enum_list, key=lambda x: enum_indexes[x])
        return sorted_enum_list


class AccesLibreApiException(Exception):
    pass


class AccessibilityParsingException(Exception):
    pass


class AccessibilityInfo(pydantic_v1.BaseModel):
    access_modality: list[ExpectedFieldsEnum] = pydantic_v1.Field(default_factory=list)
    audio_description: list[ExpectedFieldsEnum] = pydantic_v1.Field(default_factory=list)
    deaf_and_hard_of_hearing_amenities: list[ExpectedFieldsEnum] = pydantic_v1.Field(default_factory=list)
    facilities: list[ExpectedFieldsEnum] = pydantic_v1.Field(default_factory=list)
    sound_beacon: list[ExpectedFieldsEnum] = pydantic_v1.Field(default_factory=list)
    trained_personnel: list[ExpectedFieldsEnum] = pydantic_v1.Field(default_factory=list)
    transport_modality: list[ExpectedFieldsEnum] = pydantic_v1.Field(default_factory=list)

    @pydantic_v1.root_validator(pre=True)
    def set_default_to_empty_list(cls, values: dict) -> dict:
        for field_name, field_value in values.items():
            if field_value is None:
                values[field_name] = []
        return values


class AcceslibreData(TypedDict):
    title: str
    labels: list[str]


def _get_backend() -> "BaseBackend":
    backend_class = module_loading.import_string(settings.ACCESLIBRE_BACKEND)
    return backend_class()


def find_venue_at_accessibility_provider(
    name: str,
    public_name: str | None = None,
    siret: str | None = None,
    ban_id: str | None = None,
    city: str | None = None,
    postal_code: str | None = None,
    address: str | None = None,
) -> dict | None:
    """Try to find the entry at acceslibre that matches our venue
    Returns acceslibre venue
    """
    return _get_backend().find_venue_at_accessibility_provider(
        name=name,
        public_name=public_name,
        siret=siret,
        ban_id=ban_id,
        city=city,
        postal_code=postal_code,
        address=address,
    )


def get_id_at_accessibility_provider(
    name: str,
    public_name: str | None = None,
    siret: str | None = None,
    ban_id: str | None = None,
    city: str | None = None,
    postal_code: str | None = None,
    address: str | None = None,
) -> str | None:
    """
    Returns the slug (unique ID at acceslibre) of the venue at acceslibre
    """
    return _get_backend().get_id_at_accessibility_provider(
        name=name,
        public_name=public_name,
        siret=siret,
        ban_id=ban_id,
        city=city,
        postal_code=postal_code,
        address=address,
    )


def get_last_update_at_provider(slug: str) -> datetime | None:
    return _get_backend().get_last_update_at_provider(slug)


def get_accessibility_infos(slug: str) -> AccessibilityInfo | None:
    """Fetch accessibility data from acceslibre and save them in an AccessibilityInfo object
    This object will then be saved in db in the AccessibilityProvider.externalAccessibilityData JSONB
    """
    return _get_backend().get_accessibility_infos(slug=slug)


def extract_street_name(address: str | None = None, city: str | None = None, postal_code: str | None = None) -> str:
    if address and city and postal_code:
        return address.lower().replace(postal_code, "").replace(city.lower(), "").rstrip()
    return ""


def match_venue_with_acceslibre(
    acceslibre_results: list[dict],
    venue_name: str,
    venue_public_name: str | None,
    venue_address: str | None,
    venue_ban_id: str | None,
    venue_siret: str | None,
) -> dict[str, str] | None:
    """
    From the results we get from requesting acceslibre API, we try a match with our venue
    by comparing the name and address using a fuzzy matching algorithm.
    We also check that the activity of the venue at acceslibre is in the enum AcceslibreActivity
    """
    venue_name = venue_name.lower()
    venue_public_name = venue_public_name.lower() if venue_public_name else "PUBLIC_NAME_MISSING"
    venue_address = venue_address.lower() if venue_address else "ADDRESS_MISSING"

    for result in acceslibre_results:
        acceslibre_name = result["nom"].lower()
        acceslibre_address = extract_street_name(result["adresse"], result["commune"], result["code_postal"])
        acceslibre_activity = result["activite"]["slug"]
        acceslibre_ban_id = result["ban_id"]
        acceslibre_siret = result["siret"]
        # check siret matching
        if venue_siret and venue_siret == acceslibre_siret:
            return result
        if (  # pylint: disable=too-many-boolean-expressions
            # check activity is valid
            acceslibre_activity in [a.value for a in AcceslibreActivity]
            # name matching
            and (
                acceslibre_name in venue_name
                or venue_name in acceslibre_name
                or venue_public_name in acceslibre_name
                or acceslibre_name in venue_public_name
                or fuzz.ratio(acceslibre_name, venue_name) > NAME_MATCHING_RATIO
                or fuzz.ratio(acceslibre_name, venue_public_name) > NAME_MATCHING_RATIO
            )
            # check if BAN id or address matching
            and (
                (venue_ban_id and venue_ban_id == acceslibre_ban_id)
                or (
                    venue_address
                    and acceslibre_address
                    and fuzz.ratio(acceslibre_address, venue_address) > ADDRESS_MATCHING_RATIO
                )
            )
        ):
            return result
    return None


def acceslibre_to_accessibility_infos(acceslibre_data: list[AcceslibreData]) -> AccessibilityInfo:
    accessibility_infos = AccessibilityInfo()
    acceslibre_mapping = {
        "accès": "access_modality",
        "audiodescription": "audio_description",
        "équipements sourd et malentendant": "deaf_and_hard_of_hearing_amenities",
        "sanitaire": "facilities",
        "balise sonore": "sound_beacon",
        "personnel": "trained_personnel",
        "stationnement": "transport_modality",
    }

    for section in acceslibre_data:
        try:
            title = section["title"]
            labels = section["labels"]
        except KeyError:
            raise AccesLibreApiException(
                "'title' or 'labels' key is missing in one of the sections. Check API response or contact Acceslibre"
            )
        attribute_name = acceslibre_mapping.get(title)
        if not attribute_name:
            continue
        labels_enum = []
        for label in labels:
            if not (labels_enum_list := ExpectedFieldsEnum.find_enum_from_string(label)):
                # If this exception is raised, you should probably set the ExpectedFieldsEnum for the given label
                # according to acceslibre API schema, at https://github.com/MTES-MCT/acceslibre/blob/master/erp/views.py
                raise AccesLibreApiException(f"Acceslibre API returned an unexpected value: {label} for {title}")
            labels_enum.extend(labels_enum_list)
        setattr(accessibility_infos, attribute_name, labels_enum)
    return accessibility_infos


class BaseBackend:
    def find_venue_at_accessibility_provider(
        self,
        name: str,
        public_name: str | None = None,
        siret: str | None = None,
        ban_id: str | None = None,
        city: str | None = None,
        postal_code: str | None = None,
        address: str | None = None,
    ) -> dict | None:
        raise NotImplementedError()

    def get_id_at_accessibility_provider(
        self,
        name: str,
        public_name: str | None = None,
        siret: str | None = None,
        ban_id: str | None = None,
        city: str | None = None,
        postal_code: str | None = None,
        address: str | None = None,
    ) -> str | None:
        raise NotImplementedError()

    def get_last_update_at_provider(self, slug: str) -> datetime | None:
        raise NotImplementedError()

    def get_accessibility_infos(self, slug: str) -> AccessibilityInfo | None:
        raise NotImplementedError()


class TestingBackend(BaseBackend):
    def find_venue_at_accessibility_provider(
        self,
        name: str,
        public_name: str | None = None,
        siret: str | None = None,
        ban_id: str | None = None,
        city: str | None = None,
        postal_code: str | None = None,
        address: str | None = None,
    ) -> dict | None:
        return {
            "slug": "mon-lieu-chez-acceslibre",
            "uuid": str(uuid.uuid4()),
            "nom": "Un lieu",
            "adresse": "3 Rue de Valois 75001 Paris",
            "activite": {"nom": "Bibliothèque Médiathèque", "slug": "bibliotheque-mediatheque"},
            "siret": "",
            "updated_at": "2023-04-13T15:10:25.612731+02:00",
        }

    def get_id_at_accessibility_provider(
        self,
        name: str,
        public_name: str | None = None,
        siret: str | None = None,
        ban_id: str | None = None,
        city: str | None = None,
        postal_code: str | None = None,
        address: str | None = None,
    ) -> str | None:
        return "mon-lieu-chez-acceslibre"

    def get_last_update_at_provider(self, slug: str) -> datetime | None:
        return datetime(2024, 3, 1, 0, 0)

    def get_accessibility_infos(self, slug: str) -> AccessibilityInfo | None:
        accesslibre_data_list = [
            {
                "title": "stationnement",
                "labels": ["Stationnement adapté dans l'établissement"],
            },
            {
                "title": "accès",
                "labels": ["Chemin d'accès de plain pied", "Entrée de plain pied"],
            },
            {
                "title": "personnel",
                "labels": ["Personnel sensibilisé / formé"],
            },
            {
                "title": "audiodescription",
                "labels": ["avec équipement occasionnel selon la programmation"],
            },
            {
                "title": "sanitaire",
                "labels": ["Sanitaire adapté"],
            },
        ]
        acceslibre_data = [
            AcceslibreData(title=str(item["title"]), labels=[str(label) for label in item["labels"]])
            for item in accesslibre_data_list
        ]
        return acceslibre_to_accessibility_infos(acceslibre_data)


class AcceslibreBackend(BaseBackend):
    def _send_request(
        self,
        query_params: dict[str, str],
    ) -> dict:
        api_key = settings.ACCESLIBRE_API_KEY
        url = settings.ACCESLIBRE_API_URL
        headers = {"Authorization": f"Api-Key {api_key}"}
        try:
            response = requests.get(url, headers=headers, params=query_params, timeout=ACCESLIBRE_REQUEST_TIMEOUT)
        except requests.exceptions.RequestException:
            raise AccesLibreApiException(
                f"Error connecting AccesLibre API for {url} and query parameters: {query_params}"
            )
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error(
                "Got non-JSON or malformed JSON response from AccesLibre",
                extra={"url": response.url, "response": response.content},
            )
            raise AccesLibreApiException(f"Non-JSON response from AccesLibre API for {response.url}")

    def _send_request_with_slug(
        self,
        slug: str,
        request_widget_infos: bool | None = False,
    ) -> dict | None:
        """
        Acceslibre has a specific GET route /api/erps/{slug} that
        we can requested when a venue slug is known. This slug is saved in the
        Venue.accessibilityProvider.externalAccessibilityId field on our side.
        """
        api_key = settings.ACCESLIBRE_API_KEY
        url = settings.ACCESLIBRE_API_URL + slug
        if request_widget_infos:
            url += "/widget"
        headers = {"Authorization": f"Api-Key {api_key}"}
        try:
            response = requests.get(url, headers=headers, timeout=ACCESLIBRE_REQUEST_TIMEOUT)
        except requests.exceptions.RequestException:
            raise AccesLibreApiException(f"Error connecting AccesLibre API for {url}")
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                logger.error(
                    "Got non-JSON or malformed JSON response from AccesLibre",
                    extra={"url": response.url, "response": response.content},
                )
                raise AccesLibreApiException(f"Non-JSON response from AccesLibre API for {response.url}")
        return None

    def find_venue_at_accessibility_provider(
        self,
        name: str,
        public_name: str | None = None,
        siret: str | None = None,
        ban_id: str | None = None,
        city: str | None = None,
        postal_code: str | None = None,
        address: str | None = None,
    ) -> dict | None:
        search_criteria: list[dict] = [
            {"siret": siret},
            {"ban_id": ban_id},
            {
                "q": name,
                "commune": city,
                "code_postal": postal_code,
                "page_size": REQUEST_PAGE_SIZE,
            },
            {
                "q": public_name,
                "commune": city,
                "code_postal": postal_code,
                "page_size": REQUEST_PAGE_SIZE,
            },
        ]

        for criterion in search_criteria:
            if all(v is not None for v in criterion.values()):
                response = self._send_request(query_params=criterion)
                if response["count"] and (
                    matching_venue := match_venue_with_acceslibre(
                        acceslibre_results=response["results"],
                        venue_name=name,
                        venue_public_name=public_name,
                        venue_address=address,
                        venue_ban_id=ban_id,
                        venue_siret=siret,
                    )
                ):
                    return matching_venue
        return None

    def get_id_at_accessibility_provider(
        self,
        name: str,
        public_name: str | None = None,
        siret: str | None = None,
        ban_id: str | None = None,
        city: str | None = None,
        postal_code: str | None = None,
        address: str | None = None,
    ) -> str | None:
        matching_venue = find_venue_at_accessibility_provider(
            name, public_name, siret, ban_id, city, postal_code, address
        )
        if matching_venue:
            return matching_venue["slug"]
        return None

    def get_last_update_at_provider(self, slug: str) -> datetime | None:
        if response := self._send_request_with_slug(slug=slug):
            created_at = parser.isoparse(response["created_at"])
            updated_at = parser.isoparse(response["updated_at"])
            if updated_at > created_at:
                return updated_at
            return created_at
        # if Venue is not found at acceslibre, we return None
        return None

    def get_accessibility_infos(self, slug: str) -> AccessibilityInfo | None:
        if response := self._send_request_with_slug(slug=slug, request_widget_infos=True):
            try:
                response_list = response["sections"]
            except KeyError:
                raise AccesLibreApiException(
                    "'sections' key is missing in the response from acceslibre. Check API response or contact Acceslibre"
                )
            acceslibre_data = [
                AcceslibreData(title=str(item["title"]), labels=[str(label) for label in item["labels"]])
                for item in response_list
            ]
            return acceslibre_to_accessibility_infos(acceslibre_data)
        return None
