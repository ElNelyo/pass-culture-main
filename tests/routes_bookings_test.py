from datetime import datetime, timedelta
from urllib.parse import urlencode

import pytest
import requests as req

from models import Offerer, PcObject, EventType
from models.db import db
from models.pc_object import serialize
from tests.conftest import clean_database
from utils.human_ids import humanize
from utils.test_utils import API_URL, req_with_auth, create_stock_with_thing_offer, \
    create_thing_offer, create_deposit, create_stock_with_event_offer, create_venue, create_offerer, \
    create_recommendation, create_user, create_booking, create_event_offer, \
    create_event_occurrence, create_stock_from_event_occurrence, create_user_offerer


@clean_database
@pytest.mark.standalone
def test_create_booking_should_not_work_past_limit_date(app):
    offerer = create_offerer('987654321', 'Test address', 'Test city', '93000', 'Test name')

    venue = create_venue(offerer, 'Test offerer', 'reservations@test.fr', '123 rue test', '93000', 'Test city', '93')

    thing_offer = create_thing_offer(venue)

    expired_stock = create_stock_with_thing_offer(offerer=offerer, venue=venue, thing_offer=thing_offer, price=0)
    expired_stock.bookingLimitDatetime = datetime.utcnow() - timedelta(seconds=1)
    PcObject.check_and_save(expired_stock)

    user = create_user(email='test@mail.com', password='psswd123')
    PcObject.check_and_save(user)

    recommendation = create_recommendation(thing_offer, user)

    booking_json = {
        'stockId': humanize(expired_stock.id),
        'recommendationId': humanize(recommendation.id),
        'quantity': 1
    }

    r_create = req_with_auth('test@mail.com', password='psswd123').post(API_URL + '/bookings', json=booking_json)
    assert r_create.status_code == 400
    assert 'global' in r_create.json()
    assert 'date limite' in r_create.json()['global'][0]


@clean_database
@pytest.mark.standalone
def test_create_booking_should_work_before_limit_date(app):
    offerer = create_offerer('987654321', 'Test address', 'Test city', '93000', 'Test name')
    venue = create_venue(offerer, 'Test offerer', 'reservations@test.fr', '123 rue test', '93000', 'Test city', '93')
    ok_stock = create_stock_with_event_offer(offerer=offerer,
                                             venue=venue, price=0)
    ok_stock.bookingLimitDatetime = datetime.utcnow() + timedelta(minutes=2)
    ok_stock.bookingLimitDatetime = datetime.utcnow() + timedelta(minutes=2)
    PcObject.check_and_save(ok_stock)

    user = create_user(email='test@mail.com', password='psswd123')
    PcObject.check_and_save(user)

    recommendation = create_recommendation(offer=ok_stock.offer, user=user)
    PcObject.check_and_save(recommendation)

    booking_json = {
        'stockId': humanize(ok_stock.id),
        'recommendationId': humanize(recommendation.id),
        'quantity': 1
    }

    r_create = req_with_auth(email='test@mail.com', password='psswd123').post(API_URL + '/bookings', json=booking_json)
    assert r_create.status_code == 201
    id = r_create.json()['id']
    r_check = req_with_auth(email='test@mail.com', password='psswd123').get(API_URL + '/bookings/' + id)
    created_booking_json = r_check.json()
    for (key, value) in booking_json.items():
        assert created_booking_json[key] == booking_json[key]


@clean_database
@pytest.mark.standalone
def test_create_booking_should_not_work_if_too_many_bookings(app):
    offerer = create_offerer('987654321', 'Test address', 'Test city', '93000', 'Test name')
    venue = create_venue(offerer, 'Test offerer', 'reservations@test.fr', '123 rue test', '93000', 'Test city', '93')
    too_many_bookings_stock = create_stock_with_thing_offer(offerer=Offerer(), venue=venue, thing_offer=None,
                                                            available=2)

    user = create_user(email='test@email.com', password='mdppsswd')

    deposit = create_deposit(user, datetime.utcnow(), amount=50)

    recommendation = create_recommendation(offer=too_many_bookings_stock.offer, user=user)
    booking = create_booking(user, too_many_bookings_stock, venue, quantity=2)

    PcObject.check_and_save(booking, recommendation, user, deposit)

    booking_json = {
        'stockId': humanize(too_many_bookings_stock.id),
        'recommendationId': humanize(recommendation.id),
        'quantity': 1
    }

    r_create = req_with_auth('test@email.com', 'mdppsswd').post(API_URL + '/bookings', json=booking_json)

    assert r_create.status_code == 400
    assert 'global' in r_create.json()
    assert 'quantité disponible' in r_create.json()['global'][0]


