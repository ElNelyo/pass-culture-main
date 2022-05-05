import datetime
from unittest.mock import patch

import pytest

from pcapi.connectors.cine_digital_service import ResourceCDS
import pcapi.connectors.serialization.cine_digital_service_serializers as cds_serializers
from pcapi.core.booking_providers.cds.client import CineDigitalServiceAPI
import pcapi.core.booking_providers.cds.exceptions as cds_exceptions


class CineDigitalServiceGetShowTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_show_corresponding_to_show_id(self, mocked_get_resource):
        # Given
        cinema_id = "cinemaid_test"
        token = "token_test"
        api_url = "apiUrl_test/"
        resource = ResourceCDS.SHOWS

        json_shows = [
            {
                "id": 1,
                "internet_remaining_place": 10,
                "showtime": datetime.datetime(2022, 3, 28),
                "is_cancelled": False,
                "is_deleted": False,
                "showsTariffPostypeCollection": [
                    {"tariffid": {"id": 96}},
                    {"tariffid": {"id": 3}},
                    {"tariffid": {"id": 2}},
                ],
            },
            {
                "id": 2,
                "internet_remaining_place": 30,
                "showtime": datetime.datetime(2022, 3, 29),
                "is_cancelled": False,
                "is_deleted": False,
                "showsTariffPostypeCollection": [
                    {"tariffid": {"id": 96}},
                ],
            },
            {
                "id": 3,
                "internet_remaining_place": 100,
                "showtime": datetime.datetime(2022, 3, 30),
                "is_cancelled": False,
                "is_deleted": False,
                "showsTariffPostypeCollection": [{"tariffid": {"id": 96}}],
            },
        ]
        mocked_get_resource.return_value = json_shows

        # when
        cine_digital_service = CineDigitalServiceAPI(
            cinema_id="cinemaid_test", token="token_test", api_url="apiUrl_test/"
        )
        show = cine_digital_service.get_show(2)

        # then
        mocked_get_resource.assert_called_once_with(api_url, cinema_id, token, resource)

        assert show.id == 2

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_raise_exception_if_show_not_found(self, mocked_get_resource):
        json_shows = [
            {
                "id": 1,
                "internet_remaining_place": 10,
                "showtime": datetime.datetime(2022, 3, 28),
                "is_cancelled": False,
                "is_deleted": False,
                "showsTariffPostypeCollection": [{"tariffid": {"id": 96}}],
            },
        ]
        mocked_get_resource.return_value = json_shows
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        with pytest.raises(cds_exceptions.CineDigitalServiceAPIException) as cds_exception:
            cine_digital_service.get_show(4)
        assert (
            str(cds_exception.value)
            == "Show #4 not found in Cine Digital Service API for cinemaId=test_id & url=test_url"
        )


class CineDigitalServiceGetShowsRemainingPlacesTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_shows_id_with_corresponding_remaining_places(self, mocked_get_resource):
        # Given
        cinema_id = "cinemaid_test"
        token = "token_test"
        api_url = "apiUrl_test/"
        resource = ResourceCDS.SHOWS

        json_shows = [
            {
                "id": 1,
                "internet_remaining_place": 10,
                "showtime": datetime.datetime(2022, 3, 28),
                "is_cancelled": False,
                "is_deleted": False,
                "showsTariffPostypeCollection": [
                    {"tariffid": {"id": 2}},
                ],
            },
            {
                "id": 2,
                "internet_remaining_place": 30,
                "showtime": datetime.datetime(2022, 3, 29),
                "is_cancelled": False,
                "is_deleted": False,
                "showsTariffPostypeCollection": [
                    {"tariffid": {"id": 2}},
                ],
            },
            {
                "id": 3,
                "internet_remaining_place": 100,
                "showtime": datetime.datetime(2022, 3, 30),
                "is_cancelled": False,
                "is_deleted": False,
                "showsTariffPostypeCollection": [
                    {"tariffid": {"id": 2}},
                ],
            },
        ]
        mocked_get_resource.return_value = json_shows

        # when
        cine_digital_service = CineDigitalServiceAPI(
            cinema_id="cinemaid_test", token="token_test", api_url="apiUrl_test/"
        )
        shows_remaining_places = cine_digital_service.get_shows_remaining_places([2, 3])

        # then
        mocked_get_resource.assert_called_once_with(api_url, cinema_id, token, resource)

        assert shows_remaining_places == {2: 30, 3: 100}


class CineDigitalServiceGetPaymentTypeTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_voucher_payment_type(self, mocked_get_resource):
        json_payment_types = [
            {
                "id": 21,
                "active": True,
                "internalcode": "VCH",
            },
            {
                "id": 22,
                "active": True,
                "internalcode": "OTHERPAYMENTYPE",
            },
        ]

        mocked_get_resource.return_value = json_payment_types
        cine_digital_service = CineDigitalServiceAPI(
            cinema_id="cinemaid_test", token="token_test", api_url="apiUrl_test"
        )

        payment_type = cine_digital_service.get_voucher_payment_type()

        assert payment_type.id == 21
        assert payment_type.internal_code == "VCH"

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_raise_exception_if_payment_type_not_found(self, mocked_get_resource):
        json_payment_types = [
            {
                "id": 23,
                "active": True,
                "internalcode": "OTHERPAYMENTYPE2",
            },
            {
                "id": 22,
                "active": True,
                "internalcode": "OTHERPAYMENTYPE",
            },
        ]
        mocked_get_resource.return_value = json_payment_types
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        with pytest.raises(cds_exceptions.CineDigitalServiceAPIException) as cds_exception:
            cine_digital_service.get_voucher_payment_type()
        assert (
            str(cds_exception.value)
            == "Pass Culture payment type not found in Cine Digital Service API for cinemaId=test_id & url=test_url"
        )


class CineDigitalServiceGetPCVoucherTypesTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_only_voucher_types_with_pass_culture_code_and_tariff(self, mocked_get_resource):
        json_voucher_types = [
            {"id": 1, "code": "TESTCODE", "tariffid": {"id": 2, "price": 5, "active": True, "labeltariff": ""}},
            {"id": 2, "code": "PSCULTURE", "tariffid": {"id": 3, "price": 5, "active": True, "labeltariff": ""}},
            {"id": 3, "code": "PSCULTURE", "tariffid": {"id": 4, "price": 6, "active": True, "labeltariff": ""}},
            {"id": 4, "code": "PSCULTURE"},
        ]

        mocked_get_resource.return_value = json_voucher_types
        cine_digital_service = CineDigitalServiceAPI(
            cinema_id="cinema_id_test", token="token_test", api_url="apiUrl_test"
        )
        pc_voucher_types = cine_digital_service.get_pc_voucher_types()

        assert len(pc_voucher_types) == 2
        assert pc_voucher_types[0].id == 2
        assert pc_voucher_types[0].code == "PSCULTURE"
        assert pc_voucher_types[0].tariff.id == 3
        assert pc_voucher_types[0].tariff.price == 5
        assert pc_voucher_types[1].id == 3
        assert pc_voucher_types[1].tariff.id == 4


class CineDigitalServiceGetTariffTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_tariffs_with_pass_culture_tariff(self, mocked_get_resource):
        json_tariffs = [
            {
                "id": 1,
                "price": 10,
                "label": "Pass Culture 5€",
                "is_active": True,
            },
            {
                "id": 2,
                "price": 3.5,
                "label": "Other tariff",
                "is_active": True,
            },
        ]
        mocked_get_resource.return_value = json_tariffs
        cine_digital_service = CineDigitalServiceAPI(
            cinema_id="cinema_id_test", token="token_test", api_url="apiUrl_test"
        )
        tariff = cine_digital_service.get_tariff()

        assert tariff.label == "Pass Culture 5€"

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_raise_exception_if_tariff_not_found(self, mocked_get_resource):
        json_tariffs = [
            {
                "id": 1,
                "price": 10,
                "label": "Another Tariff",
                "is_active": True,
            },
            {
                "id": 2,
                "price": 3.5,
                "label": "Other tariff",
                "is_active": True,
            },
        ]
        mocked_get_resource.return_value = json_tariffs
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        with pytest.raises(cds_exceptions.CineDigitalServiceAPIException) as cds_exception:
            cine_digital_service.get_tariff()
        assert (
            str(cds_exception.value)
            == "Tariff Pass Culture not found in Cine Digital Service API for cinemaId=test_id & url=test_url"
        )


class CineDigitalServiceGetScreenTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_screen_corresponding_to_screen_id(self, mocked_get_resource):
        json_screens = [
            {
                "id": 1,
                "seatmapfronttoback": True,
                "seatmaplefttoright": False,
                "seatmapskipmissingseats": False,
            },
            {
                "id": 2,
                "seatmapfronttoback": False,
                "seatmaplefttoright": True,
                "seatmapskipmissingseats": True,
            },
            {
                "id": 3,
                "seatmapfronttoback": True,
                "seatmaplefttoright": True,
                "seatmapskipmissingseats": True,
            },
        ]
        mocked_get_resource.return_value = json_screens
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        show = cine_digital_service.get_screen(2)

        assert show.id == 2

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_raise_exception_if_screen_not_found(self, mocked_get_resource):
        json_screens = [
            {
                "id": 1,
                "seatmapfronttoback": True,
                "seatmaplefttoright": False,
                "seatmapskipmissingseats": False,
            },
            {
                "id": 2,
                "seatmapfronttoback": False,
                "seatmaplefttoright": True,
                "seatmapskipmissingseats": True,
            },
            {
                "id": 3,
                "seatmapfronttoback": True,
                "seatmaplefttoright": True,
                "seatmapskipmissingseats": True,
            },
        ]
        mocked_get_resource.return_value = json_screens
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        with pytest.raises(cds_exceptions.CineDigitalServiceAPIException) as cds_exception:
            cine_digital_service.get_screen(4)
        assert (
            str(cds_exception.value)
            == "Screen #4 not found in Cine Digital Service API for cinemaId=test_id & url=test_url"
        )


class CineDigitalServiceGetAvailableSingleSeatTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_seat_available(self, mocked_get_resource):
        seatmap_json = [
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 3, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1],
        ]

        screen = cds_serializers.ScreenCDS(
            id=1,
            seatmapfronttoback=True,
            seatmaplefttoright=True,
            seatmapskipmissingseats=False,
        )

        mocked_get_resource.return_value = seatmap_json
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        best_seat = cine_digital_service.get_available_seat(1, screen)
        assert best_seat.seatRow == 5
        assert best_seat.seatCol == 6
        assert best_seat.seatNumber == "E_6"

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_seat_infos_according_to_screen(self, mocked_get_resource):
        seatmap_json = [
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 1, 0, 3],
            [3, 3, 3, 3, 0, 3],
        ]

        screen = cds_serializers.ScreenCDS(
            id=1,
            seatmapfronttoback=False,
            seatmaplefttoright=False,
            seatmapskipmissingseats=True,
        )

        mocked_get_resource.return_value = seatmap_json
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        best_seat = cine_digital_service.get_available_seat(1, screen)
        assert best_seat.seatRow == 2
        assert best_seat.seatCol == 2
        assert best_seat.seatNumber == "B_2"

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_None_if_no_seat_available(self, mocked_get_resource):
        seatmap_json = [
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
        ]

        screen = cds_serializers.ScreenCDS(
            id=1,
            seatmapfronttoback=True,
            seatmaplefttoright=True,
            seatmapskipmissingseats=False,
        )

        mocked_get_resource.return_value = seatmap_json
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        best_seat = cine_digital_service.get_available_seat(1, screen)
        assert best_seat is None


class CineDigitalServiceGetAvailableDuoSeatTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_duo_seat_if_available(self, mocked_get_resource):
        seatmap_json = [
            [1, 1, 1, 1, 0, 1],
            [1, 1, 1, 3, 0, 1],
            [1, 1, 3, 3, 0, 1],
            [1, 1, 3, 1, 0, 1],
            [1, 1, 1, 1, 0, 1],
        ]

        screen = cds_serializers.ScreenCDS(
            id=1,
            seatmapfronttoback=True,
            seatmaplefttoright=True,
            seatmapskipmissingseats=False,
        )

        mocked_get_resource.return_value = seatmap_json
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        duo_seats = cine_digital_service.get_available_duo_seat(1, screen)
        assert len(duo_seats) == 2
        assert duo_seats[0].seatNumber == "B_2"
        assert duo_seats[1].seatNumber == "B_3"

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_empty_if_less_than_two_seats_available(self, mocked_get_resource):
        seatmap_json = [
            [3, 3, 3, 3, 0, 1],
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
            [3, 3, 3, 3, 0, 3],
        ]

        screen = cds_serializers.ScreenCDS(
            id=1,
            seatmapfronttoback=True,
            seatmaplefttoright=True,
            seatmapskipmissingseats=False,
        )

        mocked_get_resource.return_value = seatmap_json
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        duo_seats = cine_digital_service.get_available_duo_seat(1, screen)
        assert len(duo_seats) == 0

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_two_separate_seats_if_no_duo_available(self, mocked_get_resource):
        seatmap_json = [
            [1, 3, 1, 3, 0, 1],
            [3, 3, 3, 3, 0, 3],
            [1, 3, 1, 3, 0, 1],
            [3, 3, 1, 3, 0, 3],
            [3, 1, 3, 1, 0, 1],
        ]

        screen = cds_serializers.ScreenCDS(
            id=1,
            seatmapfronttoback=True,
            seatmaplefttoright=True,
            seatmapskipmissingseats=False,
        )

        mocked_get_resource.return_value = seatmap_json
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")
        duo_seats = cine_digital_service.get_available_duo_seat(1, screen)
        assert len(duo_seats) == 2
        assert duo_seats[0].seatNumber == "C_3"
        assert duo_seats[1].seatNumber == "D_3"


