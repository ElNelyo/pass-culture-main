import logging

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from pcapi import settings
from pcapi.core import mails
import pcapi.core.mails.models as mails_models
from pcapi.utils import requests


logger = logging.getLogger(__name__)


class SendinblueBackend:
    def __init__(self) -> None:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.SENDINBLUE_API_KEY
        self.api_instance = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))

    def send_transactional_sms(self, recipient: str, content: str) -> bool:
        send_transac_sms = sib_api_v3_sdk.SendTransacSms(
            sender="PassCulture",
            recipient=self._format_recipient(recipient),
            content=content,
            type="transactional",
            tag="phone-validation",
        )
        try:
            self.api_instance.send_transac_sms(send_transac_sms)

        except ApiException as exception:
            if exception.status and int(exception.status) >= 500:
                logger.warning(
                    "Sendinblue replied with status=%s when sending SMS",
                    exception.status,
                    extra={"recipient": recipient, "content": content},
                )
                raise requests.ExternalAPIException(is_retryable=True) from exception

            logger.exception("Error while sending SMS", extra={"recipient": recipient, "content": content})
            raise requests.ExternalAPIException(is_retryable=False) from exception

        except Exception as exception:
            logger.warning("Exception caught while sending SMS", extra={"recipient": recipient, "content": content})
            raise requests.ExternalAPIException(is_retryable=True) from exception

        return True

    def _format_recipient(self, recipient: str) -> str:
        """Sendinblue does not accept phone numbers with a leading '+'"""
        if recipient.startswith("+"):
            return recipient[1:]
        return recipient


class ToDevSendinblueBackend(SendinblueBackend):
    def send_transactional_sms(self, recipient: str, content: str) -> bool:
        # No need to import in production
        import sqlalchemy as sa

        from pcapi.core.users import models as users_models

        if recipient in settings.WHITELISTED_SMS_RECIPIENTS:
            if not super().send_transactional_sms(recipient, content):
                return False

        mail_recipient = settings.DEV_EMAIL_ADDRESS
        mail_content = mails_models.TransactionalWithoutTemplateEmailData(
            subject="Code de validation du téléphone",
            html_content=(
                f"<div>Le contenu suivant serait envoyé par sms au numéro {recipient}</div>"
                f"<div>{content}</div></div>"
            ),
        )

        try:
            user = users_models.User.query.filter(users_models.User.phoneNumber == recipient).one_or_none()
        except sa.orm.exc.MultipleResultsFound:
            logger.error("Several user accounts with the same phone number", extra={"phone_number": recipient})
        else:
            # Imported test users are whitelisted (Internal users, Bug Bounty, audit, etc.)
            if user is not None:
                if (
                    (user and user.has_test_role)
                    or recipient in settings.WHITELISTED_EMAIL_RECIPIENTS
                    or (settings.IS_STAGING and recipient.endswith("@yeswehack.ninja"))
                ):
                    mail_recipient = user.email

        return mails.send(recipients=[mail_recipient], data=mail_content)
