import { screen, waitFor } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import React from 'react'

import { api } from 'apiClient/api'
import { BankAccountApplicationStatus } from 'apiClient/v1'
import Notification from 'components/Notification/Notification'
import LinkVenuesDialog, {
  LinkVenuesDialogProps,
} from 'pages/Reimbursements/BankInformations/LinkVenuesDialog'
import { renderWithProviders } from 'utils/renderWithProviders'

vi.mock('apiClient/api', () => ({
  api: {
    linkVenueToBankAccount: vi.fn(),
  },
}))

const mockClose = vi.fn()

const storeOverrides = {
  user: {
    currentUser: {
      isAdmin: false,
      hasSeenProTutorials: true,
    },
    initialized: true,
  },
}

const props: LinkVenuesDialogProps = {
  closeDialog: mockClose,
  managedVenues: [
    {
      bankAccountId: 6877,
      commonName: 'Lieu 1',
      id: 1,
      siret: 'e96a1fd4-3361-41c9-894a-89e0378b0962',
      hasPricingPoint: true,
    },
    {
      bankAccountId: null,
      commonName: 'Lieu 2',
      id: 2,
      siret: 'e96a1fd4-3361-41c9-894a-89e0378b0962',
      hasPricingPoint: true,
    },
  ],
  offererId: 1,
  selectedBankAccount: {
    bic: '04d374fc-8338-45c2-a1e7-3a221991fda9',
    dateCreated: '1995-04-07',
    dsApplicationId: 11,
    id: 6877,
    isActive: true,
    label:
      'Pizza mattress searches wellness entirely transition azerbaijan, quit tournament.',
    linkedVenues: [
      {
        commonName: 'Lieu 1',
        id: 1,
      },
    ],
    obfuscatedIban: 'xxxx-xxxxx-xxxx-xxxx-3a221991fda9',
    status: BankAccountApplicationStatus.ACCEPTE,
  },
}

describe('LinkVenueDialog', () => {
  beforeEach(() => {
    vi.spyOn(api, 'linkVenueToBankAccount').mockResolvedValue()
  })

  it('Should display the dialog', async () => {
    renderWithProviders(<LinkVenuesDialog {...props} />, {
      storeOverrides,
    })

    expect(
      screen.getByText(
        /Sélectionnez les lieux dont les offres seront remboursées sur ce compte bancaire/
      )
    ).toBeInTheDocument()

    expect(screen.getByText(/1 lieu sélectionné/)).toBeInTheDocument()

    expect(screen.getByLabelText('Lieu 1')).toBeChecked()
    expect(screen.getByLabelText('Lieu 2')).not.toBeChecked()
  })

  it('Should be able to submit the form', async () => {
    renderWithProviders(
      <>
        <LinkVenuesDialog {...props} />
        <Notification />
      </>,
      {
        storeOverrides,
      }
    )

    expect(
      screen.getByRole('button', {
        name: 'Enregistrer',
      })
    ).toBeDisabled()

    await userEvent.click(
      screen.getByRole('checkbox', {
        name: 'Lieu 2',
      })
    )

    await waitFor(() =>
      expect(
        screen.getByRole('button', {
          name: 'Enregistrer',
        })
      ).not.toBeDisabled()
    )

    await userEvent.click(
      screen.getByRole('button', {
        name: 'Enregistrer',
      })
    )

    expect(api.linkVenueToBankAccount).toHaveBeenCalledWith(1, 6877, {
      venues_ids: [1, 2],
    })

    expect(
      await screen.findByText(/Vos modifications ont bien été prises en compte/)
    ).toBeInTheDocument()
  })

  it('Should handle update failure', async () => {
    vi.spyOn(api, 'linkVenueToBankAccount').mockRejectedValueOnce({})

    renderWithProviders(
      <>
        <LinkVenuesDialog {...props} />
        <Notification />
      </>,
      {
        storeOverrides,
      }
    )

    await userEvent.click(
      screen.getByRole('checkbox', {
        name: 'Lieu 2',
      })
    )

    await userEvent.click(
      screen.getByRole('button', {
        name: 'Enregistrer',
      })
    )

    expect(
      await screen.findByText(
        /Un erreur est survenue. Vos modifications n’ont pas été prises en compte/
      )
    ).toBeInTheDocument()
  })

  it('Should close the dialog on cancel click', async () => {
    renderWithProviders(<LinkVenuesDialog {...props} />, {
      storeOverrides,
    })

    await userEvent.click(
      screen.getByRole('button', {
        name: 'Annuler',
      })
    )

    expect(mockClose).toHaveBeenCalled()
  })

  it('Should show the discard dialog on cancel click', async () => {
    renderWithProviders(<LinkVenuesDialog {...props} />, {
      storeOverrides,
    })

    await userEvent.click(
      screen.getByRole('checkbox', {
        name: 'Lieu 2',
      })
    )

    await userEvent.click(
      screen.getByRole('button', {
        name: 'Annuler',
      })
    )

    expect(
      screen.getByText(
        /Les informations non sauvegardées ne seront pas prises en compte/
      )
    ).toBeInTheDocument()
  })
})
