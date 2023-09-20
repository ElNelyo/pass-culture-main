import React from 'react'

import { useIndividualOfferContext } from 'context/IndividualOfferContext'
import { OFFER_WIZARD_MODE } from 'core/Offers/constants'
import { useOfferWizardMode } from 'hooks'
import {
  StocksEventEdition,
  StocksThing,
  Template,
} from 'screens/IndividualOffer'
import { StocksEventCreation } from 'screens/IndividualOffer/StocksEventCreation/StocksEventCreation'
import Spinner from 'ui-kit/Spinner/Spinner'

const Stocks = (): JSX.Element | null => {
  const { offer } = useIndividualOfferContext()
  const mode = useOfferWizardMode()

  // Here we display a spinner because when the router transitions from
  // Informations form to Stocks form the setOffer after the submit is not
  // propagated yet so there is a quick moment where the offer is null.
  // This is a temporary fix until we use a better pattern than the IndividualOfferWizard
  // to share the offer context
  if (offer === null) {
    return <Spinner />
  }

  return (
    <Template>
      {offer.isEvent ? (
        mode === OFFER_WIZARD_MODE.CREATION ||
        mode === OFFER_WIZARD_MODE.DRAFT ? (
          <StocksEventCreation offer={offer} />
        ) : (
          <StocksEventEdition offer={offer} />
        )
      ) : (
        <StocksThing offer={offer} />
      )}
    </Template>
  )
}

export default Stocks
