import { EditVenueBodyModel, VenueTypeCode } from 'apiClient/v1'
import { unhumanizeSiret } from 'core/Venue/utils'

import { VenueSettingsFormValues } from './types'

export const serializeEditVenueBodyModel = (
  formValues: VenueSettingsFormValues,
  hideSiret: boolean,
  isVenueVirtual: boolean,
  shouldSendMail?: boolean
): EditVenueBodyModel => {
  const payload: EditVenueBodyModel = {
    banId: formValues.banId,
    bookingEmail: formValues.bookingEmail,
    city: formValues.city,
    comment: formValues.comment,
    latitude: formValues.latitude,
    longitude: formValues.longitude,
    name: formValues.name,
    postalCode: formValues.postalCode,
    publicName: formValues.publicName,
    street: formValues.street,
    siret: unhumanizeSiret(formValues.siret),
    withdrawalDetails: formValues.withdrawalDetails,
    isEmailAppliedOnAllOffers: true,
    isWithdrawalAppliedOnAllOffers: formValues.isWithdrawalAppliedOnAllOffers,
    shouldSendMail: shouldSendMail,
    venueLabelId: !formValues.venueLabel ? null : Number(formValues.venueLabel),
    venueTypeCode: formValues.venueType as VenueTypeCode,
  }

  if (hideSiret) {
    delete payload.siret
  } else {
    payload.comment = ''
  }

  return payload
}
