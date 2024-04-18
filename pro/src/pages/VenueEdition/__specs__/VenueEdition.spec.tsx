import { screen, waitForElementToBeRemoved } from '@testing-library/react'
import React from 'react'
import { Route, Routes } from 'react-router-dom'

import { api } from 'apiClient/api'
import { GetVenueResponseModel, VenueProviderResponse } from 'apiClient/v1'
import { defaultGetVenue } from 'utils/collectiveApiFactories'
import {
  RenderWithProvidersOptions,
  renderWithProviders,
} from 'utils/renderWithProviders'

import { VenueEdition } from '../VenueEdition'

const renderVenueEdition = (options?: RenderWithProvidersOptions) => {
  const storeOverrides = {
    user: {
      initialized: true,
      currentUser: {
        id: 'EY',
        isAdmin: false,
      },
    },
  }

  return renderWithProviders(
    <Routes>
      <Route
        path="/structures/:offererId/lieux/:venueId/*"
        element={<VenueEdition />}
      />
      <Route path="/accueil" element={<h1>Home</h1>} />
    </Routes>,
    {
      storeOverrides,
      initialRouterEntries: [
        `/structures/${defaultGetOffererResponseModel.id}/lieux/${defaultGetVenue.id}/edition`,
      ],
      ...options,
    }
  )
}

vi.mock('react-router-dom', async () => ({
  ...(await vi.importActual('react-router-dom')),
  useParams: () => ({
    offererId: '1234',
    venueId: '12',
  }),
  useNavigate: vi.fn(),
}))

describe('route VenueEdition', () => {
  let venue: GetVenueResponseModel
  let venueProviders: VenueProviderResponse[]

  beforeEach(() => {
    venue = {
      ...defaultGetVenue,
      publicName: 'Cinéma des iles',
      dmsToken: 'dms-token-12345',
      isPermanent: true,
    }

    venueProviders = [
      {
        id: 1,
        isActive: true,
        isFromAllocineProvider: false,
        lastSyncDate: undefined,
        venueId: 2,
        venueIdAtOfferProvider: 'cdsdemorc1',
        provider: {
          name: 'Ciné Office',
          id: 12,
          hasOffererProvider: false,
          isActive: true,
        },
        quantity: 0,
        isDuo: true,
        price: 0,
      },
    ]

    vi.spyOn(api, 'getVenue').mockResolvedValue(venue)
    vi.spyOn(api, 'listVenueProviders').mockResolvedValue({
      venue_providers: venueProviders,
    })
    vi.spyOn(api, 'getOfferer').mockResolvedValue(
      defaultGetOffererResponseModel
    )
    vi.spyOn(api, 'getVenueTypes').mockResolvedValue([])
    vi.spyOn(api, 'fetchVenueLabels').mockResolvedValue([])
    vi.spyOn(api, 'listOffers').mockResolvedValue([])
  })

  it('should call getVenue and display Venue Form screen on success', async () => {
    renderVenueEdition()

    const venuePublicName = await screen.findByRole('heading', {
      name: 'Cinéma des iles',
    })
    expect(api.getVenue).toHaveBeenCalledWith(12)
    expect(venuePublicName).toBeInTheDocument()
  })

  it('should check none accessibility', async () => {
    vi.spyOn(api, 'getVenue').mockResolvedValueOnce({
      ...venue,
      siret: undefined,
      visualDisabilityCompliant: false,
      mentalDisabilityCompliant: false,
      audioDisabilityCompliant: false,
      motorDisabilityCompliant: false,
    })

    renderVenueEdition()

    await screen.findByRole('heading', {
      name: 'Cinéma des iles',
    })

    expect(
      screen.getByLabelText('Non accessible', { exact: false })
    ).toBeChecked()
  })

  it('should not check none accessibility if every accessibility parameters are null', async () => {
    vi.spyOn(api, 'getVenue').mockResolvedValueOnce({
      ...venue,
      visualDisabilityCompliant: null,
      mentalDisabilityCompliant: null,
      audioDisabilityCompliant: null,
      motorDisabilityCompliant: null,
    })

    renderVenueEdition()

    await screen.findByRole('heading', {
      name: 'Cinéma des iles',
    })

    expect(
      screen.getByLabelText('Non accessible', { exact: false })
    ).not.toBeChecked()
  })

  it('should not render reimbursement fields when FF bank details is enabled and venue has no siret', async () => {
    vi.spyOn(api, 'getVenue').mockResolvedValueOnce({
      ...venue,
      siret: '11111111111111',
    })

    renderVenueEdition()

    await screen.findByRole('heading', {
      name: 'Cinéma des iles',
    })

    expect(
      screen.queryByText(/Barème de remboursement/)
    ).not.toBeInTheDocument()
  })

  it('should display Opening hours section if WIP_OPENING_HOURS feature flag is enabled and venue is permanent', async () => {
    renderVenueEdition({ features: ['WIP_OPENING_HOURS'] })

    await waitForElementToBeRemoved(screen.getByTestId('spinner'))

    expect(screen.getByText("Horaires d'ouverture")).toBeInTheDocument()
  })

  it('should not display Opening hours section if WIP_OPENING_HOURS feature flag is disabled', async () => {
    renderVenueEdition()

    await waitForElementToBeRemoved(screen.getByTestId('spinner'))

    expect(screen.queryByText("Horaires d'ouverture")).not.toBeInTheDocument()
  })

  it('should display the acces libre callout for permanent venues', async () => {
    venue.isPermanent = true
    renderVenueEdition({
      features: ['WIP_ACCESLIBRE'],
      initialRouterEntries: [
        `/structures/${defaultGetOffererResponseModel.id}/lieux/${defaultGetVenue.id}`,
      ],
    })

    await waitForElementToBeRemoved(screen.getByTestId('spinner'))

    expect(
      screen.getByText(
        'Renseignez facilement les modalités d’accessibilité de votre établissement sur la plateforme collaborative acceslibre.beta.gouv.fr'
      )
    ).toBeInTheDocument()
  })

  it('should not display the acces libre callout for non permanent venues', async () => {
    venue.isPermanent = false
    renderVenueEdition({
      features: ['WIP_ACCESLIBRE'],
      initialRouterEntries: [
        `/structures/${defaultGetOffererResponseModel.id}/lieux/${defaultGetVenue.id}`,
      ],
    })

    await waitForElementToBeRemoved(screen.getByTestId('spinner'))

    expect(
      screen.queryByText(
        'Renseignez facilement les modalités d’accessibilité de votre établissement sur la plateforme collaborative acceslibre.beta.gouv.fr'
      )
    ).not.toBeInTheDocument()
  })
})
