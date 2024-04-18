import format from 'date-fns/format'
import { useState } from 'react'
import useSWR from 'swr'

import { api } from 'apiClient/api'
import { BookingExportType, BookingsExportStatusFilter } from 'apiClient/v1'
import DialogBox from 'components/DialogBox'
import { GET_EVENT_PRICE_CATEGORIES_AND_SCHEDULES_BY_DAYE_QUERY_KEY } from 'config/swrQueryKeys'
import strokeDeskIcon from 'icons/stroke-desk.svg'
import { daysOfWeek } from 'pages/VenueEdition/OpeningHoursForm/OpeningHoursForm'
import { Button } from 'ui-kit'
import { ButtonVariant } from 'ui-kit/Button/types'
import { BaseRadio } from 'ui-kit/form/shared'
import RadioButtonWithImage from 'ui-kit/RadioButtonWithImage'
import Spinner from 'ui-kit/Spinner/Spinner'
import { FORMAT_DD_MM_YYYY } from 'utils/date'
import { downloadFile } from 'utils/downloadFile'
import { pluralize } from 'utils/pluralize'

import style from './DownloadBookingsModal.module.scss'

interface DownloadBookingsModalProps {
  offerId: number
  onDimiss: () => void
}

export const DownloadBookingsModal = ({
  offerId,
  onDimiss,
}: DownloadBookingsModalProps) => {
  const [bookingsType, setBookingsType] = useState<BookingsExportStatusFilter>()
  const [selectedDate, setSelectedDate] = useState<string>()

  const stockSchedulesAndPricesByDateQuery = useSWR(
    [GET_EVENT_PRICE_CATEGORIES_AND_SCHEDULES_BY_DAYE_QUERY_KEY],
    () => api.getOfferPriceCategoriesAndSchedulesByDates(offerId),
    { fallbackData: [] }
  )

  const handleSubmit = async (
    event: React.SyntheticEvent<HTMLFormElement, SubmitEvent>
  ) => {
    event.preventDefault()
    const fileFormat = event.nativeEvent.submitter?.dataset.export
    if (fileFormat === BookingExportType.CSV) {
      downloadFile(
        await api.exportBookingsForOfferAsCsv(
          offerId,
          bookingsType!,
          selectedDate!
        ),
        `reservations-${bookingsType}-${selectedDate}.csv`,
        'text/csv'
      )
    } else if (fileFormat === BookingExportType.EXCEL) {
      downloadFile(
        new Uint8Array(
          await api.exportBookingsForOfferAsExcel(
            offerId,
            bookingsType!,
            selectedDate!
          )
        ),
        `reservations-${bookingsType}-${selectedDate}.xlsx`,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      )
    }
  }

  const createDateRow = (
    eventDate: string,
    schedulesCount: number,
    priceCategoriesCount: number
  ) => {
    const date = new Date(eventDate)
    const day = daysOfWeek[date.getDay()]
    return (
      <tr key={eventDate} className={style['table-row']}>
        <td className={style['table-column']}>
          <BaseRadio
            type="radio"
            value={eventDate}
            name="bookings-date-select"
            checked={selectedDate === eventDate}
            className={style['bookings-date-radio']}
            withBorder={false}
            label={
              <div className={style['radio-label']}>
                <abbr title={day} className={style['bookings-day']}>
                  {day.substring(0, 3)}
                </abbr>
                <span>{format(date, FORMAT_DD_MM_YYYY)}</span>
              </div>
            }
            onChange={() => setSelectedDate(eventDate)}
          />
        </td>
        <td className={style['table-column']}>
          {pluralize(schedulesCount, 'horaire')}
        </td>
        <td className={style['table-column']}>
          {pluralize(priceCategoriesCount, 'tarif')}
        </td>
      </tr>
    )
  }

  return (
    <DialogBox
      hasCloseButton
      labelledBy="download-bookings-modal"
      onDismiss={onDimiss}
    >
      <form onSubmit={handleSubmit}>
        <div className={style['container']}>
          <h1 id="download-bookings-modal" className={style['header']}>
            Télécharger vos réservations
          </h1>
          <fieldset className={style['date-select-section']}>
            <legend>
              <div>Sélectionner la date:</div>
            </legend>
            {stockSchedulesAndPricesByDateQuery.isLoading ? (
              <Spinner />
            ) : (
              <>
                <div className={style['bookings-date-count']}>
                  {pluralize(
                    stockSchedulesAndPricesByDateQuery.data.length,
                    'date'
                  )}
                </div>
                <hr className={style['horizontal-line']} />
                <table className={style['date-select-table']}>
                  <thead className={style['date-select-table-header']}>
                    <tr>
                      <th scope="col" className={style['table-header']}>
                        Date
                      </th>
                      <th className={style['table-header']} scope="col">
                        Horaires
                      </th>
                      <th className={style['table-header']} scope="col">
                        Tarifs
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {stockSchedulesAndPricesByDateQuery.data.map((date) =>
                      createDateRow(
                        date.eventDate,
                        date.scheduleCount,
                        date.priceCategoriesCount
                      )
                    )}
                  </tbody>
                </table>
                <hr className={style['horizontal-line']} />
              </>
            )}
          </fieldset>
          <fieldset>
            <legend>
              <div>Sélectionnez le type de réservations :</div>
            </legend>
            <div className={style['bookings-radio-buttons']}>
              <RadioButtonWithImage
                className={style['bookings-radio-buttons-validated']}
                name="select-bookings-type"
                icon={strokeDeskIcon}
                label="Réservations confirmées et validées uniquement"
                description="Les réservations au statut confirmées et validées ne sont plus annulables par les bénéficiaires."
                isChecked={
                  bookingsType === BookingsExportStatusFilter.VALIDATED
                }
                onChange={() =>
                  setBookingsType(BookingsExportStatusFilter.VALIDATED)
                }
                value={BookingsExportStatusFilter.VALIDATED}
              />
              <RadioButtonWithImage
                name="select-bookings-type"
                icon={strokeDeskIcon}
                label="Toutes les réservations"
                description="Les réservations dont le statut n’est pas “confirmée” ou “validée” pourront encore être annulées par les bénéficiaires."
                isChecked={bookingsType === BookingsExportStatusFilter.ALL}
                onChange={() => setBookingsType(BookingsExportStatusFilter.ALL)}
                value={BookingsExportStatusFilter.ALL}
              />
            </div>
          </fieldset>

          <div className={style['actions']}>
            <Button variant={ButtonVariant.SECONDARY} onClick={onDimiss}>
              Annuler
            </Button>
            <Button
              variant={ButtonVariant.PRIMARY}
              type="submit"
              data-export={BookingExportType.CSV}
              disabled={
                selectedDate === undefined || bookingsType === undefined
              }
            >
              Télécharger au format CSV
            </Button>
            <Button
              variant={ButtonVariant.PRIMARY}
              type="submit"
              data-export={BookingExportType.EXCEL}
              disabled={
                selectedDate === undefined || bookingsType === undefined
              }
            >
              Télécharger au format Excel
            </Button>
          </div>
        </div>
      </form>
    </DialogBox>
  )
}
