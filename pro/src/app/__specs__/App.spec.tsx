import { setUser } from '@sentry/browser'
import { screen, waitFor } from '@testing-library/react'
import React from 'react'
import { Routes, Route } from 'react-router-dom-v5-compat'

import ProtectedRoute from 'app/AppRouter/ProtectedRoute'
import { URL_FOR_MAINTENANCE } from 'utils/config'
import { renderWithProviders } from 'utils/renderWithProviders'

import { App } from '../App'

jest.mock('hooks/useAnalytics', () => ({
  useConfigureFirebase: jest.fn(),
}))

window.scrollTo = jest.fn()

jest.mock('hooks/useLogNavigation', () => jest.fn())

const renderApp = (storeOverrides: any, url = '/') =>
  renderWithProviders(
    <App>
      <Routes>
        <Route path="/" element={<p>Sub component</p>} />
        <Route path="/connexion" element={<p>Login page</p>} />
        <Route
          path="/offres"
          element={
            <ProtectedRoute>
              <p>Private Page</p>
            </ProtectedRoute>
          }
        />
      </Routes>
    </App>,
    { storeOverrides, initialRouterEntries: [url] }
  )

jest.mock('@sentry/browser', () => ({
  setUser: jest.fn(),
}))

jest.spyOn(window, 'scrollTo').mockImplementation()

global.window = Object.create(window)
Object.defineProperty(window, 'location', {
  value: {
    href: 'someurl',
  },
  writable: true,
})

describe('src | App', () => {
  let store: any

  beforeEach(() => {
    store = {
      user: {
        initialized: true,
        currentUser: {
          id: 'user_id',
          publicName: 'François',
          isAdmin: false,
        },
      },
    }
  })

  it('should render App and children components when isMaintenanceActivated is false', async () => {
    renderApp(store)

    expect(await screen.findByText('Sub component')).toBeInTheDocument()
    expect(setUser).toHaveBeenCalledWith({ id: store.user.currentUser.id })
  })

  it('should render a Redirect component when isMaintenanceActivated is true', async () => {
    store = {
      ...store,
      maintenance: {
        isActivated: true,
      },
    }
    renderApp(store)

    await waitFor(() => {
      expect(window.location.href).toEqual(URL_FOR_MAINTENANCE)
    })
  })

  it('should redirect to login when route is private and user not logged in', () => {
    store = {
      ...store,
      user: { initialized: false, currentUser: null },
    }
    renderApp(store, '/offres')

    expect(screen.getByText('Login page')).toBeInTheDocument()
  })
})
