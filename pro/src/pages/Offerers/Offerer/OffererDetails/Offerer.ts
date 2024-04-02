import { GetOffererResponseModel } from 'apiClient/v1'

interface ApiKeyType {
  maxAllowed: number
  savedApiKeys: string[]
}

export interface Offerer {
  apiKey: ApiKeyType
  city: string
  name: string
  postalCode: string
  siren: string
  street: string
  id: number
  demarchesSimplifieesApplicationId: string
}

export const transformOffererResponseModelToOfferer = (
  offerer: GetOffererResponseModel
): Offerer => ({
  apiKey: {
    maxAllowed: offerer.apiKey.maxAllowed,
    savedApiKeys: offerer.apiKey.prefixes,
  },
  city: offerer.city || '',
  name: offerer.name || '',
  postalCode: offerer.postalCode || '',
  siren: offerer.siren || '',
  street: offerer.street || '',
  id: offerer.id || 0,
  demarchesSimplifieesApplicationId:
    offerer.demarchesSimplifieesApplicationId || '',
})

export const formatSiren = (siren: string) => {
  if (!siren) {
    return ''
  }

  const blocks = []
  for (let i = 0; i < siren.length; i += 3) {
    blocks.push(siren.substr(i, 3))
  }

  return blocks.join(' ')
}
