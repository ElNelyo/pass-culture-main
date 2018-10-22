""" repository offer queries """
from datetime import datetime, timedelta

import pytest

from models import Thing, PcObject, Event
from models.offer_type import EventType
from repository.offer_queries import departement_or_national_offers, \
    get_offers_for_recommendations_search, get_active_offers_by_type
from tests.conftest import clean_database
from utils.test_utils import create_event, \
    create_event_occurrence, \
    create_event_offer, \
    create_stock_from_event_occurrence, \
    create_thing, \
    create_thing_offer, \
    create_offerer, \
    create_venue, create_user, create_stock_from_offer, create_mediation


@pytest.mark.standalone
@clean_database
def test_departement_or_national_offers_with_national_thing_returns_national_thing(app):
    # Given
    thing = create_thing(thing_name='Lire un livre', is_national=True)
    offerer = create_offerer()
    venue = create_venue(offerer, departement_code='34')
    offer = create_thing_offer(venue, thing)
    PcObject.check_and_save(offer)
    query = Thing.query.filter_by(name='Lire un livre')
    # When
    query = departement_or_national_offers(query, Thing, ['93'])

    assert thing in query.all()


@pytest.mark.standalone
@clean_database
def test_departement_or_national_offers_with_national_event_returns_national_event(app):
    # Given
    event = create_event('Voir une pièce')
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer = create_event_offer(venue, event)
    PcObject.check_and_save(offer)
    query = Event.query.filter_by(name='Voir une pièce')
    # When
    query = departement_or_national_offers(query, Event, ['93'])

    assert event in query.all()


@pytest.mark.standalone
@clean_database
def test_type_search(app):
    # Given
    type_label = str(EventType['CONFERENCE_DEBAT_DEDICACE'])
    other_type_label = str(EventType['MUSIQUE'])

    conference_event = create_event(
        'Rencontre avec Franck Lepage',
        type=type_label
    )
    concert_event = create_event(
        'Concert de Gael Faye',
        type=other_type_label
    )

    offerer = create_offerer(
        siren='507633576',
        address='1 BD POISSONNIERE',
        city='Paris',
        postal_code='75002',
        name='LE GRAND REX PARIS',
        validation_token=None,
        iban=None,
        bic=None
    )
    venue = create_venue(
        offerer,
        name='LE GRAND REX PARIS',
        address="1 BD POISSONNIERE",
        postal_code='75002',
        city="Paris",
        departement_code='75',
        is_virtual=False,
        longitude="2.4002701",
        latitude="48.8363788",
        siret="50763357600016"
    )

    conference_offer = create_event_offer(venue, conference_event)
    concert_offer = create_event_offer(venue, concert_event)

    conference_event_occurrence = create_event_occurrence(
        conference_offer
    )
    concert_event_occurrence = create_event_occurrence(
        concert_offer
    )

    conference_stock = create_stock_from_event_occurrence(conference_event_occurrence)
    concert_stock = create_stock_from_event_occurrence(concert_event_occurrence)

    PcObject.check_and_save(conference_stock, concert_stock)

    offers = get_offers_for_recommendations_search(
        type_values=[
            type_label
        ],
    )

    assert conference_offer in offers


@clean_database
@pytest.mark.standalone
def test_get_active_offers_by_type_when_departement_code_00(app):
    # Given
    offerer = create_offerer()
    venue_34 = create_venue(offerer, postal_code='34000', departement_code='34', siret=offerer.siren + '11111')
    venue_93 = create_venue(offerer, postal_code='93000', departement_code='93', siret=offerer.siren + '22222')
    venue_75 = create_venue(offerer, postal_code='75000', departement_code='75', siret=offerer.siren + '33333')
    offer_34 = create_thing_offer(venue_34)
    offer_93 = create_thing_offer(venue_93)
    offer_75 = create_thing_offer(venue_75)
    stock_34 = create_stock_from_offer(offer_34)
    stock_93 = create_stock_from_offer(offer_93)
    stock_75 = create_stock_from_offer(offer_75)

    PcObject.check_and_save(stock_34, stock_93, stock_75)

    # When
    user = create_user(departement_code='00')
    offers = get_active_offers_by_type(Thing, user=user, departement_codes=['00'], offer_id=None)

    # Then
    assert offer_34 in offers
    assert offer_93 in offers
    assert offer_75 in offers


@clean_database
@pytest.mark.standalone
def test_get_active_event_offers_only_returns_event_offers(app):
    # Given
    user = create_user(departement_code='93')
    offerer = create_offerer()
    venue = create_venue(offerer, departement_code='93')
    offer1 = create_thing_offer(venue, thumb_count=1)
    offer2 = create_event_offer(venue, thumb_count=1)
    now = datetime.utcnow()
    event_occurrence = create_event_occurrence(offer2, beginning_datetime=now + timedelta(hours=72),
                                               end_datetime=now + timedelta(hours=74))
    mediation = create_mediation(offer2)
    stock1 = create_stock_from_offer(offer1, price=0)
    stock2 = create_stock_from_event_occurrence(event_occurrence, price=0, available=10,
                                                booking_limit_date=now + timedelta(days=2))
    PcObject.check_and_save(user, stock1, stock2, mediation, event_occurrence)

    # When
    offers = get_active_offers_by_type(Event, user=user, departement_codes=['93'])
    # Then
    assert len(offers) == 1
    assert offers[0].id == offer2.id
