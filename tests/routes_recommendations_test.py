""" routes recommendations tests """
from datetime import datetime, timedelta
from pprint import pprint

import pytest

from models import PcObject
from tests.conftest import clean_database
from utils.human_ids import humanize
from utils.test_utils import API_URL, \
    create_event_occurrence, \
    create_event_offer, \
    create_mediation, \
    create_offerer, \
    create_recommendation, \
    create_stock_from_event_occurrence, \
    create_stock_from_offer, \
    create_thing_offer, \
    create_user, \
    create_venue, \
    req, \
    req_with_auth

RECOMMENDATION_URL = API_URL + '/recommendations'


@pytest.mark.standalone
def test_put_recommendations_works_only_when_logged_in():
    # when
    response = req.put(
        RECOMMENDATION_URL,
        headers={'origin': 'http://localhost:3000'}
    )

    # then
    assert response.status_code == 401


@pytest.mark.standalone
def test_get_recommendations_works_only_when_logged_in():
    # when
    url = RECOMMENDATION_URL + '?keywords=Training'
    response = req.get(url, headers={'origin': 'http://localhost:3000'})

    # then
    assert response.status_code == 401


@clean_database
@pytest.mark.standalone
def test_get_recommendations_returns_one_recommendation_found_from_search_with_matching_case(app):
    # given
    search = "keywords=Training"
    user = create_user(email='test@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_event_offer(venue, event_name='Training in Modern Jazz')
    recommendation = create_recommendation(offer, user, search=search)
    stock = create_stock_from_offer(offer)
    PcObject.check_and_save(stock, recommendation)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.get(RECOMMENDATION_URL + '?%s' % search)

    # then
    recommendations = response.json()
    assert 'Training' in recommendations[0]['offer']['eventOrThing']['name']
    assert recommendations[0]['search'] == 'keywords=Training'


@clean_database
@pytest.mark.standalone
def test_get_recommendations_returns_one_recommendation_found_from_search_ignoring_case(app):
    # given
    search = "keywords=rencontres"
    user = create_user(email='test@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_event_offer(venue, event_name='Rencontres avec des auteurs')
    # NOTE: we need to create event occurrence and stock because
    # GET recommendations filter offer without stock
    event_occurrence = create_event_occurrence(offer)
    stock = create_stock_from_event_occurrence(event_occurrence)
    recommendation = create_recommendation(offer, user, search=search)
    stock = create_stock_from_offer(offer)
    PcObject.check_and_save(stock, recommendation)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.get(RECOMMENDATION_URL + '?%s' % search)

    # then
    recommendations = response.json()
    assert 'Rencontres' in recommendations[0]['offer']['eventOrThing']['name']
    assert recommendations[0]['search'] == 'keywords=rencontres'


@clean_database
@pytest.mark.standalone
def test_get_recommendations_does_not_return_recommendations_of_offers_with_soft_deleted_stocks(app):
    # given
    search = 'keywords=rencontres'
    user = create_user(email='test@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer1 = create_event_offer(venue, event_name='Rencontres avec des peintres')
    offer2 = create_event_offer(venue, event_name='Rencontres avec des auteurs')
    recommendation1 = create_recommendation(offer1, user, search=search)
    recommendation2 = create_recommendation(offer2, user, search=search)

    # NOTE: we need to create event occurrence and stock because
    # GET recommendations filter offer without stock
    event_occurrence1 = create_event_occurrence(offer1)
    event_occurrence2 = create_event_occurrence(offer1)
    event_occurrence3 = create_event_occurrence(offer2)

    stock1 = create_stock_from_event_occurrence(event_occurrence1, price=10, soft_deleted=False)
    stock2 = create_stock_from_event_occurrence(event_occurrence2, price=20, soft_deleted=True)
    stock3 = create_stock_from_event_occurrence(event_occurrence3, price=30, soft_deleted=True)

    PcObject.check_and_save(stock1, stock2, stock3, recommendation1, recommendation2)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.get(RECOMMENDATION_URL + '?%s' % search)

    # then
    assert len(response.json()) == 1


@clean_database
@pytest.mark.standalone
def test_put_recommendations_does_not_return_recommendations_of_offers_with_soft_deleted_stocks(app):
    # Given
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_event_offer(venue)
    user = create_user(email='test@email.com', password='P@55w0rd')
    event_occurrence1 = create_event_occurrence(offer)
    event_occurrence2 = create_event_occurrence(offer)
    stock1 = create_stock_from_event_occurrence(event_occurrence1, soft_deleted=True)
    stock2 = create_stock_from_event_occurrence(event_occurrence2, soft_deleted=False)
    thing_offer1 = create_thing_offer(venue)
    thing_offer2 = create_thing_offer(venue)
    stock3 = create_stock_from_offer(thing_offer1, soft_deleted=True)
    stock4 = create_stock_from_offer(thing_offer2, soft_deleted=False)
    recommendation1 = create_recommendation(offer, user)
    recommendation2 = create_recommendation(thing_offer1, user)
    recommendation3 = create_recommendation(thing_offer2, user)
    PcObject.check_and_save(stock1, stock2, stock3, stock4, recommendation1, recommendation2, recommendation3)

    # When
    response = req_with_auth('test@email.com', 'P@55w0rd').put(RECOMMENDATION_URL, json={})

    # Then
    recommendation_ids = [r['id'] for r in (response.json())]
    assert humanize(recommendation1.id) in recommendation_ids
    assert humanize(recommendation2.id) not in recommendation_ids
    assert humanize(recommendation3.id) in recommendation_ids


@clean_database
@pytest.mark.standalone
def test_put_recommendations_returns_nothing_if_no_stock_on_offer(app):
    # given
    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_event_offer(venue)
    PcObject.check_and_save(user, offer)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.put(RECOMMENDATION_URL, json={'seenRecommendationIds': []})

    # then
    assert response.status_code == 200
    assert len(response.json()) == 0


@clean_database
@pytest.mark.standalone
def test_put_recommendations_returns_one_recommendation_for_offer_on_thing_with_free_stock_with_thumb_count(app):
    # given
    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_thing_offer(venue, thumb_count=1)
    stock = create_stock_from_offer(offer, price=0)
    PcObject.check_and_save(user, stock)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.put(RECOMMENDATION_URL, json={'seenRecommendationIds': []})

    # then
    assert response.status_code == 200
    assert len(response.json()) == 1


@clean_database
@pytest.mark.standalone
def test_put_recommendations_returns_nothing_for_offer_on_thing_with_free_stock_without_thumb_count_and_no_mediation(
        app):
    # given
    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_thing_offer(venue, thumb_count=0)
    stock = create_stock_from_offer(offer, price=0)
    PcObject.check_and_save(user, stock)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.put(RECOMMENDATION_URL, json={'seenRecommendationIds': []})

    # then
    assert response.status_code == 200
    assert len(response.json()) == 0


@clean_database
@pytest.mark.standalone
def test_put_recommendations_returns_one_recommendation_for_offer_on_thing_with_free_stock_with_mediation_but_no_thumb_count(
        app):
    # given
    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_thing_offer(venue, thumb_count=0)
    stock = create_stock_from_offer(offer, price=0)
    mediation = create_mediation(offer)
    PcObject.check_and_save(user, stock, mediation)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.put(RECOMMENDATION_URL, json={'seenRecommendationIds': []})

    # then
    assert response.status_code == 200
    assert len(response.json()) == 1


@clean_database
@pytest.mark.standalone
def test_put_recommendations_returns_nothing_for_offer_on_event_with_free_stock_if_no_mediation_and_no_thumb_count(app):
    # given
    now = datetime.utcnow()
    four_days_from_now = now + timedelta(days=4)
    eight_days_from_now = now + timedelta(days=8)

    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_event_offer(venue)
    event_occurrence = create_event_occurrence(
        offer,
        beginning_datetime=four_days_from_now,
        end_datetime=eight_days_from_now
    )
    stock = create_stock_from_event_occurrence(event_occurrence, price=0, available=20)
    PcObject.check_and_save(user, stock)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.put(RECOMMENDATION_URL, json={'seenRecommendationIds': []})

    # then
    assert response.status_code == 200
    assert len(response.json()) == 0


@clean_database
@pytest.mark.standalone
def test_put_recommendations_returns_one_recommendation_for_offer_on_event_with_free_stock_and_mediation_but_no_thumb_count(
        app):
    # given
    now = datetime.utcnow()
    four_days_from_now = now + timedelta(days=4)
    eight_days_from_now = now + timedelta(days=8)

    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_event_offer(venue)
    event_occurrence = create_event_occurrence(
        offer,
        beginning_datetime=four_days_from_now,
        end_datetime=eight_days_from_now
    )
    mediation = create_mediation(offer)
    stock = create_stock_from_event_occurrence(event_occurrence, price=0, available=20)
    PcObject.check_and_save(user, stock, mediation)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.put(RECOMMENDATION_URL, json={'seenRecommendationIds': []})

    # then
    assert response.status_code == 200
    assert len(response.json()) == 1


@clean_database
@pytest.mark.standalone
def test_put_recommendations_returns_one_recommendation_for_offer_on_event_with_free_stock_and_thumb_count_but_no_mediation(
        app):
    # given
    now = datetime.utcnow()
    four_days_from_now = now + timedelta(days=4)
    eight_days_from_now = now + timedelta(days=8)

    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_event_offer(venue, thumb_count=1, dominant_color=b'123')
    event_occurrence = create_event_occurrence(
        offer,
        beginning_datetime=four_days_from_now,
        end_datetime=eight_days_from_now
    )
    stock = create_stock_from_event_occurrence(event_occurrence, price=0, available=20)
    PcObject.check_and_save(user, stock)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    # when
    response = auth_request.put(RECOMMENDATION_URL, json={'seenRecommendationIds': []})

    # then
    assert response.status_code == 200
    assert len(response.json()) == 1


@clean_database
@pytest.mark.standalone
def test_get_favorite_recommendations_works_only_when_logged_in(app):
    # when
    response = req.get(RECOMMENDATION_URL + '/favorites', headers={'origin': 'http://localhost:3000'})

    # then
    assert response.status_code == 401


@clean_database
@pytest.mark.standalone
def test_get_favorite_recommendations_returns_recommendations_favored_by_current_user(app):
    # given
    user1 = create_user(email='user1@test.com')
    user2 = create_user(email='user2@test.com')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer1 = create_event_offer(venue)
    offer2 = create_event_offer(venue)
    recommendation1 = create_recommendation(offer1, user1, is_favorite=False)
    recommendation2 = create_recommendation(offer2, user1, is_favorite=True)
    recommendation3 = create_recommendation(offer2, user1, is_favorite=True)
    recommendation4 = create_recommendation(offer2, user2, is_favorite=True)
    PcObject.check_and_save(user1, user2, recommendation1, recommendation2, recommendation3, recommendation4)
    auth_request = req_with_auth(user1.email, user1.clearTextPassword)

    # when
    response = auth_request.get(RECOMMENDATION_URL + '/favorites')

    # then
    assert response.status_code == 200
    assert len(response.json()) == 2


@clean_database
@pytest.mark.standalone
def test_put_recommendations_returns_requested_recommendation_first(app):
    # given
    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer1 = create_thing_offer(venue, thumb_count=1)
    offer2 = create_event_offer(venue, thumb_count=1)
    offer3 = create_thing_offer(venue, thumb_count=1)
    offer4 = create_thing_offer(venue, thumb_count=1)
    now = datetime.utcnow()
    fifteen_min_ago = now - timedelta(minutes=15)
    event_occurrence = create_event_occurrence(offer2, beginning_datetime=now + timedelta(hours=72),
                                               end_datetime=now + timedelta(hours=74))
    mediation = create_mediation(offer2)
    stock1 = create_stock_from_offer(offer1, price=0)
    stock2 = create_stock_from_event_occurrence(event_occurrence, price=0, available=10, soft_deleted=False,
                                                booking_limit_date=now + timedelta(days=3))
    stock3 = create_stock_from_offer(offer3, price=0)
    stock4 = create_stock_from_offer(offer4, price=0)
    recommendation_offer3 = create_recommendation(offer3, user)
    recommendation_offer4 = create_recommendation(offer4, user, date_read=now - timedelta(days=1))
    PcObject.check_and_save(user, stock1, stock2, stock3, stock4, mediation, event_occurrence, recommendation_offer3,
                            recommendation_offer4)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    data = {'seenRecommendationIds': []}
    # when
    response = auth_request.put(RECOMMENDATION_URL + '?offerId=%s' % humanize(offer1.id), json=data)

    # then
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 4
    offer_ids = set(map(lambda x: x['offer']['id'], response_json))
    recommendation_ids = set(map(lambda x: x['id'], response_json))
    assert response_json[0]['offer']['id'] == humanize(offer1.id)
    assert humanize(offer1.id) in offer_ids
    assert humanize(offer2.id) in offer_ids
    assert humanize(offer3.id) in offer_ids
    assert humanize(recommendation_offer4.id) in recommendation_ids
    assert humanize(recommendation_offer3.id) in recommendation_ids


@clean_database
@pytest.mark.standalone
def test_put_recommendations_when_expired_in_seen(app):
    # given
    now = datetime.utcnow()
    fifteen_min_ago = now - timedelta(minutes=15)
    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer1 = create_thing_offer(venue, thumb_count=1)
    offer2 = create_event_offer(venue, thumb_count=1)
    offer3 = create_thing_offer(venue, thumb_count=1)
    offer4 = create_thing_offer(venue, thumb_count=1)
    event_occurrence = create_event_occurrence(offer2, beginning_datetime=now + timedelta(hours=72),
                                               end_datetime=now + timedelta(hours=74))
    mediation = create_mediation(offer2)
    stock1 = create_stock_from_offer(offer1, price=0)
    stock2 = create_stock_from_event_occurrence(event_occurrence, price=0, available=10, soft_deleted=False,
                                                booking_limit_date=now + timedelta(days=3))
    stock3 = create_stock_from_offer(offer3, price=0)
    stock4 = create_stock_from_offer(offer4, price=0)
    recommendation_offer1 = create_recommendation(offer1, user, valid_until_date=fifteen_min_ago)
    recommendation_offer2 = create_recommendation(offer2, user, valid_until_date=fifteen_min_ago)
    recommendation_offer3 = create_recommendation(offer3, user, valid_until_date=fifteen_min_ago)
    recommendation_offer4 = create_recommendation(offer4, user, date_read=now - timedelta(days=1),
                                                  valid_until_date=fifteen_min_ago)
    PcObject.check_and_save(stock1, stock2, stock3, stock4, mediation, event_occurrence, recommendation_offer3,
                            recommendation_offer4, recommendation_offer1, recommendation_offer2)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    data = {'seenRecommendationIds': []}
    # when
    response = auth_request.put(RECOMMENDATION_URL + '?offerId=%s' % humanize(offer1.id), json=data)

    # then
    assert response.status_code == 200
    response_json = response.json()
    pprint(response_json)
    assert len(response_json) == 4
    recommendation_ids = set(map(lambda x: x['id'], response_json))
    assert humanize(recommendation_offer1.id) not in recommendation_ids
    assert humanize(recommendation_offer2.id) not in recommendation_ids
    assert humanize(recommendation_offer3.id) not in recommendation_ids
    assert humanize(recommendation_offer4.id) not in recommendation_ids


@clean_database
@pytest.mark.standalone
def test_put_recommendations_when_expired_in_seen(app):
    # given
    now = datetime.utcnow()
    fifteen_min_ago = now - timedelta(minutes=15)
    user = create_user(email='weird.bug@email.com', password='P@55w0rd')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer1 = create_thing_offer(venue, thumb_count=1)
    stock1 = create_stock_from_offer(offer1, price=0)
    recommendation_offer1 = create_recommendation(offer1, user, valid_until_date=fifteen_min_ago)
    PcObject.check_and_save(stock1, recommendation_offer1)
    auth_request = req_with_auth(user.email, user.clearTextPassword)

    data = {'seenRecommendationIds': []}
    # when
    response = auth_request.put(RECOMMENDATION_URL + '?offerId=%s' % humanize(offer1.id), json=data)

    # then
    assert response.status_code == 200
    response_json = response.json()
    pprint(response_json)
    assert len(response_json) == 1
    recommendation_ids = set(map(lambda x: x['id'], response_json))
    assert humanize(recommendation_offer1.id) not in recommendation_ids