@clean_database
@pytest.mark.standalone
def test_create_booking_should_work_if_user_can_book_and_enough_credit(app):
    # Given
    offerer = create_offerer('819202819', '1 Fake Address', 'Fake city', '93000', 'Fake offerer')
    venue = create_venue(offerer, 'venue name', 'booking@email.com', '1 fake street', '93000', 'False city', '93')
    thing_offer = create_thing_offer(venue)

    user = create_user(email='test@email.com', password='mdppsswd')
    PcObject.check_and_save(user)

    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=50, available=1)
    PcObject.check_and_save(stock)

    recommendation = create_recommendation(thing_offer, user)
    PcObject.check_and_save(recommendation)

    deposit = create_deposit(user, datetime.utcnow(), amount=50)
    PcObject.check_and_save(deposit)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': humanize(recommendation.id),
        'quantity': 1
    }
    r_create = req_with_auth('test@email.com', 'mdppsswd').post(API_URL + '/bookings', json=booking_json)
    assert r_create.status_code == 201


@clean_database
@pytest.mark.standalone
def test_create_booking_should_work_if_canceled_bookings_user_can_book_and_enough_credit_(app):
    # Given
    offerer = create_offerer('819202819', '1 Fake Address', 'Fake city', '93000', 'Fake offerer')
    venue = create_venue(offerer, 'venue name', 'booking@email.com', '1 fake street', '93000', 'False city', '93')
    thing_offer = create_thing_offer(venue)

    user = create_user(email='test@email.com', password='mdppsswd')
    PcObject.check_and_save(user)

    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=50, available=1)
    PcObject.check_and_save(stock)

    booking = create_booking(user, stock, venue, is_cancelled=True)
    PcObject.check_and_save(booking)

    recommendation = create_recommendation(thing_offer, user)
    PcObject.check_and_save(recommendation)

    deposit = create_deposit(user, datetime.utcnow(), amount=50)
    PcObject.check_and_save(deposit)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': humanize(recommendation.id),
        'quantity': 1
    }
    r_create = req_with_auth('test@email.com', 'mdppsswd').post(API_URL + '/bookings', json=booking_json)
    assert r_create.status_code == 201


@clean_database
@pytest.mark.standalone
def test_create_booking_should_not_work_for_free_offer_if_not_userCanBookFreeOffers(app):
    # Given
    user = create_user(email='cannotBook_freeOffers@email.com', can_book_free_offers=False, password='testpsswd')
    PcObject.check_and_save(user)

    offerer = create_offerer(siren='899999768', address='2 Test adress', city='Test city', postal_code='93000',
                             name='Test offerer')
    PcObject.check_and_save(offerer)

    venue = create_venue(offerer=offerer, name='Venue name', booking_email='booking@email.com',
                         address='1 Test address', postal_code='93000', city='Test city', departement_code='93')
    PcObject.check_and_save(venue)

    thing_offer = create_thing_offer(venue)
    PcObject.check_and_save(thing_offer)

    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=0)
    PcObject.check_and_save(stock)

    recommendation = create_recommendation(thing_offer, user)
    PcObject.check_and_save(recommendation)

    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=500)
    PcObject.check_and_save(deposit)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': humanize(recommendation.id),
        'quantity': 1
    }

    # When
    r_create = req_with_auth('cannotBook_freeOffers@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                                  json=booking_json)

    # Then
    assert r_create.status_code == 400
    assert 'cannotBookFreeOffers' in r_create.json()


@clean_database
@pytest.mark.standalone
def test_create_booking_should_not_work_if_not_enough_credit(app):
    # Given
    user = create_user(email='insufficient_funds_test@email.com', password='testpsswd')
    offerer = create_offerer(siren='899999768', address='2 Test adress', city='Test city', postal_code='93000',
                             name='Test offerer')
    venue = create_venue(offerer=offerer, name='Venue name', booking_email='booking@email.com',
                         address='1 Test address', postal_code='93000', city='Test city', departement_code='93')
    stock = create_stock_with_event_offer(offerer, venue, price=200)
    event_offer = stock.resolvedOffer
    recommendation = create_recommendation(event_offer, user)
    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=0)

    PcObject.check_and_save(recommendation)
    PcObject.check_and_save(stock)
    PcObject.check_and_save(deposit)

    booking_json = {
        "stockId": humanize(stock.id),
        "recommendationId": humanize(recommendation.id),
        "quantity": 1
    }

    # When
    r_create = req_with_auth('insufficient_funds_test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                                    json=booking_json)

    # Then
    assert r_create.status_code == 400
    assert 'insufficientFunds' in r_create.json()


@clean_database
@pytest.mark.standalone
def test_create_booking_should_work_if_enough_credit_when_userCanBookFreeOffers(app):
    # Given
    user = create_user(email='sufficient_funds@email.com', password='testpsswd')
    PcObject.check_and_save(user)

    offerer = create_offerer(siren='899999768', address='2 Test adress', city='Test city', postal_code='93000',
                             name='Test offerer')
    PcObject.check_and_save(offerer)

    venue = create_venue(offerer, 'Test offerer', 'reservations@test.fr', '123 rue test', '93000', 'Test city', '93')
    PcObject.check_and_save(venue)

    thing_offer = create_thing_offer(venue)
    PcObject.check_and_save(thing_offer)

    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=5)
    PcObject.check_and_save(stock)

    recommendation = create_recommendation(thing_offer, user)
    PcObject.check_and_save(recommendation)

    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=9)
    PcObject.check_and_save(deposit)

    booking_json = {
        "stockId": humanize(stock.id),
        "recommendationId": humanize(recommendation.id),
        "quantity": 1
    }

    # When
    r_create = req_with_auth('sufficient_funds@email.com', 'testpsswd').post(API_URL + '/bookings', json=booking_json)

    # Then
    r_create_json = r_create.json()
    assert r_create.status_code == 201
    assert r_create_json['amount'] == 5.0
    assert r_create_json['quantity'] == 1


