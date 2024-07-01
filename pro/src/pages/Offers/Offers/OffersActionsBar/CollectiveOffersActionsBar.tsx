import { useState } from 'react'
import { mutate } from 'swr'

import { api } from 'apiClient/api'
import {
  CollectiveBookingStatus,
  CollectiveOfferResponseModel,
  CollectiveOfferStatus,
} from 'apiClient/v1'
import { ActionsBarSticky } from 'components/ActionsBarSticky/ActionsBarSticky'
import { GET_COLLECTIVE_OFFERS_QUERY_KEY } from 'config/swrQueryKeys'
import { DEFAULT_SEARCH_FILTERS } from 'core/Offers/constants'
import { useQuerySearchFilters } from 'core/Offers/hooks/useQuerySearchFilters'
import { SearchFiltersParams } from 'core/Offers/types'
import { serializeApiFilters } from 'core/Offers/utils/serializer'
import { useNotification } from 'hooks/useNotification'
import fullHideIcon from 'icons/full-hide.svg'
import fullValidateIcon from 'icons/full-validate.svg'
import { Button } from 'ui-kit/Button/Button'
import { ButtonVariant } from 'ui-kit/Button/types'

import { CollectiveDeactivationConfirmDialog } from './DeactivationConfirmDialog/CollectiveDeactivationConfirmDialog'
import {
  computeActivationSuccessMessage,
  computeAllActivationSuccessMessage,
  computeAllDeactivationSuccessMessage,
  computeDeactivationSuccessMessage,
} from './utils'
import { computeSelectedOffersLabel } from './utils/computeSelectedOffersLabel'

export type CollectiveOffersActionsBarProps = {
  areAllOffersSelected: boolean
  clearSelectedOfferIds: () => void
  selectedOffers: CollectiveOfferResponseModel[]
  toggleSelectAllCheckboxes: () => void
  getUpdateOffersStatusMessage: (selectedOfferIds: number[]) => string
}

const updateCollectiveOffersStatus = async (
  isActive: boolean,
  areAllOffersSelected: boolean,
  selectedOffers: CollectiveOfferResponseModel[],
  notify: ReturnType<typeof useNotification>,
  apiFilters: SearchFiltersParams
) => {
  const payload = serializeApiFilters(apiFilters)
  if (areAllOffersSelected) {
    //  Bulk edit if all editable offers are selected
    try {
      await api.patchAllCollectiveOffersActiveStatus({
        ...payload,
        isActive,
      })

      notify.pending(
        isActive
          ? computeAllActivationSuccessMessage(selectedOffers.length)
          : computeAllDeactivationSuccessMessage(selectedOffers.length)
      )
    } catch {
      notify.error(
        `Une erreur est survenue lors de ${
          isActive ? 'la publication' : 'la désactivation'
        } des offres`
      )
    }
  } else {
    try {
      //  Differenciate template and bookable selected offers so that there can be two separarate api status update calls
      const collectiveOfferIds = []
      const collectiveOfferTemplateIds = []

      for (const offer of selectedOffers) {
        if (offer.isShowcase) {
          collectiveOfferTemplateIds.push(offer.id)
        } else {
          collectiveOfferIds.push(offer.id)
        }
      }

      if (collectiveOfferIds.length > 0) {
        await api.patchCollectiveOffersActiveStatus({
          ids: collectiveOfferIds.map((id) => Number(id)),
          isActive,
        })
      }

      if (collectiveOfferTemplateIds.length > 0) {
        await api.patchCollectiveOffersTemplateActiveStatus({
          ids: collectiveOfferTemplateIds.map((ids) => Number(ids)),
          isActive,
        })
      }

      notify.information(
        isActive
          ? computeActivationSuccessMessage(selectedOffers.length)
          : computeDeactivationSuccessMessage(selectedOffers.length)
      )
    } catch {
      notify.error(
        `Une erreur est survenue lors de ${
          isActive ? 'la publication' : 'la désactivation'
        } des offres sélectionnées`
      )
    }
  }

  await mutate([GET_COLLECTIVE_OFFERS_QUERY_KEY, apiFilters])
}

function canDeactivateCollectiveOffers(offers: CollectiveOfferResponseModel[]) {
  return offers.every((offer) => {
    //  Check that all the offers are published or expired
    return (
      offer.status === CollectiveOfferStatus.ACTIVE ||
      (offer.status === CollectiveOfferStatus.EXPIRED &&
        (!offer.booking?.booking_status ||
          offer.booking.booking_status === CollectiveBookingStatus.CANCELLED))
    )
  })
}

export function CollectiveOffersActionsBar({
  selectedOffers,
  clearSelectedOfferIds,
  toggleSelectAllCheckboxes,
  areAllOffersSelected,
  getUpdateOffersStatusMessage,
}: CollectiveOffersActionsBarProps) {
  const urlSearchFilters = useQuerySearchFilters()

  const notify = useNotification()
  const [isDeactivationDialogOpen, setIsDeactivationDialogOpen] =
    useState(false)

  const apiFilters = {
    ...DEFAULT_SEARCH_FILTERS,
    ...urlSearchFilters,
  }
  delete apiFilters.page

  const handleClose = () => {
    clearSelectedOfferIds()
    areAllOffersSelected && toggleSelectAllCheckboxes()
  }

  function onDeactivateOffersClicked() {
    if (!canDeactivateCollectiveOffers(selectedOffers)) {
      notify.error(
        'Seules les offres au statut publié ou expiré peuvent être masquées.'
      )
      return
    }
    setIsDeactivationDialogOpen(true)
  }

  const handleUpdateOffersStatus = async (isActivating: boolean) => {
    await updateCollectiveOffersStatus(
      isActivating,
      areAllOffersSelected,
      selectedOffers,
      notify,
      apiFilters
    )

    handleClose()
  }

  const handleActivate = async () => {
    const updateOfferStatusMessage = getUpdateOffersStatusMessage(
      selectedOffers.map((offer) => offer.id)
    )
    if (!updateOfferStatusMessage) {
      await handleUpdateOffersStatus(true)
    } else {
      notify.error(updateOfferStatusMessage)
    }
  }

  const handleDeactivateOffers = async () => {
    await handleUpdateOffersStatus(false)
    setIsDeactivationDialogOpen(false)
  }

  return (
    <>
      {isDeactivationDialogOpen && (
        <CollectiveDeactivationConfirmDialog
          areAllOffersSelected={areAllOffersSelected}
          nbSelectedOffers={selectedOffers.length}
          onConfirm={handleDeactivateOffers}
          onCancel={() => setIsDeactivationDialogOpen(false)}
        />
      )}

      <ActionsBarSticky>
        <ActionsBarSticky.Left>
          <span role="status">
            {computeSelectedOffersLabel(selectedOffers.length)}
          </span>
        </ActionsBarSticky.Left>
        <ActionsBarSticky.Right>
          <Button onClick={handleClose} variant={ButtonVariant.SECONDARY}>
            Annuler
          </Button>
          <Button
            onClick={onDeactivateOffersClicked}
            icon={fullHideIcon}
            variant={ButtonVariant.SECONDARY}
          >
            Masquer
          </Button>
          <Button
            onClick={handleActivate}
            icon={fullValidateIcon}
            variant={ButtonVariant.SECONDARY}
          >
            Publier
          </Button>
        </ActionsBarSticky.Right>
      </ActionsBarSticky>
    </>
  )
}
