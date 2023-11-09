declare namespace Cypress {
  interface Chainable {
    logout(): Chainable
    login(email: string, password: string, redirectUrl?: string): Chainable
    setFeatureFlags(features: Feature[]): Chainable
  }
}

interface Feature {
  name: string
  isActive: boolean
}
