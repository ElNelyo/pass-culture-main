from datetime import datetime
import re
from typing import Callable
from typing import Dict
from typing import List

from pcapi import settings
from pcapi.connectors.api_demarches_simplifiees import get_application_details
from pcapi.core.users.models import User
from pcapi.domain.demarches_simplifiees import get_closed_application_ids_for_demarche_simplifiee
from pcapi.domain.user_activation import create_beneficiary_from_application
from pcapi.domain.user_emails import send_activation_email
from pcapi.models import ApiErrors
from pcapi.models import ImportStatus
from pcapi.models.beneficiary_import import BeneficiaryImportSources
from pcapi.repository import repository
from pcapi.repository.beneficiary_import_queries import find_applications_ids_to_retry
from pcapi.repository.beneficiary_import_queries import is_already_imported
from pcapi.repository.beneficiary_import_queries import save_beneficiary_import_with_status
from pcapi.repository.user_queries import find_by_civility
from pcapi.repository.user_queries import find_user_by_email
from pcapi.utils.logger import logger
from pcapi.utils.mailing import MailServiceException
from pcapi.utils.mailing import send_raw_email


def run(
    process_applications_updated_after: datetime,
    get_all_applications_ids: Callable[..., List[int]] = get_closed_application_ids_for_demarche_simplifiee,
    get_applications_ids_to_retry: Callable[..., List[int]] = find_applications_ids_to_retry,
    get_details: Callable[..., Dict] = get_application_details,
    already_imported: Callable[..., bool] = is_already_imported,
    already_existing_user: Callable[..., User] = find_user_by_email,
) -> None:
    procedure_id = settings.DMS_OLD_ENROLLMENT_PROCEDURE_ID
    logger.info(
        "[BATCH][REMOTE IMPORT BENEFICIARIES] Start import from Démarches Simplifiées - Procedure %s", procedure_id
    )
    error_messages: List[str] = []
    new_beneficiaries: List[User] = []
    applications_ids = get_all_applications_ids(procedure_id, settings.DMS_TOKEN, process_applications_updated_after)
    retry_ids = get_applications_ids_to_retry()

    logger.info(
        "[BATCH][REMOTE IMPORT BENEFICIARIES] %i new applications to process - Procedure %s",
        len(applications_ids),
        procedure_id,
    )
    logger.info(
        "[BATCH][REMOTE IMPORT BENEFICIARIES] %i previous applications to retry - Procedure %s",
        len(retry_ids),
        procedure_id,
    )

    for application_id in retry_ids + applications_ids:
        details = get_details(application_id, procedure_id, settings.DMS_TOKEN)
        try:
            information = parse_beneficiary_information(details)
        except Exception:  # pylint: disable=broad-except
            _process_error(error_messages, application_id, procedure_id)
            continue

        if already_existing_user(information["email"]):
            _process_rejection(information, procedure_id)
            continue

        if not already_imported(information["application_id"]):
            process_beneficiary_application(
                information=information,
                error_messages=error_messages,
                new_beneficiaries=new_beneficiaries,
                retry_ids=retry_ids,
                procedure_id=procedure_id,
            )

    logger.info(
        "[BATCH][REMOTE IMPORT BENEFICIARIES] End import from Démarches Simplifiées - Procedure %s", procedure_id
    )


def process_beneficiary_application(
    information: Dict,
    error_messages: List[str],
    new_beneficiaries: List[User],
    retry_ids: List[int],
    procedure_id: int,
    find_duplicate_users: Callable[..., List[User]] = find_by_civility,
) -> None:
    duplicate_users = find_duplicate_users(
        information["first_name"], information["last_name"], information["birth_date"]
    )

    if not duplicate_users or information["application_id"] in retry_ids:
        _process_creation(error_messages, information, new_beneficiaries, procedure_id)
    else:
        _process_duplication(duplicate_users, error_messages, information, procedure_id)


