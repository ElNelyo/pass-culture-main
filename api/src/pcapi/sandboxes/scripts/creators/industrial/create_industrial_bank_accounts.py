import logging

from pcapi.core.finance import factories as finance_factories
from pcapi.core.finance import models as finance_models
from pcapi.core.offerers import factories as offerers_factories
from pcapi.core.offers import factories as offers_factories


logger = logging.getLogger(__name__)


def create_industrial_bank_accounts() -> None:
    logger.info("create_industrial_bank_accounts")
    create_offerer_without_bank_accounts()
    create_offerer_with_various_bank_accounts_state()
    create_offerer_with_all_his_venue_linked()
    create_offerer_at_least_one_venue_linked()
    create_offerer_with_none_venue_linked()
    create_offerer_with_all_his_venue_linked_to_one_bank_account()
    create_offerer_with_only_one_venue_linked()


def create_offerer_without_bank_accounts() -> None:
    logger.info("create_offerer_without_bank_accounts")
    offerer_without_bank_accounts = offerers_factories.OffererFactory(name="without_bank_accounts")
    offerers_factories.UserOffererFactory(
        offerer=offerer_without_bank_accounts, user__email="offerer_with_bank_accounts@mail.com"
    )
    venue = offerers_factories.VenueFactory(managingOfferer=offerer_without_bank_accounts)
    offer = offers_factories.OfferFactory(venue=venue)
    offers_factories.StockFactory(offer=offer)


def create_offerer_with_various_bank_accounts_state() -> None:
    logger.info("create_offerer_with_various_bank_accounts_state")
    offerer_with_various_bank_accounts_status = offerers_factories.OffererFactory(name="various_bank_account_status")
    offerers_factories.UserOffererFactory(
        offerer=offerer_with_various_bank_accounts_status, user__email="various_bank_accounts_status@mail.com"
    )
    finance_factories.BankAccountFactory(
        status=finance_models.BankAccountApplicationStatus.ACCEPTED, offerer=offerer_with_various_bank_accounts_status
    )
    finance_factories.BankAccountFactory(
        status=finance_models.BankAccountApplicationStatus.DRAFT, offerer=offerer_with_various_bank_accounts_status
    )
    finance_factories.BankAccountFactory(
        status=finance_models.BankAccountApplicationStatus.ON_GOING, offerer=offerer_with_various_bank_accounts_status
    )
    finance_factories.BankAccountFactory(
        status=finance_models.BankAccountApplicationStatus.REFUSED, offerer=offerer_with_various_bank_accounts_status
    )
    finance_factories.BankAccountFactory(
        status=finance_models.BankAccountApplicationStatus.WITHOUT_CONTINUATION,
        offerer=offerer_with_various_bank_accounts_status,
    )
    venue = offerers_factories.VenueFactory(managingOfferer=offerer_with_various_bank_accounts_status)
    offer = offers_factories.OfferFactory(venue=venue)
    offers_factories.StockFactory(offer=offer)


def create_offerer_with_all_his_venue_linked() -> None:
    logger.info("create_offerer_with_all_his_venue_linked")

    offerer_with_all_venues_linked = offerers_factories.OffererFactory(name="all_venues_linked")
    offerers_factories.UserOffererFactory(offerer=offerer_with_all_venues_linked, user__email="all_venues_linked")
    first_venue_with_non_free_offer = offerers_factories.VenueFactory(managingOfferer=offerer_with_all_venues_linked)
    offers_factories.StockFactory(offer__venue=first_venue_with_non_free_offer)
    second_venue_with_non_free_offer = offerers_factories.VenueFactory(managingOfferer=offerer_with_all_venues_linked)
    offers_factories.StockFactory(offer__venue=second_venue_with_non_free_offer)

    bank_account = finance_factories.BankAccountFactory(offerer=offerer_with_all_venues_linked)
    offerers_factories.VenueBankAccountLinkFactory(venue=first_venue_with_non_free_offer, bankAccount=bank_account)
    offerers_factories.VenueBankAccountLinkFactory(venue=second_venue_with_non_free_offer, bankAccount=bank_account)


