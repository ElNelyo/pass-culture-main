import format from 'date-fns/format'
import React, { useEffect, useState } from 'react'

import {
  BookingRecapResponseModel,
  GetIndividualOfferResponseModel,
} from 'apiClient/v1'
import {
  DEFAULT_PRE_FILTERS,
  EMPTY_FILTER_VALUE,
} from 'core/Bookings/constants'
import useActiveFeature from 'hooks/useActiveFeature'
import strokeBookingHold from 'icons/stroke-booking-hold.svg'
import { getFilteredBookingsRecapAdapter } from 'pages/Bookings/adapters'
import { IndividualBookingsTable } from 'screens/Bookings/BookingsRecapTable/BookingsTable/IndividualBookingsTable'
import { DEFAULT_OMNISEARCH_CRITERIA } from 'screens/Bookings/BookingsRecapTable/Filters'
import Header from 'screens/Bookings/BookingsRecapTable/Header'
import filterBookingsRecap from 'screens/Bookings/BookingsRecapTable/utils/filterBookingsRecap'
import { Button } from 'ui-kit/Button'
import { ButtonVariant } from 'ui-kit/Button/types'
import Spinner from 'ui-kit/Spinner/Spinner'
import { SvgIcon } from 'ui-kit/SvgIcon/SvgIcon'
import { FORMAT_ISO_DATE_ONLY } from 'utils/date'

import styles from './BookingsSummary.module.scss'
import { DownloadBookingsModal } from './DownloadBookingsModal/DownloadBookingsModal'

interface BookingsSummaryScreenProps {
  offer: GetIndividualOfferResponseModel
}

export const BookingsSummaryScreen = ({
  offer,
}: BookingsSummaryScreenProps) => {
  const [bookings, setBookings] = useState<BookingRecapResponseModel[] | null>(
    null
  )
  const [totalBookings, setTotalBookings] = useState<number>(0)
  const [bookingsStatusFilters, setBookingsStatusFilter] = useState<string[]>(
    []
  )

  const [isModalOpen, setIsModalOpen] = useState(false)

  const isDownloadBookingsFeatureEnabled = useActiveFeature(
    'WIP_ENABLE_DOWNLOAD_BOOKINGS'
  )

  useEffect(() => {
    const loadBookings = async () => {
      const response = await getFilteredBookingsRecapAdapter({
        ...DEFAULT_PRE_FILTERS,
        offerId: String(offer.id),
        bookingBeginningDate: '2015-01-01',
        bookingEndingDate: format(new Date(), FORMAT_ISO_DATE_ONLY),
      })

      if (response.isOk) {
        setBookings(response.payload.bookings)
        setTotalBookings(response.payload.total)
      }
    }
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    loadBookings()
  }, [setBookings, offer.id])

  if (bookings?.length === 0) {
    return (
      <div className={styles['no-data']}>
        <SvgIcon
          className={styles['no-data-icon']}
          src={strokeBookingHold}
          alt=""
          width="128"
          viewBox="0 0 200 156"
        />

        <div>Vous n’avez pas encore de réservations</div>
      </div>
    )
  }

  const filteredBookings = filterBookingsRecap(bookings ?? [], {
    bookingStatus: bookingsStatusFilters,
    // Improve the filtering of the base bookings page, it is a mess
    // because it mixes backend and frontend filtering in weird ways.
    // Thus I must reuse this function with lots of empty values
    // to filter by booking status
    bookingBeneficiary: EMPTY_FILTER_VALUE,
    bookingToken: EMPTY_FILTER_VALUE,
    offerISBN: EMPTY_FILTER_VALUE,
    offerName: EMPTY_FILTER_VALUE,
    selectedOmniSearchCriteria: DEFAULT_OMNISEARCH_CRITERIA,
    keywords: EMPTY_FILTER_VALUE,
    bookingInstitution: EMPTY_FILTER_VALUE,
    bookingId: EMPTY_FILTER_VALUE,
  })

  return (
    <>
      {isModalOpen && (
        <DownloadBookingsModal
          offerId={offer.id}
          onDimiss={() => setIsModalOpen(false)}
        />
      )}

      <div className={styles['header']}>
        <h2 className={styles['header-title']}>Réservations</h2>
        {isDownloadBookingsFeatureEnabled &&
          bookings !== null &&
          bookings.length && (
            <Button
              variant={ButtonVariant.PRIMARY}
              onClick={() => setIsModalOpen(true)}
            >
              Télécharger les réservations
            </Button>
          )}
      </div>
      {bookings !== null ? (
        <>
          <Header
            bookingsRecapFilteredLength={totalBookings}
            isLoading={false}
            resetBookings={() => setBookingsStatusFilter([])}
          />
          <IndividualBookingsTable
            bookings={filteredBookings}
            bookingStatuses={bookingsStatusFilters}
            updateGlobalFilters={({ bookingStatus }) => {
              setBookingsStatusFilter(bookingStatus ?? [])
            }}
            resetFilters={() => setBookingsStatusFilter([])}
          />
        </>
      ) : (
        <Spinner />
      )}
    </>
  )
}
