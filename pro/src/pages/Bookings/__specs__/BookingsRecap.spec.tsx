import { screen, waitFor } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import React from 'react'

import { api } from 'apiClient/api'
import {
  SharedCurrentUserResponseModel,
  VenueListItemResponseModel,
} from 'apiClient/v1'
import { ApiError } from 'apiClient/v2'
import { ApiRequestOptions } from 'apiClient/v2/core/ApiRequestOptions'
import { ApiResult } from 'apiClient/v2/core/ApiResult'
import { FETCH_ERROR_MESSAGE } from 'app/App/App'
import Notification from 'components/Notification/Notification'
import { DEFAULT_PRE_FILTERS } from 'core/Bookings/constants'
import {
  FORMAT_ISO_DATE_ONLY,
  formatBrowserTimezonedDateAsUTC,
} from 'utils/date'
import {
  bookingRecapFactory,
  venueListItemFactory,
} from 'utils/individualApiFactories'
import { renderWithProviders } from 'utils/renderWithProviders'

import { Bookings } from '../Bookings'

vi.mock('apiClient/api', () => ({
  api: {
    getProfile: vi.fn(),
    getBookingsPro: vi.fn(),
    getVenues: vi.fn(),
    getUserHasBookings: vi.fn(),
    getBookingsCsv: vi.fn(),
  },
}))

vi.mock('utils/date', async () => {
  return {
    ...(await vi.importActual('utils/date')),
    getToday: vi.fn().mockReturnValue(new Date('2020-06-15T12:00:00Z')),
  }
})

const NTH_ARGUMENT_GET_BOOKINGS = {
  page: 1,
  venueId: 2,
  eventDate: 4,
  bookingBeginningDate: 6,
  bookingEndingDate: 7,
}

const renderBookingsRecap = async (
  storeOverrides: any,
  initialEntries = '/reservations',
  waitDomReady?: boolean
) => {
  const rtlReturn = renderWithProviders(
    <>
      <Bookings />
      <Notification />
    </>,
    { storeOverrides, initialRouterEntries: [initialEntries] }
  )

  const { hasBookings } = await api.getUserHasBookings()
  const displayBookingsButton = screen.getByRole('button', { name: 'Afficher' })
  const downloadBookingsCsvButton = screen.getByRole('button', {
    name: 'Télécharger',
  })

  const submitFilters = async () => {
    await userEvent.click(displayBookingsButton)
  }
  const submitDownloadFilters = async () => {
    await userEvent.click(downloadBookingsCsvButton)
  }

  if (waitDomReady || waitDomReady === undefined) {
    if (hasBookings) {
      await waitFor(() => expect(displayBookingsButton).not.toBeDisabled())
    } else {
      const loadingMessage = screen.queryByText('Chargement en cours ...')
      await waitFor(() => expect(loadingMessage).not.toBeInTheDocument())
    }
  }

  return {
    rtlReturn,
    submitDownloadFilters,
    submitFilters,
  }
}

