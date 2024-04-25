import { api } from 'apiClient/api'
import { OfferType } from 'apiClient/v1'
import { DEFAULT_PRE_FILTERS } from 'core/Bookings/constants'
import { PreFiltersParams } from 'core/Bookings/types'
import { downloadFile } from 'utils/downloadFile'

export const downloadBookingsCSVFile = async (
  filters: PreFiltersParams & { page?: number }
) => {
  const bookingsCsvText = await api.getBookingsCsv(
    filters.page,
    filters.offerVenueId !== DEFAULT_PRE_FILTERS.offerVenueId
      ? Number(filters.offerVenueId)
      : null,
    null,
    filters.offerEventDate !== DEFAULT_PRE_FILTERS.offerEventDate
      ? filters.offerEventDate
      : null,
    filters.bookingStatusFilter,
    filters.bookingBeginningDate,
    filters.bookingEndingDate,
    // TODO fix PreFiltersParams type to use OfferType instead of string
    filters.offerType !== DEFAULT_PRE_FILTERS.offerType
      ? (filters.offerType as OfferType)
      : null
  )

  const date = new Date().toISOString()
  downloadFile(
    bookingsCsvText,
    `reservations_pass_culture-${date}.csv`,
    'text/csv'
  )
}