def create_offerer_at_least_one_venue_linked() -> None:
    logger.info("create_offerer_at_least_one_venue_linked")
    offerer_with_one_venue_linked = offerers_factories.OffererFactory(name="at_least_one_venue_linked")
    offerers_factories.UserOffererFactory(
        offerer=offerer_with_one_venue_linked, user__email="at_least_one_venue_linked"
    )
    first_venue_with_non_free_offer = offerers_factories.VenueFactory(managingOfferer=offerer_with_one_venue_linked)
    offers_factories.StockFactory(offer__venue=first_venue_with_non_free_offer)
    second_venue_with_non_free_offer = offerers_factories.VenueFactory(managingOfferer=offerer_with_one_venue_linked)
    offers_factories.StockFactory(offer__venue=second_venue_with_non_free_offer)

    bank_account = finance_factories.BankAccountFactory(offerer=offerer_with_one_venue_linked)
    offerers_factories.VenueBankAccountLinkFactory(venue=first_venue_with_non_free_offer, bankAccount=bank_account)


def create_offerer_with_none_venue_linked() -> None:
    logger.info("create_offerer_with_none_venue_linked")
    offerer_with_none_venue_linked = offerers_factories.OffererFactory(name="none_venue_linked")
    offerers_factories.UserOffererFactory(offerer=offerer_with_none_venue_linked, user__email="none_venue_linked")
    first_venue_with_non_free_offer = offerers_factories.VenueFactory(managingOfferer=offerer_with_none_venue_linked)
    offers_factories.StockFactory(offer__venue=first_venue_with_non_free_offer)
    second_venue_with_non_free_offer = offerers_factories.VenueFactory(managingOfferer=offerer_with_none_venue_linked)
    offers_factories.StockFactory(offer__venue=second_venue_with_non_free_offer)

    finance_factories.BankAccountFactory(offerer=offerer_with_none_venue_linked)


def create_offerer_with_all_his_venue_linked_to_one_bank_account() -> None:
    logger.info("create_offerer_with_all_his_venue_linked_to_one_bank_account")

    offerer_with_all_venues_linked = offerers_factories.OffererFactory(
        name="all_venues_linked_to_only_one_bank_account"
    )
    offerers_factories.UserOffererFactory(
        offerer=offerer_with_all_venues_linked, user__email="all_venues_linked_to_only_one_bank_account"
    )
    first_venue_with_non_free_offer = offerers_factories.VenueFactory(managingOfferer=offerer_with_all_venues_linked)
    offers_factories.StockFactory(offer__venue=first_venue_with_non_free_offer)
    second_venue_with_non_free_offer = offerers_factories.VenueFactory(managingOfferer=offerer_with_all_venues_linked)
    offers_factories.StockFactory(offer__venue=second_venue_with_non_free_offer)

    bank_account = finance_factories.BankAccountFactory(offerer=offerer_with_all_venues_linked)
    finance_factories.BankAccountFactory(offerer=offerer_with_all_venues_linked)
    offerers_factories.VenueBankAccountLinkFactory(venue=first_venue_with_non_free_offer, bankAccount=bank_account)
    offerers_factories.VenueBankAccountLinkFactory(venue=second_venue_with_non_free_offer, bankAccount=bank_account)


def create_offerer_with_only_one_venue_linked() -> None:
    logger.info("create_offerer_with_only_one_venue_linked")
    offerer_with_only_one_venue_linked = offerers_factories.OffererFactory(name="offerer_with_only_one_venue_linked")
    offerers_factories.UserOffererFactory(
        offerer=offerer_with_only_one_venue_linked, user__email="offerer_with_only_one_venue_linked"
    )
    first_venue_with_non_free_offer = offerers_factories.VenueFactory(
        managingOfferer=offerer_with_only_one_venue_linked
    )
    offers_factories.StockFactory(offer__venue=first_venue_with_non_free_offer)
    second_venue_with_non_free_offer = offerers_factories.VenueFactory(
        managingOfferer=offerer_with_only_one_venue_linked
    )
    offers_factories.StockFactory(offer__venue=second_venue_with_non_free_offer)
    third_venue_with_non_free_offer = offerers_factories.VenueFactory(
        managingOfferer=offerer_with_only_one_venue_linked
    )

    bank_account = finance_factories.BankAccountFactory(offerer=offerer_with_only_one_venue_linked)

    offerers_factories.VenueBankAccountLinkFactory(venue=third_venue_with_non_free_offer, bankAccount=bank_account)