def parse_beneficiary_information(application_detail: Dict) -> Dict:
    dossier = application_detail["dossier"]

    information = {
        "last_name": dossier["individual"]["nom"],
        "first_name": dossier["individual"]["prenom"],
        "civility": dossier["individual"]["civilite"],
        "email": dossier["email"],
        "application_id": dossier["id"],
    }

    for field in dossier["champs"]:
        label = field["type_de_champ"]["libelle"]
        value = field["value"]

        if "Veuillez indiquer votre département" in label:
            information["department"] = re.search("^[0-9]{2,3}|[2BbAa]{2}", value).group(0)
        if label == "Date de naissance":
            information["birth_date"] = datetime.strptime(value, "%Y-%m-%d")
        if label == "Numéro de téléphone":
            information["phone"] = value
        if label == "Code postal de votre adresse de résidence":
            space_free = value.strip().replace(" ", "")
            information["postal_code"] = re.search("^[0-9]{5}", space_free).group(0)
        if label == "Veuillez indiquer votre statut":
            information["activity"] = value

    return information


def _process_creation(
    error_messages: List[str], information: Dict, new_beneficiaries: List[User], procedure_id: int
) -> None:
    new_beneficiary = create_beneficiary_from_application(information)
    try:
        repository.save(new_beneficiary)
    except ApiErrors as api_errors:
        logger.warning(
            "[BATCH][REMOTE IMPORT BENEFICIARIES] Could not save application %s, because of error: %s - Procedure %s",
            information["application_id"],
            api_errors,
            procedure_id,
        )
        error_messages.append(str(api_errors))
    else:
        logger.info(
            "[BATCH][REMOTE IMPORT BENEFICIARIES] Successfully created user for application %s - Procedure %s",
            information["application_id"],
            procedure_id,
        )
        save_beneficiary_import_with_status(
            ImportStatus.CREATED,
            information["application_id"],
            source=BeneficiaryImportSources.demarches_simplifiees,
            source_id=procedure_id,
            user=new_beneficiary,
        )
        new_beneficiaries.append(new_beneficiary)
        try:
            send_activation_email(new_beneficiary, send_raw_email)
        except MailServiceException:
            logger.exception(
                "Email send_activation_email failure for application %s - Procedure %s",
                information["application_id"],
                procedure_id,
            )


def _process_duplication(
    duplicate_users: List[User], error_messages: List[str], information: Dict, procedure_id: int
) -> None:
    number_of_beneficiaries = len(duplicate_users)
    duplicate_ids = ", ".join([str(u.id) for u in duplicate_users])
    message = f"{number_of_beneficiaries} utilisateur(s) en doublon {duplicate_ids} pour le dossier {information['application_id']}"
    logger.warning(
        "[BATCH][REMOTE IMPORT BENEFICIARIES] Duplicate beneficiaries found : %s - Procedure %s", message, procedure_id
    )
    error_messages.append(message)
    save_beneficiary_import_with_status(
        ImportStatus.DUPLICATE,
        information["application_id"],
        source=BeneficiaryImportSources.demarches_simplifiees,
        source_id=procedure_id,
        detail=f"Utilisateur en doublon : {duplicate_ids}",
    )


def _process_rejection(information: Dict, procedure_id: int) -> None:
    save_beneficiary_import_with_status(
        ImportStatus.REJECTED,
        information["application_id"],
        source=BeneficiaryImportSources.demarches_simplifiees,
        source_id=procedure_id,
        detail="Compte existant avec cet email",
    )
    logger.warning(
        "[BATCH][REMOTE IMPORT BENEFICIARIES] Rejected application %s because of already existing email - Procedure %s",
        information["application_id"],
        procedure_id,
    )


def _process_error(error_messages: List[str], application_id: int, procedure_id: int) -> None:
    error = f"Le dossier {application_id} contient des erreurs et a été ignoré - Procedure {procedure_id}"
    logger.error("[BATCH][REMOTE IMPORT BENEFICIARIES] %s", error)
    error_messages.append(error)
    save_beneficiary_import_with_status(
        ImportStatus.ERROR,
        application_id,
        source=BeneficiaryImportSources.demarches_simplifiees,
        source_id=procedure_id,
        detail=error,
    )
