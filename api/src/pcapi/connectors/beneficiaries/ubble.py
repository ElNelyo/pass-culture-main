import datetime
import logging
import typing
import urllib.parse

import requests

from pcapi import settings
from pcapi.connectors.beneficiaries import exceptions
from pcapi.core.fraud import models as fraud_models


logger = logging.getLogger(__name__)


def configure_session() -> requests.Session:
    session = requests.Session()
    session.auth = (settings.UBBLE_CLIENT_ID, settings.UBBLE_CLIENT_SECRET)
    session.headers.update(
        {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
        }
    )

    return session


def build_url(path: str) -> str:
    return urllib.parse.urljoin(settings.UBBLE_API_URL, path)


INCLUDED_MODELS = {
    "documents": fraud_models.UbbleIdentificationDocuments,
    "document-checks": fraud_models.UbbleIdentificationDocumentChecks,
}


def _get_included_attributes(
    response: fraud_models.UbbleIdentificationResponse, type_: str
) -> typing.Union[fraud_models.UbbleIdentificationDocuments, fraud_models.UbbleIdentificationDocumentChecks]:
    filtered = list(filter(lambda included: included["type"] == type_, response["included"]))
    attributes = INCLUDED_MODELS[type_](**filtered[0].get("attributes")) if filtered else None
    return attributes


def _get_data_attribute(response: fraud_models.UbbleIdentificationResponse, name: str) -> typing.Any:
    return response["data"]["attributes"].get(name)


def _extract_useful_content_from_response(
    response: fraud_models.UbbleIdentificationResponse,
) -> fraud_models.UbbleContent:
    documents: fraud_models.UbbleIdentificationDocuments = _get_included_attributes(response, "documents")
    document_checks: fraud_models.UbbleIdentificationDocumentChecks = _get_included_attributes(
        response, "document-checks"
    )
    score = _get_data_attribute(response, "score")
    comment = _get_data_attribute(response, "comment")
    identification_id = _get_data_attribute(response, "identification-id")
    identification_url = _get_data_attribute(response, "identification-url")
    status = _get_data_attribute(response, "status")
    registered_at = _get_data_attribute(response, "created-at")

    content = fraud_models.UbbleContent(
        status=status,
        birth_date=getattr(documents, "birth_date", None),
        first_name=getattr(documents, "first_name", None),
        last_name=getattr(documents, "last_name", None),
        document_type=getattr(documents, "document_type", None),
        id_document_number=getattr(documents, "document_number", None),
        score=score,
        comment=comment,
        expiry_date_score=getattr(document_checks, "expiry_date_score", None),
        supported=getattr(document_checks, "supported", None),
        identification_id=identification_id,
        identification_url=identification_url,
        registration_datetime=registered_at,
    )
    return content


def start_identification(
    user_id: int,
    phone_number: str,
    birth_date: datetime.date,
    first_name: str,
    last_name: str,
    webhook_url: str,
    redirect_url: str,
) -> fraud_models.UbbleContent:
    session = configure_session()

    data = {
        "data": {
            "type": "identifications",
            "attributes": {
                "identification-form": {
                    "external-user-id": user_id,
                    "phone-number": phone_number,
                },
                "reference-data": {
                    "birth-date": datetime.date.strftime(birth_date, "%Y-%m-%d"),
                    "first-name": first_name,
                    "last-name": last_name,
                },
                "webhook": webhook_url,
                "redirect_url": redirect_url,
            },
        }
    }

    try:
        response = session.post(build_url("/identifications/"), json=data)
    except IOError as e:
        # Any exception explicitely raised by requests or urllib3 inherits from IOError
        logger.exception("Request error while starting Ubble identification: %s", e, extra={"alert": "Ubble error"})
        raise exceptions.IdentificationServiceUnavailable()

    if not response.ok:
        # https://ubbleai.github.io/developer-documentation/#errors
        logger.error(
            "Error while starting Ubble identification: %s, %s",
            response.status_code,
            response.text,
            extra={"alert": "Ubble error"},
        )
        if response.status_code in (410, 429):
            raise exceptions.IdentificationServiceUnavailable()
        # Other errors should not happen, so keep them different than Ubble unavailable
        raise exceptions.IdentificationServiceError()

    content = _extract_useful_content_from_response(response.json())
    return content


def get_content(identification_id: str) -> fraud_models.UbbleContent:
    session = configure_session()
    response = session.get(
        build_url(f"/identifications/{identification_id}/"),
    )
    content = _extract_useful_content_from_response(response.json())
    return content