class CineDigitalServiceCancelBookingTest:
    @patch("pcapi.core.booking_providers.cds.client.put_resource")
    def test_should_cancel_booking_with_success(self, mocked_put_resource):
        # Given
        json_response = {}
        mocked_put_resource.return_value = json_response
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")

        # When
        try:
            cine_digital_service.cancel_booking(["3107362853729", "1312079646868"])
        except cds_exceptions.CineDigitalServiceAPIException:
            assert False, "Should not raise exception"

    @patch("pcapi.core.booking_providers.cds.client.put_resource")
    def test_should_cancel_booking_with_errors_for_each_barcode(self, mocked_put_resource):
        # Given
        json_response = {
            "111111111111": "BARCODE_NOT_FOUND",
            "222222222222": "TICKET_ALREADY_CANCELED",
            "333333333333": "AFTER_END_OF_DAY",
            "444444444444": "AFTER_END_OF_SHOW",
            "555555555555": "DAY_CLOSED",
        }
        mocked_put_resource.return_value = json_response
        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")

        # When
        with pytest.raises(cds_exceptions.CineDigitalServiceAPIException) as exception:
            cine_digital_service.cancel_booking(
                ["111111111111", "222222222222", "333333333333", "444444444444", "555555555555"]
            )
        sep = "\n"
        assert (
            str(exception.value)
            == f"""Error while canceling bookings :{sep}111111111111 : BARCODE_NOT_FOUND{sep}222222222222 : TICKET_ALREADY_CANCELED{sep}333333333333 : AFTER_END_OF_DAY{sep}444444444444 : AFTER_END_OF_SHOW{sep}555555555555 : DAY_CLOSED"""
        )


class CineDigitalServiceGetVoucherForShowTest:
    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_none_when_show_does_not_have_pass_culture_tariff(self, mocked_get_resource):
        show = cds_serializers.ShowCDS(
            id=1,
            is_cancelled=False,
            is_deleted=False,
            internet_remaining_place=20,
            showtime=datetime.datetime.utcnow(),
            shows_tariff_pos_type_collection=[cds_serializers.ShowTariffCDS(tariff=cds_serializers.IdObjectCDS(id=5))],
        )
        json_voucher_types = [
            {"id": 1, "code": "TESTCODE", "tariffid": {"id": 2, "price": 5, "active": True, "labeltariff": ""}},
            {"id": 2, "code": "PSCULTURE", "tariffid": {"id": 3, "price": 6, "active": True, "labeltariff": ""}},
        ]

        mocked_get_resource.return_value = json_voucher_types

        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")

        voucher_type = cine_digital_service.get_voucher_type_for_show(show)
        print("voucher_type", voucher_type)
        assert not voucher_type

    @patch("pcapi.core.booking_providers.cds.client.get_resource")
    def test_should_return_psculture_voucher_with_the_lower_price(self, mocked_get_resource):
        show = cds_serializers.ShowCDS(
            id=1,
            is_cancelled=False,
            is_deleted=False,
            internet_remaining_place=20,
            showtime=datetime.datetime.utcnow(),
            shows_tariff_pos_type_collection=[
                cds_serializers.ShowTariffCDS(tariff=cds_serializers.IdObjectCDS(id=3)),
                cds_serializers.ShowTariffCDS(tariff=cds_serializers.IdObjectCDS(id=2)),
            ],
        )
        json_voucher_types = [
            {"id": 1, "code": "PSCULTURE", "tariffid": {"id": 2, "price": 5, "active": True, "labeltariff": ""}},
            {"id": 2, "code": "PSCULTURE", "tariffid": {"id": 3, "price": 6, "active": True, "labeltariff": ""}},
        ]

        mocked_get_resource.return_value = json_voucher_types

        cine_digital_service = CineDigitalServiceAPI(cinema_id="test_id", token="token_test", api_url="test_url")

        voucher_type = cine_digital_service.get_voucher_type_for_show(show)
        print("voucher_type", voucher_type)
        assert voucher_type.id == 1
        assert voucher_type.tariff.id == 2
        assert voucher_type.tariff.price == 5
