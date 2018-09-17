"""events"""
import binascii
from flask import current_app as app, jsonify, request

from models import ApiErrors, Event, Offer, Offerer, PcObject, Venue
from utils.human_ids import dehumanize
from utils.includes import EVENT_INCLUDES
from utils.logger import logger
from utils.rest import expect_json_data, \
    load_or_404, \
    login_or_api_key_required
from validation.events import check_has_venue_id


@app.route('/events/<id>', methods=['GET'])
@login_or_api_key_required
def get_event(id):
    event = load_or_404(Event, id)
    return jsonify(
        event._asdict(include=EVENT_INCLUDES)
    ), 200


@app.route('/events', methods=['POST'])
@login_or_api_key_required
@expect_json_data
def post_event():
    venue_id = request.json.get('venueId')
    event = Event()
    event.populateFromDict(request.json)
    offer = Offer()
    check_has_venue_id(venue_id)
    api_errors = ApiErrors()
    try:
        offer.venueId = dehumanize(venue_id)
    except binascii.Error:
        api_errors.addError('venueId', 'le lieu est invalide')
        raise api_errors
    offer.event = event
    PcObject.check_and_save(event, offer)
    return jsonify(
        event._asdict(include=EVENT_INCLUDES)
    ), 201


@app.route('/events/<id>', methods=['PATCH'])
@login_or_api_key_required
@expect_json_data
def patch_event(id):
    event = load_or_404(Event, id)
    event.populateFromDict(request.json)
    PcObject.check_and_save(event)
    return jsonify(
        event._asdict(include=EVENT_INCLUDES)
    ), 200
