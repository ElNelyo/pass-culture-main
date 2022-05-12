import Package from '../../package.json'

// TODO check empty response type from api
// found the right type into fetch-node types if needed.
// FIX ME
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface EmptyResponse {}

// TODO: ModelObject should be removed when offer.extraData is correctly typed on api
// FIX ME
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface ModelObject {}

export interface ApiErrorResonseMessages {
  global?: string[]
  [key: string]: string[] | undefined
}

export class ApiError extends Error {
  name = 'ApiError'
  content: any
  statusCode: number

  constructor(
    statusCode: number,
    content: ApiErrorResonseMessages,
    message?: string
  ) {
    super(message)
    this.content = content
    this.statusCode = statusCode
  }
}

export const HTTP_STATUS = {
  NO_CONTENT: 204,
  FORBIDDEN: 403,
  SERVICE_UNAVAILABLE: 503,
  GATEWAY_TIMEOUT: 504,
  TOO_MANY_REQUESTS: 429,
  GONE: 410,
  NOT_FOUND: 404,
}

/**
 * For each http calls to the api, retrieves the access token and fetchs.
 * Ignores native/v1/refresh_access_token.
 *
 * First decodes the local access token:
 * on success: continue to the call
 * on error (401): try to refresh the access token
 * on error (other): propagates error
 */
export const safeFetch = async (
  url: string,
  options: RequestInit
): Promise<Response> => {
  const runtimeOptions: RequestInit = {
    ...options,
    headers: {
      ...options.headers,
      'app-version': Package.version,
    },
  }

  /* tslint:disable-next-line */
  return await fetch(url, { ...runtimeOptions, credentials: 'include' })
}

// In this case, the following `any` is not that much of a problem in the context of usage
// with the autogenerated files of swagger-codegen.
// !!! Not encouraging to use `any` anywhere else !!!
export async function handleGeneratedApiResponse(
  response: Response
): Promise<any | void> {
  if (
    response.status === HTTP_STATUS.NO_CONTENT ||
    response.status === HTTP_STATUS.SERVICE_UNAVAILABLE
  ) {
    return {}
  }
  const responseBody = await response.json()
  if (!response.ok) {
    throw new ApiError(
      response.status,
      await responseBody,
      `Échec de la requête ${response.url}, code: ${response.status}`
    )
  }

  return await responseBody
}

export function isApiError(error: ApiError | unknown): error is ApiError {
  return (error as ApiError).name === 'ApiError'
}

export function extractApiErrorMessageForKey(
  error: unknown,
  errorKey: string
): string {
  let errorMessages = ''
  if (isApiError(error)) {
    const { content } = error
    if (errorKey in content) {
      errorMessages = content[errorKey][0]
    }
  }
  return errorMessages
}

export function extractApiGlobalErrorMessage(error: unknown) {
  let message = 'Une erreur est survenue'
  const globalErrorMessages = extractApiErrorMessageForKey(error, 'global')
  if (globalErrorMessages.length > 0) {
    message = globalErrorMessages
  }
  return message
}

export function extractApiFirstErrorMessage(error: unknown) {
  if (isApiError(error)) {
    const { content } = error
    const errorsList: string[][] = Object.values(content)
    if (errorsList.length && errorsList[0].length) {
      return errorsList[0][0]
    }
  }
  return ''
}
