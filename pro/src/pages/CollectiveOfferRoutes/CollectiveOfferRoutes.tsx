import React from 'react'
import { useParams, Route, Switch } from 'react-router-dom'

import { extractOfferIdAndOfferTypeFromRouteParams } from 'core/OfferEducational'

import CollectiveOfferCreationRoutes from './CollectiveOfferCreationRoutes'

const CollectiveOfferRoutes = (): JSX.Element => {
  const { offerId: offerIdFromParams } = useParams<{
    offerId: string
  }>()

  const { offerId, isTemplate } =
    extractOfferIdAndOfferTypeFromRouteParams(offerIdFromParams)

  return (
    <Switch>
      <Route path={['/offre/creation/collectif']}>
        <CollectiveOfferCreationRoutes
          offerId={undefined}
          isTemplate={isTemplate}
        />
      </Route>
      <Route
        path={[
          '/offre/collectif/:offerId/creation',
          '/offre/collectif/vitrine/:offerId/creation',
        ]}
      >
        <CollectiveOfferCreationRoutes
          offerId={offerId}
          isTemplate={isTemplate}
        />
      </Route>
    </Switch>
  )
}

export default CollectiveOfferRoutes
