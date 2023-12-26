import { screen } from '@testing-library/react'
import React from 'react'

import { INITIAL_OFFERER_VENUES } from 'pages/Home/OffererVenues'
import {
  defaultGetOffererResponseModel,
  defaultGetOffererVenueResponseModel,
} from 'utils/apiFactories'
import {
  RenderWithProvidersOptions,
  renderWithProviders,
} from 'utils/renderWithProviders'

import Offerers, { OfferersProps } from '../Offerers'

const renderOfferers = (
  props: Partial<OfferersProps> = {},
  options?: RenderWithProvidersOptions
) => {
  renderWithProviders(
    <Offerers
      receivedOffererNames={{
        offerersNames: [{ name: 'name', id: 1 }],
      }}
      onSelectedOffererChange={() => null}
      cancelLoading={() => null}
      selectedOfferer={defaultGetOffererResponseModel}
      isLoading={false}
      hasAtLeastOnePhysicalVenue={false}
      isUserOffererValidated
      venues={INITIAL_OFFERER_VENUES}
      {...props}
    />,
    options
  )
}

describe('Offerers', () => {
  it('should not display venue soft deleted if user is not validated', () => {
    renderOfferers({ isUserOffererValidated: false })

    expect(
      screen.getByText(
        /Le rattachement à votre structure est en cours de traitement par les équipes du pass Culture/
      )
    ).toBeInTheDocument()
    expect(
      screen.queryByText(
        /Votre structure a été désactivée. Pour plus d’informations sur la désactivation veuillez contacter notre support./
      )
    ).not.toBeInTheDocument()
  })

  it('should display venue soft deleted', () => {
    renderOfferers()

    expect(
      screen.queryByText(
        /Votre structure a été désactivée. Pour plus d’informations sur la désactivation veuillez contacter notre support./
      )
    ).toBeInTheDocument()
  })

  it("should display the carnet d'adresses", () => {
    renderOfferers(
      {
        selectedOfferer: {
          ...defaultGetOffererResponseModel,
          managedVenues: [defaultGetOffererVenueResponseModel],
          isActive: true,
        },
      },
      { features: ['WIP_PARTNER_PAGE'] }
    )

    expect(screen.getByText('Carnet d’adresses')).toBeInTheDocument()
  })
})