@clean_database
@pytest.mark.standalone
def test_create_booking_should_work_for_paid_offer_if_user_can_not_book_but_has_enough_credit(app):
    user = create_user(email='can_book_paid_offers@email.com', can_book_free_offers=False, password='testpsswd')
    PcObject.check_and_save(user)

    offerer = create_offerer(siren='899999768', address='2 Test adress', city='Test city', postal_code='93000',
                             name='Test offerer')
    PcObject.check_and_save(offerer)

    venue = create_venue(offerer, 'Test offerer', 'reservations@test.fr', '123 rue test', '93000', 'Test city', '93')
    PcObject.check_and_save(venue)

    thing_offer = create_thing_offer(venue)
    PcObject.check_and_save(thing_offer)

    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=10)
    PcObject.check_and_save(stock)

    recommendation = create_recommendation(thing_offer, user)
    PcObject.check_and_save(recommendation)

    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=500)
    PcObject.check_and_save(deposit)

    booking_json = {
        "stockId": humanize(stock.id),
        "recommendationId": humanize(recommendation.id),
        "quantity": 1
    }

    # When
    r_create = req_with_auth('can_book_paid_offers@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                                 json=booking_json)
    r_create_json = r_create.json()

    # Then
    assert r_create.status_code == 201
    assert r_create_json['amount'] == 10.0
    assert r_create_json['quantity'] == 1


@clean_database
@pytest.mark.standalone
def test_create_booking_should_not_work_if_only_public_credit_and_100_euros_limit_physical_thing_reached(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    PcObject.check_and_save(user)

    offerer = create_offerer()
    PcObject.check_and_save(offerer)

    venue = create_venue(offerer)
    PcObject.check_and_save(venue)

    thing_offer = create_thing_offer(venue)
    PcObject.check_and_save(thing_offer)

    stock_1 = create_stock_with_thing_offer(offerer, venue, thing_offer, price=90)
    stock_2 = create_stock_with_thing_offer(offerer, venue, thing_offer, price=9)
    PcObject.check_and_save(stock_1, stock_2)

    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=500, source='public')
    PcObject.check_and_save(deposit)

    booking_1 = create_booking(user, stock_1, venue, recommendation=None)
    PcObject.check_and_save(booking_1)

    recommendation = create_recommendation(thing_offer, user)
    PcObject.check_and_save(recommendation)

    booking_json = {
        "stockId": humanize(stock_2.id),
        "recommendationId": humanize(recommendation.id),
        "quantity": 2
    }

    # When
    response = req_with_auth('test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                 json=booking_json)
    # Then
    error_message = response.json()
    assert response.status_code == 400
    assert error_message['global'] == ['La limite de 100 € pour les biens culturels ' \
                                       'ne vous permet pas de réserver']


@clean_database
@pytest.mark.standalone
def test_create_booking_returns_bad_request_if_no_stock_id_is_given(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    PcObject.check_and_save(user)
    booking_json = {
        'stockId': None,
        'recommendationId': 'AFQA',
        'quantity': 2
    }

    # When
    response = req_with_auth('test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                 json=booking_json)
    # Then
    error_message = response.json()
    assert response.status_code == 400
    assert error_message['stockId'] == ['Vous devez préciser un identifiant d\'offre']


@clean_database
@pytest.mark.standalone
def test_create_booking_returns_bad_request_if_no_quantity_is_given(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    PcObject.check_and_save(user)
    booking_json = {
        'stockId': 'AE',
        'recommendationId': 'AFQA',
        'quantity': None
    }

    # When
    response = req_with_auth('test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                 json=booking_json)
    # Then
    error_message = response.json()
    assert response.status_code == 400
    assert error_message['quantity'] == ['Vous devez préciser une quantité pour la réservation']


@clean_database
@pytest.mark.standalone
def test_create_booking_returns_bad_request_if_negative_quantity_is_given(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    thing_offer = create_thing_offer(venue)
    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=90)
    PcObject.check_and_save(stock, user)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': None,
        'quantity': -3
    }

    # When
    response = req_with_auth('test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                 json=booking_json)
    # Then
    error_message = response.json()
    assert response.status_code == 400
    assert error_message['quantity'] == ['Vous devez préciser une quantité pour la réservation']


@clean_database
@pytest.mark.standalone
def test_create_booking_returns_bad_request_if_offer_is_inactive(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    thing_offer = create_thing_offer(venue)
    thing_offer.isActive = False
    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=90)
    PcObject.check_and_save(stock, user)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': None,
        'quantity': 1,
    }

    # When
    response = req_with_auth('test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                 json=booking_json)
    # Then
    error_message = response.json()
    assert response.status_code == 400
    assert error_message['stockId'] == ["Cette offre a été retirée. Elle n'est plus valable."]


@clean_database
@pytest.mark.standalone
def test_create_booking_returns_bad_request_if_offerer_is_inactive(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    thing_offer = create_thing_offer(venue)
    offerer.isActive = False
    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=90)
    PcObject.check_and_save(stock, user)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': None,
        'quantity': 1,
    }

    # When
    response = req_with_auth('test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                 json=booking_json)
    # Then
    error_message = response.json()
    assert response.status_code == 400
    assert error_message['stockId'] == ["Cette offre a été retirée. Elle n'est plus valable."]


@clean_database
@pytest.mark.standalone
def test_create_booking_returns_bad_request_if_stock_is_soft_deleted(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    thing_offer = create_thing_offer(venue)
    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=90)
    stock.isSoftDeleted = True
    PcObject.check_and_save(stock, user)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': None,
        'quantity': 1,
    }

    # When
    response = req_with_auth('test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                 json=booking_json)
    # Then
    error_message = response.json()
    assert response.status_code == 400
    assert error_message['stockId'] == ["Cette date a été retirée. Elle n'est plus disponible."]


@clean_database
@pytest.mark.standalone
def test_create_booking_returns_bad_request_if_null_quantity_is_given(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    thing_offer = create_thing_offer(venue)
    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=90)
    PcObject.check_and_save(stock, user)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': None,
        'quantity': 0
    }

    # When
    response = req_with_auth('test@email.com', 'testpsswd').post(API_URL + '/bookings',
                                                                 json=booking_json)
    # Then
    error_message = response.json()
    assert response.status_code == 400
    assert error_message['quantity'] == ['Vous devez préciser une quantité pour la réservation']


@clean_database
@pytest.mark.standalone
def test_patch_booking_returns_400_when_it_is_not_is_cancelled_true_key(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=500)
    booking = create_booking(user, quantity=1)
    PcObject.check_and_save(user, deposit, booking)

    # When
    response = req_with_auth(user.email, user.clearTextPassword) \
        .patch(API_URL + '/bookings/' + humanize(booking.id), json={"quantity": 3})

    # Then
    assert response.status_code == 400
    db.session.refresh(booking)
    assert booking.quantity == 1


@clean_database
@pytest.mark.standalone
def test_patch_booking_returns_400_when_is_cancelled_false_key(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=500)
    booking = create_booking(user)
    booking.isCancelled = True
    PcObject.check_and_save(user, deposit, booking)

    # When
    response = req_with_auth(user.email, user.clearTextPassword) \
        .patch(API_URL + '/bookings/' + humanize(booking.id), json={"isCancelled": False})

    # Then
    assert response.status_code == 400
    db.session.refresh(booking)
    assert booking.isCancelled


@clean_database
@pytest.mark.standalone
def test_cancel_booking_returns_200_and_effectively_marks_the_booking_as_cancelled(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=500)
    booking = create_booking(user)
    PcObject.check_and_save(user, deposit, booking)

    # When
    response = req_with_auth(user.email, user.clearTextPassword) \
        .patch(API_URL + '/bookings/' + humanize(booking.id), json={"isCancelled": True})

    # Then
    assert response.status_code == 200
    db.session.refresh(booking)
    assert booking.isCancelled


@clean_database
@pytest.mark.standalone
def test_cancel_booking_returns_404_if_booking_does_not_exist(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    PcObject.check_and_save(user)

    # When
    response = req_with_auth(user.email, user.clearTextPassword) \
        .patch(API_URL + '/bookings/AX', json={"isCancelled": True})

    # Then
    assert response.status_code == 404


@clean_database
@pytest.mark.standalone
def test_cancel_booking_for_other_users_returns_403_and_does_not_mark_the_booking_as_cancelled(app):
    # Given
    other_user = create_user(email='test2@email.com', password='testpsswd')
    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(other_user, deposit_date, amount=500)
    booking = create_booking(other_user)
    user = create_user(email='test@email.com', password='testpsswd')
    PcObject.check_and_save(user, other_user, deposit, booking)

    # When
    response = req_with_auth(user.email, user.clearTextPassword) \
        .patch(API_URL + '/bookings/' + humanize(booking.id), json={"isCancelled": True})

    # Then
    assert response.status_code == 403
    db.session.refresh(booking)
    assert not booking.isCancelled


@clean_database
@pytest.mark.standalone
def test_an_admin_cancelling_a_users_booking_returns_200_and_effectively_marks_the_booking_as_cancelled(app):
    # Given
    admin_user = create_user(email='test@email.com', can_book_free_offers=False, password='testpsswd', is_admin=True)
    other_user = create_user(email='test2@email.com', password='testpsswd')
    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(other_user, deposit_date, amount=500)
    booking = create_booking(other_user)
    PcObject.check_and_save(admin_user, other_user, deposit, booking)

    # When
    response = req_with_auth(admin_user.email, admin_user.clearTextPassword) \
        .patch(API_URL + '/bookings/' + humanize(booking.id), json={"isCancelled": True})

    # Then
    assert response.status_code == 200
    db.session.refresh(booking)
    assert booking.isCancelled


@pytest.mark.standalone
class GetBookingByTokenTest:
    @clean_database
    def test_when_user_has_rights_and_regular_offer_returns_status_code_200_user_and_booking_data(self, app):
        # Given
        user = create_user(public_name='John Doe', email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(admin_user, offerer)
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name', event_type=EventType.CINEMA)
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(user_offerer, booking, event_occurrence)

        expected_json = {'bookingId': humanize(booking.id),
                         'date': serialize(booking.stock.eventOccurrence.beginningDatetime),
                         'email': 'user@email.fr',
                         'isUsed': False,
                         'offerName': 'Event Name',
                         'userName': 'John Doe',
                         'venueDepartementCode': '93'}

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').get(API_URL + '/bookings/token/{}'.format(booking.token))
        # Then
        assert response.status_code == 200
        response_json = response.json()
        assert response_json == expected_json

    @clean_database
    def test_when_activation_event_and_user_has_rights_returns_user_and_booking_data_with_phone_number_and_date_of_birth(
            self, app):
        # Given
        user = create_user(email='user@email.fr', phone_number='0698765432', date_of_birth=datetime(2001, 2, 1))
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd', is_admin=True, can_book_free_offers=False)
        offerer = create_offerer()
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Offre d\'activation', event_type=EventType.ACTIVATION)
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(admin_user, booking, event_occurrence)

        expected_json = {'bookingId': humanize(booking.id),
                         'date': serialize(booking.stock.eventOccurrence.beginningDatetime),
                         'dateOfBirth': '2001-02-01T00:00:00Z',
                         'email': 'user@email.fr',
                         'isUsed': False,
                         'offerName': 'Offre d\'activation',
                         'phoneNumber': '0698765432',
                         'userName': 'John Doe',
                         'venueDepartementCode': '93'}

        # When
        url = API_URL + '/bookings/token/{}'.format(booking.token)
        response = req_with_auth('admin@email.fr', 'P@55w0rd').get(url)
        # Then
        assert response.status_code == 200
        response_json = response.json()
        assert response_json == expected_json

    @clean_database
    def test_when_user_has_rights_and_email_with_special_characters_url_encoded_returns_status_code_200(self, app):
        # Given
        user = create_user(email='user+plus@email.fr')
        user_admin = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(user_admin, offerer, is_admin=True)
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(user_offerer, booking, event_occurrence)
        url_email = urlencode({'email': 'user+plus@email.fr'})
        url = API_URL + '/bookings/token/{}?{}'.format(booking.token, url_email)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').get(url)
        # Then
        assert response.status_code == 200

    @clean_database
    def test_when_user_doesnt_have_rights_returns_status_code_204(self, app):
        # Given
        user = create_user(email='user@email.fr')
        querying_user = create_user(email='querying@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(querying_user, booking, event_occurrence)

        # When
        response = req_with_auth('querying@email.fr', 'P@55w0rd').get(
            API_URL + '/bookings/token/{}'.format(booking.token))
        # Then
        assert response.status_code == 204

    @clean_database
    def test_when_user_not_logged_in_and_gives_right_email_returns_204(self, app):
        # Given
        user = create_user(email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(admin_user, booking, event_occurrence)

        url = API_URL + '/bookings/token/{}?email={}'.format(booking.token, 'user@email.fr')
        # When
        response = req.get(url, headers={'origin': 'http://localhost:3000'})
        # Then
        assert response.status_code == 204

    @clean_database
    def test_when_user_not_logged_in_and_give_right_email_and_event_offer_id_returns_204(self, app):
        # Given
        user = create_user(email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(admin_user, booking, event_occurrence)
        url = API_URL + '/bookings/token/{}?email={}&offer_id={}'.format(booking.token, 'user@email.fr',
                                                                         humanize(offer.id))

        # When
        response = req.get(url, headers={'origin': 'http://localhost:3000'})
        # Then
        assert response.status_code == 204

    @clean_database
    def test_when_not_logged_in_and_give_right_email_and_offer_id_thing_returns_204(self, app):
        # Given
        user = create_user(email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_thing_offer(offerer, venue, thing_offer=None, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(admin_user, booking)
        url = API_URL + '/bookings/token/{}?email={}&offer_id={}'.format(booking.token, 'user@email.fr',
                                                                         humanize(stock.offerId))

        # When
        response = req.get(url, headers={'origin': 'http://localhost:3000'})
        # Then
        assert response.status_code == 204

    @clean_database
    def test_when_token_user_has_rights_but_token_not_found_returns_status_code_404_and_global_error(self, app):
        # Given
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        PcObject.check_and_save(admin_user)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').get(API_URL + '/bookings/token/{}'.format('12345'))
        # Then
        assert response.status_code == 404
        assert response.json()['global'] == ["Cette contremarque n'a pas été trouvée"]

    @clean_database
    def test_when_user_not_logged_in_and_wrong_email_returns_404_and_global_in_error(self, app):
        # Given
        user = create_user(email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(admin_user, booking, event_occurrence)

        # When
        url = API_URL + '/bookings/token/{}?email={}'.format(booking.token, 'toto@email.fr')
        response = req_with_auth('admin@email.fr', 'P@55w0rd').get(url)
        # Then
        assert response.status_code == 404
        assert response.json()['global'] == ["Cette contremarque n'a pas été trouvée"]

    @clean_database
    def test_when_user_not_logged_in_right_email_and_wrong_offer_returns_404_and_global_in_error(self, app):
        # Given
        user = create_user(email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_thing_offer(offerer, venue, thing_offer=None, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(admin_user, booking)
        url = API_URL + '/bookings/token/{}?email={}&offer_id={}'.format(booking.token, 'user@email.fr', humanize(123))

        # When
        response = req.get(url, headers={'origin': 'http://localhost:3000'})
        # Then
        assert response.status_code == 404
        assert response.json()['global'] == ["Cette contremarque n'a pas été trouvée"]

    @clean_database
    def test_when_user_has_rights_and_email_with_special_characters_not_url_encoded_returns_404(self, app):
        # Given
        user = create_user(email='user+plus@email.fr')
        user_admin = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(user_admin, offerer, is_admin=True)
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(user_offerer, booking, event_occurrence)
        url = API_URL + '/bookings/token/{}?email={}'.format(booking.token, user.email)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').get(url)
        # Then
        assert response.status_code == 404

    @clean_database
    def test_when_user_not_logged_in_and_doesnt_give_email_returns_400_and_email_in_error(self, app):
        # Given
        user = create_user(email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(admin_user, booking, event_occurrence)

        url = API_URL + '/bookings/token/{}'.format(booking.token)
        # When
        response = req.get(url, headers={'origin': 'http://localhost:3000'})
        # Then
        assert response.status_code == 400
        error_message = response.json()
        assert error_message['email'] == [
            'Vous devez préciser l\'email de l\'utilisateur quand vous n\'êtes pas connecté(e)']

    @pytest.mark.standalone
    def test_when_not_logged_in_give_right_email_and_offer_id_thing_but_already_validated_token_returns_410_and_booking_in_error(
            self, app):
        # Given
        user = create_user(email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_thing_offer(offerer, venue, thing_offer=None, price=0)
        booking = create_booking(user, stock, venue=venue, is_used=True)

        PcObject.check_and_save(admin_user, booking)
        url = API_URL + '/bookings/token/{}?email={}&offer_id={}'.format(booking.token, 'user@email.fr',
                                                                         humanize(stock.offerId))

        # When
        response = req.get(url, headers={'origin': 'http://localhost:3000'})
        # Then
        assert response.status_code == 410
        assert response.json()['booking'] == ['Cette réservation a déjà été validée']

    @clean_database
    def test_when_not_logged_in_and_give_right_email_and_offer_id_thing_but_cancelled_booking_returns_410_and_booking_in_error(
            self, app):
        # Given
        user = create_user(email='user@email.fr')
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_thing_offer(offerer, venue, thing_offer=None, price=0)
        booking = create_booking(user, stock, venue=venue, is_cancelled=True)

        PcObject.check_and_save(admin_user, booking)
        url = API_URL + '/bookings/token/{}?email={}&offer_id={}'.format(booking.token, 'user@email.fr',
                                                                         humanize(stock.offerId))

        # When
        response = req.get(url, headers={'origin': 'http://localhost:3000'})
        # Then
        assert response.status_code == 410
        assert response.json()['booking'] == ['Cette réservation a été annulée']


@pytest.mark.standalone
class PatchBookingAsAnonymousUserTest:
    @clean_database
    def test_patch_booking_with_token_and_valid_email_and_offer_id(self, app):
        # Given
        user = create_user()
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking)
        url = API_URL + '/bookings/token/{}?email={}&offer_id={}'.format(booking.token, user.email,
                                                                         humanize(stock.resolvedOffer.id))

        # When
        response = req.patch(url, headers={'origin': 'http://localhost:3000'})

        # Then
        assert response.status_code == 204
        db.session.refresh(booking)
        assert booking.isUsed is True

    @clean_database
    def test_patch_booking_with_token_and_offer_id_without_email_returns_400(self, app):
        # Given
        user = create_user()
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking)
        url = API_URL + '/bookings/token/{}?&offer_id={}'.format(booking.token, humanize(stock.resolvedOffer.id))

        # When
        response = req.patch(url, headers={'origin': 'http://localhost:3000'})

        # Then
        assert response.status_code == 400
        assert response.json()['email'] == [
            "L'adresse email qui a servie à la réservation est obligatoire dans l'URL [?email=<email>]"]

    @clean_database
    def test_patch_booking_with_token_and_email_without_offer_id_returns_400(self, app):
        # Given
        user = create_user()
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking)
        url = API_URL + '/bookings/token/{}?email={}'.format(booking.token, user.email)

        # When
        response = req.patch(url, headers={'origin': 'http://localhost:3000'})

        # Then
        assert response.status_code == 400
        assert response.json()['offer_id'] == ["L'id de l'offre réservée est obligatoire dans l'URL [?offer_id=<id>]"]

    @clean_database
    def test_patch_booking_with_token_without_offer_id_and_without_email_returns_400_with_both_errors(self, app):
        # Given
        user = create_user()
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking)
        url = API_URL + '/bookings/token/{}'.format(booking.token, user.email)

        # When
        response = req.patch(url, headers={'origin': 'http://localhost:3000'})

        # Then
        assert response.status_code == 400
        assert response.json()['offer_id'] == ["L'id de l'offre réservée est obligatoire dans l'URL [?offer_id=<id>]"]
        assert response.json()['email'] == [
            "L'adresse email qui a servie à la réservation est obligatoire dans l'URL [?email=<email>]"]

    @clean_database
    def test_patch_booking_with_token_returns_404_if_booking_missing(self, app):
        # Given
        user = create_user()
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking)
        url = API_URL + '/bookings/token/{}?email={}&offer_id={}'.format(booking.token, 'wrong.email@test.com',
                                                                         humanize(stock.resolvedOffer.id))

        # When
        response = req.patch(url, headers={'origin': 'http://localhost:3000'})

        # Then
        assert response.status_code == 404
        assert response.json()['global'] == ["Cette contremarque n'a pas été trouvée"]


@pytest.mark.standalone
class PatchBookingByTokenAsLoggedInUserTest:
    @clean_database
    def test_when_has_rights_return_204_and_is_used_is_true(self, app):
        # Given
        user = create_user()
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(admin_user, offerer)
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking, user_offerer)
        url = API_URL + '/bookings/token/{}'.format(booking.token)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').patch(url)

        # Then
        assert response.status_code == 204
        db.session.refresh(booking)
        assert booking.isUsed == True


@pytest.mark.standalone
class PatchBookingByTokenAsLoggedInUserTest:
    @clean_database
    def test_valid_request_with_non_standard_header_returns_204_and_is_used_is_true(self, app):
        # Given
        user = create_user()
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(admin_user, offerer)
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking, user_offerer)
        url = API_URL + '/bookings/token/{}'.format(booking.token)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd', headers={'origin': 'http://random_header.fr'}).patch(url)

        # Then
        assert response.status_code == 204
        db.session.refresh(booking)
        assert booking.isUsed == True

    @clean_database
    def test_valid_request_and_email_with_special_character_url_encoded_returns_204(self, app):
        # Given
        user = create_user(email='user+plus@email.fr')
        user_admin = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(user_admin, offerer, is_admin=True)
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(user_offerer, booking, event_occurrence)
        url_email = urlencode({'email': 'user+plus@email.fr'})
        url = API_URL + '/bookings/token/{}?{}'.format(booking.token, url_email)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').patch(url)
        # Then
        assert response.status_code == 204

    @clean_database
    def test_when_user_not_editor_and_valid_email_returns_403_global_in_error_and_is_used_is_false(self, app):
        # Given
        user = create_user()
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking, admin_user)
        url = API_URL + '/bookings/token/{}?email={}'.format(booking.token, user.email)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').patch(url)

        # Then
        assert response.status_code == 403
        assert response.json()['global'] == ["Cette structure n'est pas enregistr\u00e9e chez cet utilisateur."]
        db.session.refresh(booking)
        assert booking.isUsed == False

    @clean_database
    def test_when_user_not_editor_and_invalid_email_returns_404_and_is_used_is_false(self, app):
        # Given
        user = create_user()
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking, admin_user)
        url = API_URL + '/bookings/token/{}?email={}'.format(booking.token, 'wrong@email.fr')

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').patch(url)

        # Then
        assert response.status_code == 404
        db.session.refresh(booking)
        assert booking.isUsed == False

    @clean_database
    @pytest.mark.standalone
    def test_email_with_special_character_not_url_encoded_returns_404(self, app):
        # Given
        user = create_user(email='user+plus@email.fr')
        user_admin = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(user_admin, offerer, is_admin=True)
        venue = create_venue(offerer)
        offer = create_event_offer(venue, event_name='Event Name')
        event_occurrence = create_event_occurrence(offer)
        stock = create_stock_from_event_occurrence(event_occurrence, price=0)
        booking = create_booking(user, stock, venue=venue)

        PcObject.check_and_save(user_offerer, booking, event_occurrence)
        url = API_URL + '/bookings/token/{}?email={}'.format(booking.token, user.email)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').patch(url)
        # Then
        assert response.status_code == 404

    @clean_database
    def test_when_user_not_editor_and_valid_email_but_invalid_offer_id_returns_404_and_is_used_false(self, app):
        # Given
        user = create_user()
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        PcObject.check_and_save(booking, admin_user)
        url = API_URL + '/bookings/token/{}?email={}&offer_id={}'.format(booking.token, user.email, humanize(123))

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').patch(url)

        # Then
        assert response.status_code == 404
        db.session.refresh(booking)
        assert booking.isUsed == False

    @clean_database
    def test_valid_request_when_booking_is_cancelled_returns_410_and_booking_in_error_and_is_used_is_false(self, app):
        # Given
        user = create_user()
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(admin_user, offerer)
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        booking.isCancelled = True
        PcObject.check_and_save(booking, user_offerer)
        url = API_URL + '/bookings/token/{}'.format(booking.token)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').patch(url)

        # Then
        assert response.status_code == 410
        assert response.json()['booking'] == ['Cette réservation a été annulée']
        db.session.refresh(booking)
        assert booking.isUsed == False

    @clean_database
    def test_valid_request_when_booking_already_validated_returns_410_and_booking_in_error_and_is_used_is_false(self, app):
        # Given
        user = create_user()
        admin_user = create_user(email='admin@email.fr', password='P@55w0rd')
        offerer = create_offerer()
        user_offerer = create_user_offerer(admin_user, offerer)
        venue = create_venue(offerer)
        stock = create_stock_with_event_offer(offerer, venue, price=0)
        booking = create_booking(user, stock, venue=venue)
        booking.isUsed = True
        PcObject.check_and_save(booking, user_offerer)
        url = API_URL + '/bookings/token/{}'.format(booking.token)

        # When
        response = req_with_auth('admin@email.fr', 'P@55w0rd').patch(url)

        # Then
        assert response.status_code == 410
        assert response.json()['booking'] == ['Cette réservation a déjà été validée']
        db.session.refresh(booking)
        assert booking.isUsed == True


@clean_database
@pytest.mark.standalone
def test_cannot_cancel_used_booking(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    deposit_date = datetime.utcnow() - timedelta(minutes=2)
    deposit = create_deposit(user, deposit_date, amount=500)
    booking = create_booking(user, is_used=True)
    PcObject.check_and_save(user, deposit, booking)
    url = API_URL + '/bookings/' + humanize(booking.id)

    # When
    response = req_with_auth(user.email, user.clearTextPassword) \
        .patch(API_URL + '/bookings/' + humanize(booking.id), json={"isCancelled": True})

    # Then
    assert response.status_code == 400
    assert response.json()['booking'] == ["Impossible d\'annuler une réservation consommée"]
    db.session.refresh(booking)
    assert not booking.isCancelled


@clean_database
@pytest.mark.standalone
def test_post_booking_on_stock_with_non_validated_venue_returns_status_code_400_and_stock_id_in_error(app):
    # Given
    user = create_user(email='test@email.com', password='testpsswd')
    deposit = create_deposit(user, datetime.utcnow())
    offerer = create_offerer()
    venue = create_venue(offerer)
    venue.generate_validation_token()
    thing_offer = create_thing_offer(venue)
    stock = create_stock_with_thing_offer(offerer, venue, thing_offer, price=10)
    PcObject.check_and_save(stock, user, deposit)

    booking_json = {
        'stockId': humanize(stock.id),
        'recommendationId': None,
        'quantity': 1
    }

    # When
    r_create = req_with_auth(user.email, user.clearTextPassword).post(API_URL + '/bookings', json=booking_json)

    # Then
    assert r_create.status_code == 400
    assert r_create.json()['stockId'] == [
        'Vous ne pouvez pas encore réserver cette offre, son lieu est en attente de validation']


@clean_database
@pytest.mark.standalone
def test_get_booking_with_url_has_completed_url(app):
    # Given
    user = create_user(email='user+plus@email.fr')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_thing_offer(venue, url='https://host/path/{token}?offerId={offerId}&email={email}')
    stock = create_stock_with_thing_offer(offerer=offerer, venue=venue, thing_offer=offer, price=0)
    booking = create_booking(user, stock, venue=venue, token='ABCDEF')

    PcObject.check_and_save(booking)

    # When
    response = req_with_auth(user.email, 'totallysafepsswd').get(API_URL + '/bookings/' + humanize(booking.id))

    # Then
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['completedUrl'] == 'https://host/path/ABCDEF?offerId=%s&email=user+plus@email.fr' % humanize(
        offer.id)
