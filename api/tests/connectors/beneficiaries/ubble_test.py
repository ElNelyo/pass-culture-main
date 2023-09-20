import json
import logging

import pytest

from pcapi.connectors.beneficiaries import ubble
from pcapi.core.fraud import models as fraud_models
from pcapi.core.testing import assert_num_queries
from pcapi.core.testing import override_features
from pcapi.core.testing import override_settings
from pcapi.core.users.models import GenderEnum
from pcapi.utils import requests as requests_utils

from tests.core.subscription.test_factories import UbbleIdentificationResponseFactory
from tests.test_utils import json_default


class StartIdentificationTest:
    def test_start_identification(self, ubble_mock, caplog):
        with caplog.at_level(logging.INFO):
            response = ubble.start_identification(
                user_id=123,
                first_name="prenom",
                last_name="nom",
                webhook_url="http://webhook/url/",
                redirect_url="http://redirect/url",
            )

        assert isinstance(response, fraud_models.UbbleContent)
        assert ubble_mock.call_count == 1

        attributes = ubble_mock.last_request.json()["data"]["attributes"]
        assert attributes["identification-form"]["external-user-id"] == 123
        assert attributes["identification-form"]["phone-number"] is None

        assert attributes["reference-data"]["first-name"] == "prenom"
        assert attributes["reference-data"]["last-name"] == "nom"
        assert attributes["webhook"] == "http://webhook/url/"
        assert attributes["redirect_url"] == "http://redirect/url"

        assert len(caplog.records) >= 1
        record = caplog.records[1]
        assert record.extra["status_code"] == 201
        assert record.extra["identification_id"] == str(response.identification_id)
        assert record.extra["request_type"] == "start-identification"
        assert record.message == "Valid response from Ubble"

    def test_start_identification_connection_error(self, ubble_mock_connection_error, caplog):
        with pytest.raises(requests_utils.ExternalAPIException):
            with caplog.at_level(logging.ERROR):
                ubble.start_identification(
                    user_id=123,
                    first_name="prenom",
                    last_name="nom",
                    webhook_url="http://webhook/url/",
                    redirect_url="http://redirect/url",
                )

        assert ubble_mock_connection_error.call_count == 1
        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.extra["request_type"] == "start-identification"
        assert record.extra["error_type"] == "network"
        assert record.message == "Ubble start-identification: Network error"

    def test_start_identification_http_error_status(self, ubble_mock_http_error_status, caplog):
        with pytest.raises(requests_utils.ExternalAPIException):
            ubble.start_identification(
                user_id=123,
                first_name="prenom",
                last_name="nom",
                webhook_url="http://webhook/url/",
                redirect_url="http://redirect/url",
            )

        assert ubble_mock_http_error_status.call_count == 1
        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.extra["status_code"] == 401
        assert record.extra["request_type"] == "start-identification"
        assert record.extra["error_type"] == "http"
        assert record.message == "Ubble start-identification: Unexpected error: 401, "


class BuildUrlTest:
    @override_features(WIP_ENABLE_MOCK_UBBLE=True)
    @override_settings(UBBLE_MOCK_API_URL="http://example.com")
    def test_use_mock_api_if_ff_enabled_and_url_set(self):
        url = ubble.build_url("")

        assert url == "http://example.com"

    @override_features(WIP_ENABLE_MOCK_UBBLE=False)
    @override_settings(UBBLE_MOCK_API_URL="http://example.com")
    def test_use_real_ubble_if_ff_disabled_and_url_set(self):
        url = ubble.build_url("")

        assert url == "https://api.ubble.ai"

    @override_features(WIP_ENABLE_MOCK_UBBLE=True)
    @override_settings(UBBLE_MOCK_API_URL="")
    def test_use_real_ubble_if_ff_enabled_and_url_unset(self):
        with assert_num_queries(0):
            url = ubble.build_url("")

        assert url == "https://api.ubble.ai"


class GetContentTest:
    def test_get_content(self, ubble_mocker, caplog):
        ubble_response = UbbleIdentificationResponseFactory()
        with ubble_mocker(
            ubble_response.data.attributes.identification_id,
            json.dumps(ubble_response.dict(by_alias=True), sort_keys=True, default=json_default),
        ):
            with caplog.at_level(logging.INFO):
                ubble.get_content(ubble_response.data.attributes.identification_id)

            assert caplog.records[0].message == "External service called"

            supervision_record = caplog.records[1]
            assert supervision_record.message == "Valid response from Ubble"
            assert supervision_record.extra["status_code"] == 200
            assert supervision_record.extra["identification_id"] == ubble_response.data.attributes.identification_id
            assert supervision_record.extra["status"] == ubble_response.data.attributes.status.value
            assert not supervision_record.extra["score"]
            assert supervision_record.extra["request_type"] == "get-content"

    def test_get_content_http_error(self, requests_mock, caplog):
        identification_id = "some-id"
        requests_mock.register_uri("GET", f"/identifications/{identification_id}/", status_code=401)

        with caplog.at_level(logging.ERROR):
            with pytest.raises(requests_utils.ExternalAPIException) as exc_info:
                ubble.get_content(identification_id)

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.message == "Ubble get-content: Unexpected error: 401, "
        assert record.extra["status_code"] == 401
        assert record.extra["identification_id"] == identification_id
        assert record.extra["request_type"] == "get-content"
        assert record.extra["error_type"] == "http"
        assert exc_info.value.is_retryable is False

    def test_get_content_network_error(self, requests_mock, caplog):
        identification_id = "some-id"
        requests_mock.register_uri("GET", f"/identifications/{identification_id}/", status_code=503)

        with caplog.at_level(logging.ERROR):
            with pytest.raises(requests_utils.ExternalAPIException) as exc_info:
                ubble.get_content(identification_id)

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.message == "Ubble get-content: External error: 503"
        assert record.extra["status_code"] == 503
        assert record.extra["identification_id"] == identification_id
        assert record.extra["request_type"] == "get-content"
        assert record.extra["error_type"] == "http"
        assert exc_info.value.is_retryable is True


class HelperFunctionsTest:
    @pytest.mark.parametrize(
        "ubble_gender, expected",
        [
            ("M", GenderEnum.M),
            ("F", GenderEnum.F),
            ("X", None),
            (None, None),
        ],
    )
    def test_parse_ubble_gender(self, ubble_gender, expected):
        assert ubble._parse_ubble_gender(ubble_gender) == expected
