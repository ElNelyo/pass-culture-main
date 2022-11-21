import React, { useEffect, useState } from 'react'
import { useHistory, useLocation } from 'react-router-dom'

import RouteLeavingGuardCollectiveOfferCreation from 'components/RouteLeavingGuardCollectiveOfferCreation'
import {
  CollectiveOffer,
  DEFAULT_EAC_FORM_VALUES,
  IOfferEducationalFormValues,
  isCollectiveOffer,
  Mode,
  setInitialFormValues,
} from 'core/OfferEducational'
import canOffererCreateCollectiveOfferAdapter from 'core/OfferEducational/adapters/canOffererCreateCollectiveOfferAdapter'
import getCollectiveOfferFormDataApdater from 'core/OfferEducational/adapters/getCollectiveOfferFormDataAdapter'
import patchCollectiveOfferAdapter from 'core/OfferEducational/adapters/patchCollectiveOfferAdapter'
import postCollectiveOfferAdapter from 'core/OfferEducational/adapters/postCollectiveOfferAdapter'
import useNotification from 'hooks/useNotification'
import { queryParamsFromOfferer } from 'pages/Offers/utils/queryParamsFromOfferer'
import OfferEducationalScreen from 'screens/OfferEducational'
import { IOfferEducationalProps } from 'screens/OfferEducational/OfferEducational'
import Spinner from 'ui-kit/Spinner/Spinner'

import { useCollectiveOfferImageUpload } from './useCollectiveOfferImageUpload'

type AsyncScreenProps = Pick<
  IOfferEducationalProps,
  'categories' | 'userOfferers' | 'domainsOptions'
>

interface CollectiveOfferCreationProps {
  offer?: CollectiveOffer
  setOffer: (offer: CollectiveOffer) => void
}

const CollectiveOfferCreation = ({
  offer,
  setOffer,
}: CollectiveOfferCreationProps): JSX.Element => {
  const history = useHistory()
  const location = useLocation()

  const [isReady, setIsReady] = useState<boolean>(false)
  const [screenProps, setScreenProps] = useState<AsyncScreenProps | null>(null)
  const [initialValues, setInitialValues] =
    useState<IOfferEducationalFormValues>(DEFAULT_EAC_FORM_VALUES)

  const { structure: offererId, lieu: venueId } =
    queryParamsFromOfferer(location)

  const notify = useNotification()
  const { imageOffer, onImageDelete, onImageUpload, handleImageOnSubmit } =
    useCollectiveOfferImageUpload(offer, false)

  const createOrPatchDraftOffer = async (
    offerValues: IOfferEducationalFormValues
  ) => {
    const isCreatingOffer = offer === undefined
    const adapter = isCreatingOffer
      ? () => postCollectiveOfferAdapter({ offer: offerValues })
      : () =>
          patchCollectiveOfferAdapter({
            offer: offerValues,
            initialValues,
            offerId: offer.id,
          })

    const { payload, isOk, message } = await adapter()

    if (!isOk) {
      return notify.error(message)
    }

    const offerId = offer?.id ?? payload.id
    await handleImageOnSubmit(offerId, isCreatingOffer)
    if (offer && isCollectiveOffer(payload)) {
      setOffer({
        ...payload,
        imageUrl: imageOffer?.url,
        imageCredit: imageOffer?.credit,
      })
    }

    history.push(`/offre/${payload.id}/collectif/stocks`)
  }

  useEffect(() => {
    if (!isReady) {
      const loadData = async () => {
        const result = await getCollectiveOfferFormDataApdater({
          offererId,
          offer,
        })

        if (!result.isOk) {
          notify.error(result.message)
        }

        const { categories, offerers, domains, initialValues } = result.payload

        setScreenProps({
          categories: categories,
          userOfferers: offerers,
          domainsOptions: domains,
        })

        setInitialValues(values =>
          setInitialFormValues(
            { ...values, ...initialValues },
            offerers,
            initialValues.offererId ?? offererId,
            initialValues.venueId ?? venueId
          )
        )

        setIsReady(true)
      }

      loadData()
    }
  }, [isReady, venueId, offererId])

  return isReady && screenProps ? (
    <>
      <OfferEducationalScreen
        {...screenProps}
        getIsOffererEligible={canOffererCreateCollectiveOfferAdapter}
        initialValues={initialValues}
        mode={Mode.CREATION}
        onSubmit={createOrPatchDraftOffer}
        isTemplate={false}
        imageOffer={imageOffer}
        onImageDelete={onImageDelete}
        onImageUpload={onImageUpload}
      />
      <RouteLeavingGuardCollectiveOfferCreation />
    </>
  ) : (
    <Spinner />
  )
}

export default CollectiveOfferCreation
