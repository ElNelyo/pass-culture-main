import logging

from flask import current_app as app
from flask import redirect
from flask import request

from pcapi import settings
from pcapi.core.users import models as user_models
from pcapi.core.users.external.educonnect import api as educonnect_api
from pcapi.core.users.external.educonnect import exceptions as educonnect_exceptions
from pcapi.models.api_errors import ApiErrors
from pcapi.routes.native.security import authenticated_user_required

from . import blueprint


logger = logging.getLogger(__name__)


@blueprint.saml_blueprint.route("educonnect/login", methods=["GET"])
@authenticated_user_required
def login_educonnect(user: user_models.User) -> None:
    redirect_url = educonnect_api.get_login_redirect_url(user)

    response = redirect(redirect_url, code=302)

    response.headers["Cache-Control"] = "no-cache, no-store"
    response.headers["Pragma"] = "no-cache"

    return response


@blueprint.saml_blueprint.route("acs", methods=["POST"])
def on_educonnect_authentication_response() -> None:
    try:
        educonnect_user = educonnect_api.get_educonnect_user(request.form["SAMLResponse"])
    except educonnect_exceptions.ResponseTooOld:
        raise ApiErrors({"saml_response": "Too old"})  # TODO: redirect user to error page
    except educonnect_exceptions.EduconnectAuthenticationException:
        raise ApiErrors()  # TODO: redirect user to error page

    user_id = app.redis_client.get(educonnect_user.saml_request_id)
    if user_id is None:
        raise ApiErrors({"saml_request_id": "user associated to saml_request_id not found"})
    user = user_models.User.query.get(user_id)

    logger.info(
        "Received educonnect authentication response",
        extra={
            "user_email": user.email,
            "date_of_birth": educonnect_user.birth_date.isoformat(),
            "educonnect_connection_date": educonnect_user.connection_datetime.isoformat(),
            "educonnect_id": educonnect_user.educonnect_id,
            "first_name": educonnect_user.first_name,
            "last_name": educonnect_user.last_name,
            "logout_url": educonnect_user.logout_url,
            "saml_request_id": educonnect_user.saml_request_id,
            "student_level": educonnect_user.student_level,
        },
    )

    # TODO: redirect user to the right page
    return redirect(settings.WEBAPP_V2_URL, code=302)