describe('components | BookingsRecap | Pro user', () => {
  let store: any
  let venue: VenueListItemResponseModel
  let user

  beforeEach(() => {
    const emptyBookingsRecapPage = {
      bookingsRecap: [],
      page: 0,
      pages: 0,
      total: 0,
    }
    vi.spyOn(api, 'getBookingsPro').mockResolvedValue(emptyBookingsRecapPage)

    user = {
      isAdmin: false,
      email: 'rené@example.com',
    } as SharedCurrentUserResponseModel
    store = {
      user: {
        currentUser: user,
      },
    }
    vi.spyOn(api, 'getProfile').mockResolvedValue(user)
    venue = venueListItemFactory()
    vi.spyOn(api, 'getVenues').mockResolvedValue({ venues: [venue] })
    vi.spyOn(api, 'getUserHasBookings').mockResolvedValue({ hasBookings: true })
  })

  it('should show a pre-filter section', async () => {
    await renderBookingsRecap(store)

    const eventDateFilter = screen.getByLabelText('Date de l’évènement')
    const eventVenueFilter = screen.getByLabelText('Lieu')
    const eventBookingPeriodFilter = screen.getByText('Période de réservation')
    expect(eventDateFilter).toBeInTheDocument()
    expect(eventVenueFilter).toBeInTheDocument()
    expect(eventBookingPeriodFilter).toBeInTheDocument()
    expect(eventVenueFilter).toHaveValue(DEFAULT_PRE_FILTERS.offerVenueId)
    expect(eventDateFilter).not.toHaveValue()
  })

  it('should ask user to select a pre-filter before clicking on "Afficher"', async () => {
    await renderBookingsRecap(store)

    expect(api.getBookingsPro).not.toHaveBeenCalled()
    const choosePreFiltersMessage = screen.getByText(
      'Pour visualiser vos réservations, veuillez sélectionner un ou plusieurs des filtres précédents et cliquer sur « Afficher »'
    )
    expect(choosePreFiltersMessage).toBeInTheDocument()
  })

  it('should request bookings of venue requested by user when user clicks on "Afficher"', async () => {
    const bookingRecap = bookingRecapFactory()
    const spyGetBookingsPro = vi
      .spyOn(api, 'getBookingsPro')
      .mockResolvedValue({
        page: 1,
        pages: 1,
        total: 1,
        bookingsRecap: [bookingRecap],
      })
    const { submitFilters } = await renderBookingsRecap(store)

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.id.toString()
    )
    await submitFilters()

    await screen.findAllByText(bookingRecap.stock.offerName)
    expect(
      spyGetBookingsPro.mock.calls[0][NTH_ARGUMENT_GET_BOOKINGS.venueId - 1]
    ).toBe(venue.id.toString())
  })

  it('should warn user that his prefilters returned no booking when no bookings where returned by selected pre-filters', async () => {
    vi.spyOn(api, 'getBookingsPro').mockResolvedValue({
      page: 1,
      pages: 0,
      total: 0,
      bookingsRecap: [],
    })
    const { submitFilters } = await renderBookingsRecap(store)

    await submitFilters()

    const noBookingsForPreFilters = await screen.findByText(
      'Aucune réservation trouvée pour votre recherche'
    )
    expect(noBookingsForPreFilters).toBeInTheDocument()
  })

  it('should allow user to reset its pre-filters in the no bookings warning', async () => {
    vi.spyOn(api, 'getBookingsPro').mockResolvedValue({
      page: 1,
      pages: 0,
      total: 0,
      bookingsRecap: [],
    })
    const { submitFilters } = await renderBookingsRecap(store)
    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.id.toString()
    )
    await submitFilters()

    const resetButton = screen.getByText('Afficher toutes les réservations', {
      selector: '.button-ternary-pink',
    })
    await userEvent.click(resetButton)

    expect(screen.getByLabelText('Lieu')).toHaveValue(
      DEFAULT_PRE_FILTERS.offerVenueId
    )
  })

  it('should not allow user to reset prefilters when none were applied', async () => {
    const bookingRecap = bookingRecapFactory()
    vi.spyOn(api, 'getBookingsPro').mockResolvedValue({
      page: 1,
      pages: 1,
      total: 1,
      bookingsRecap: [bookingRecap],
    })
    const { submitFilters } = await renderBookingsRecap(store)

    await submitFilters()

    expect(
      screen.getByRole('button', { name: 'Réinitialiser les filtres' })
    ).toBeDisabled()
  })

  it('should allow user to reset prefilters when some where applied', async () => {
    const bookingRecap = bookingRecapFactory()
    vi.spyOn(api, 'getBookingsPro').mockResolvedValue({
      page: 1,
      pages: 1,
      total: 1,
      bookingsRecap: [bookingRecap],
    })
    const { submitFilters } = await renderBookingsRecap(store)
    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.id.toString()
    )
    const beginningPeriodInput = screen.getByLabelText('Début de la période')
    const endingPeriodInput = screen.getByLabelText('Fin de la période')
    expect(beginningPeriodInput).toHaveDisplayValue(['2020-05-16'])
    expect(endingPeriodInput).toHaveDisplayValue(['2020-06-15'])

    await userEvent.type(beginningPeriodInput, '2019-01-01')
    await userEvent.type(endingPeriodInput, '2019-02-01')
    await submitFilters()

    const resetButton = await screen.findByText('Réinitialiser les filtres')
    await userEvent.click(resetButton)

    expect(screen.getByLabelText('Lieu')).toHaveValue(
      DEFAULT_PRE_FILTERS.offerVenueId
    )

    await waitFor(() =>
      expect(beginningPeriodInput).toHaveDisplayValue(['2020-05-16'])
    )
    expect(endingPeriodInput).toHaveDisplayValue(['2020-06-15'])
  })

  it('should ask user to select a pre-filter when user reset them', async () => {
    const bookingRecap = bookingRecapFactory()
    vi.spyOn(api, 'getBookingsPro').mockResolvedValue({
      page: 1,
      pages: 1,
      total: 1,
      bookingsRecap: [bookingRecap],
    })
    const { submitFilters } = await renderBookingsRecap(store)
    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.id.toString()
    )
    await submitFilters()

    const resetButton = await screen.findByText('Réinitialiser les filtres')
    await userEvent.click(resetButton)

    expect(
      screen.getByRole('button', { name: 'Réinitialiser les filtres' })
    ).toBeDisabled()
    const choosePreFiltersMessage = screen.getByText(
      'Pour visualiser vos réservations, veuillez sélectionner un ou plusieurs des filtres précédents et cliquer sur « Afficher »'
    )
    expect(choosePreFiltersMessage).toBeInTheDocument()
  })

  it('should have a CSV download button', async () => {
    await renderBookingsRecap(store)

    expect(
      screen.getByRole('button', { name: 'Télécharger' })
    ).toBeInTheDocument()
  })

  it('should fetch API for CSV when clicking on the download button and disable button while its loading', async () => {
    const { submitDownloadFilters } = await renderBookingsRecap({
      ...store,
    })

    // submit utils method wait for button to become disabled then enabled.
    await submitDownloadFilters()
    const downloadSubButton = await screen.findByRole('button', {
      name: 'Fichier CSV (.csv)',
    })
    await userEvent.click(downloadSubButton)

    expect(api.getBookingsCsv).toHaveBeenCalledWith(
      1,
      null,
      null,
      null,
      DEFAULT_PRE_FILTERS.bookingStatusFilter,
      DEFAULT_PRE_FILTERS.bookingBeginningDate,
      DEFAULT_PRE_FILTERS.bookingEndingDate,
      null
    )
  })

  it('should display an error message on CSV download when API returns a status other than 200', async () => {
    vi.spyOn(api, 'getBookingsCsv').mockRejectedValueOnce(
      new ApiError({} as ApiRequestOptions, { status: 400 } as ApiResult, '')
    )

    const { submitDownloadFilters } = await renderBookingsRecap({
      ...store,
    })

    await submitDownloadFilters()
    const downloadSubButton = await screen.findByRole('button', {
      name: 'Fichier CSV (.csv)',
    })
    await userEvent.click(downloadSubButton)

    expect(
      await screen.findByText(FETCH_ERROR_MESSAGE, { exact: false })
    ).toBeInTheDocument()
  })

  it('should fetch bookings for the filtered venue as many times as the number of pages', async () => {
    const bookings1 = bookingRecapFactory()
    const bookings2 = bookingRecapFactory()
    const paginatedBookingRecapReturned = {
      page: 1,
      pages: 2,
      total: 2,
      bookingsRecap: [bookings1],
    }
    const secondPaginatedBookingRecapReturned = {
      page: 2,
      pages: 2,
      total: 2,
      bookingsRecap: [bookings2],
    }
    const spyGetBookingsPro = vi
      .spyOn(api, 'getBookingsPro')
      .mockResolvedValueOnce(paginatedBookingRecapReturned)
      .mockResolvedValueOnce(secondPaginatedBookingRecapReturned)

    const { submitFilters } = await renderBookingsRecap(store)

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.id.toString()
    )
    await submitFilters()

    expect(screen.getByText(bookings2.stock.offerName)).toBeInTheDocument()

    expect(screen.getByText(bookings1.stock.offerName)).toBeInTheDocument()

    expect(api.getBookingsPro).toHaveBeenCalledTimes(2)
    expect(
      spyGetBookingsPro.mock.calls[0][NTH_ARGUMENT_GET_BOOKINGS.page - 1]
    ).toBe(1)
    expect(
      spyGetBookingsPro.mock.calls[0][NTH_ARGUMENT_GET_BOOKINGS.venueId - 1]
    ).toBe(venue.id.toString())
    expect(
      spyGetBookingsPro.mock.calls[1][NTH_ARGUMENT_GET_BOOKINGS.page - 1]
    ).toBe(2)
    expect(
      spyGetBookingsPro.mock.calls[1][NTH_ARGUMENT_GET_BOOKINGS.venueId - 1]
    ).toBe(venue.id.toString())
  })

  it('should request bookings of event date requested by user when user clicks on "Afficher"', async () => {
    const bookingRecap = bookingRecapFactory()
    const spyGetBookingsPro = vi
      .spyOn(api, 'getBookingsPro')
      .mockResolvedValue({
        page: 1,
        pages: 1,
        total: 1,
        bookingsRecap: [bookingRecap],
      })
    const { submitFilters } = await renderBookingsRecap(store)

    await userEvent.type(
      screen.getByLabelText('Date de l’évènement'),
      '2020-06-08'
    )
    await submitFilters()

    await screen.findAllByText(bookingRecap.stock.offerName)
    expect(
      spyGetBookingsPro.mock.calls[0][NTH_ARGUMENT_GET_BOOKINGS.eventDate - 1]
    ).toStrictEqual(
      formatBrowserTimezonedDateAsUTC(
        new Date(2020, 5, 8),
        FORMAT_ISO_DATE_ONLY
      )
    )
  })

  it('should set booking period to null when user select event date', async () => {
    const bookingRecap = bookingRecapFactory()
    const spyGetBookingsPro = vi
      .spyOn(api, 'getBookingsPro')
      .mockResolvedValue({
        page: 1,
        pages: 1,
        total: 1,
        bookingsRecap: [bookingRecap],
      })
    const { submitFilters } = await renderBookingsRecap(store)

    await userEvent.type(
      screen.getByLabelText('Date de l’évènement'),
      '2020-08-10'
    )
    await submitFilters()

    await screen.findAllByText(bookingRecap.stock.offerName)
    expect(
      spyGetBookingsPro.mock.calls[0][
        NTH_ARGUMENT_GET_BOOKINGS.bookingEndingDate - 1
      ]
    ).toBeUndefined()
    expect(
      spyGetBookingsPro.mock.calls[0][
        NTH_ARGUMENT_GET_BOOKINGS.bookingBeginningDate - 1
      ]
    ).toBeUndefined()
  })

  it('should request bookings of default period when user clicks on "Afficher" without selecting a period', async () => {
    const bookingRecap = bookingRecapFactory()

    const spyGetBookingsPro = vi
      .spyOn(api, 'getBookingsPro')
      .mockResolvedValue({
        page: 1,
        pages: 1,
        total: 1,
        bookingsRecap: [bookingRecap],
      })
    const { submitFilters } = await renderBookingsRecap(store)

    await submitFilters()

    await screen.findAllByText(bookingRecap.stock.offerName)
    expect(
      spyGetBookingsPro.mock.calls[0][
        NTH_ARGUMENT_GET_BOOKINGS.bookingBeginningDate - 1
      ]
    ).toStrictEqual(DEFAULT_PRE_FILTERS.bookingBeginningDate)
    expect(
      spyGetBookingsPro.mock.calls[0][
        NTH_ARGUMENT_GET_BOOKINGS.bookingEndingDate - 1
      ]
    ).toStrictEqual(DEFAULT_PRE_FILTERS.bookingEndingDate)
  })

  it('should request bookings of selected period when user clicks on "Afficher"', async () => {
    const bookingRecap = bookingRecapFactory()
    const spyGetBookingsPro = vi
      .spyOn(api, 'getBookingsPro')
      .mockResolvedValue({
        page: 1,
        pages: 1,
        total: 1,
        bookingsRecap: [bookingRecap],
      })
    const { submitFilters } = await renderBookingsRecap(store)

    const beginningPeriodInput = screen.getByLabelText('Début de la période')
    const endingPeriodInput = screen.getByLabelText('Fin de la période')

    await userEvent.clear(beginningPeriodInput)
    await userEvent.clear(endingPeriodInput)
    await userEvent.type(beginningPeriodInput, '2020-05-10')
    await userEvent.type(endingPeriodInput, '2020-06-05')
    await submitFilters()

    await screen.findAllByText(bookingRecap.stock.offerName)
    expect(
      spyGetBookingsPro.mock.calls[0][
        NTH_ARGUMENT_GET_BOOKINGS.bookingBeginningDate - 1
      ]
    ).toStrictEqual('2020-05-10')
    expect(
      spyGetBookingsPro.mock.calls[0][
        NTH_ARGUMENT_GET_BOOKINGS.bookingEndingDate - 1
      ]
    ).toStrictEqual('2020-06-05')
  })

  it('should reset bookings recap list when applying filters', async () => {
    const booking = bookingRecapFactory()
    const otherVenueBooking = bookingRecapFactory()
    const otherVenue = venueListItemFactory()
    vi.spyOn(api, 'getVenues').mockResolvedValue({
      venues: [venue, otherVenue],
    })
    const paginatedBookingRecapReturned = {
      page: 1,
      pages: 1,
      total: 1,
      bookingsRecap: [booking],
    }
    const otherVenuePaginatedBookingRecapReturned = {
      page: 1,
      pages: 1,
      total: 1,
      bookingsRecap: [otherVenueBooking],
    }
    vi.spyOn(api, 'getBookingsPro')
      .mockResolvedValueOnce(otherVenuePaginatedBookingRecapReturned)
      .mockResolvedValueOnce(paginatedBookingRecapReturned)

    const { submitFilters } = await renderBookingsRecap(store)

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      otherVenue.id.toString()
    )
    await submitFilters()

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.id.toString()
    )
    await submitFilters()

    expect(screen.getByText(booking.stock.offerName)).toBeInTheDocument()
    expect(
      screen.queryByText(otherVenueBooking.stock.offerName)
    ).not.toBeInTheDocument()
  })

  it('should show notification with information message when there are more than 5 pages', async () => {
    const bookingsRecap = { pages: 6, bookingsRecap: [] }
    vi.spyOn(api, 'getBookingsPro')
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 1 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 2 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 3 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 4 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 5 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 6 })
    await renderBookingsRecap(store)

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.id.toString()
    )
    await userEvent.click(screen.getByText('Afficher', { selector: 'button' }))

    const informationalMessage = await screen.findByText(
      'L’affichage des réservations a été limité à 5 000 réservations. Vous pouvez modifier les filtres pour affiner votre recherche.'
    )
    expect(informationalMessage).toBeInTheDocument()
    expect(api.getBookingsPro).toHaveBeenCalledTimes(5)
  })

  it('should not show notification with information message when there are 5 pages or less', async () => {
    const bookingsRecap = { pages: 5, bookingsRecap: [] }
    vi.spyOn(api, 'getBookingsPro')
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 1 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 2 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 3 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 4 })
      // @ts-expect-error FIX ME
      .mockResolvedValueOnce({ ...bookingsRecap, page: 5 })
    await renderBookingsRecap(store)

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.id.toString()
    )
    await userEvent.click(screen.getByText('Afficher', { selector: 'button' }))

    expect(api.getBookingsPro).toHaveBeenCalledTimes(5)
    const informationalMessage = screen.queryByText(
      'L’affichage des réservations a été limité à 5 000 réservations. Vous pouvez modifier les filtres pour affiner votre recherche.'
    )
    expect(informationalMessage).not.toBeInTheDocument()
  })

  it('should inform the user that the filters have been modified when at least one of them was and before clicking on the "Afficher" button', async () => {
    const { submitFilters } = await renderBookingsRecap(store)
    await submitFilters()

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.publicName ?? venue.name
    )

    const informationalMessage = await screen.findByTestId(
      'refresh-required-message'
    )
    expect(informationalMessage).toBeInTheDocument()
  })

  it('should not inform the user when the selected filter is the same than the actual filter', async () => {
    await renderBookingsRecap(store)
    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.publicName ?? venue.name
    )

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      screen.getByText('Tous les lieux')
    )

    const informationalMessage = screen.queryByText(
      'Vos filtres ont été modifiés. Veuillez cliquer sur « Afficher » pour actualiser votre recherche.'
    )
    expect(informationalMessage).not.toBeInTheDocument()
  })

  it('should not inform the user of pre-filter modifications before first click on "Afficher" button', async () => {
    await renderBookingsRecap(store)

    await userEvent.selectOptions(
      screen.getByLabelText('Lieu'),
      venue.publicName ?? venue.name
    )

    const informationalMessage = screen.queryByText(
      'Vos filtres ont été modifiés. Veuillez cliquer sur « Afficher » pour actualiser votre recherche.'
    )
    expect(informationalMessage).not.toBeInTheDocument()
  })

  it('should display no booking screen when user does not have any booking yet', async () => {
    //Given
    vi.spyOn(api, 'getUserHasBookings').mockResolvedValue({
      hasBookings: false,
    })
    await renderBookingsRecap(store)

    //Then
    const displayBookingsButton = screen.getByRole('button', {
      name: 'Afficher',
    })
    const downloadBookingsCsvButton = screen.getByRole('button', {
      name: 'Télécharger',
    })
    const informationMessage = await screen.findByText(
      'Vous n’avez aucune réservation pour le moment'
    )

    expect(displayBookingsButton).toBeDisabled()
    expect(downloadBookingsCsvButton).toBeDisabled()
    expect(informationMessage).toBeInTheDocument()
  })
})
