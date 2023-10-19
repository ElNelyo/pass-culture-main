import { format } from 'date-fns'

import { OfferStatus } from 'apiClient/v1'
import { StocksEvent } from 'components/StocksEventList/StocksEventList'
import { SelectOption } from 'custom_types/form'
import { FORMAT_HH_mm, FORMAT_ISO_DATE_ONLY, isDateValid } from 'utils/date'
import { getLocalDepartementDateTimeFromUtc } from 'utils/timezone'

import { STOCK_EVENT_FORM_DEFAULT_VALUES } from '../constants'
import { StockEventFormValues } from '../types'
import { setFormReadOnlyFields } from '../utils'

interface BuildInitialValuesCommonArgs {
  departementCode?: string | null
  today: Date
  lastProviderName: string | null
  offerStatus: OfferStatus
  priceCategoriesOptions: SelectOption[]
}

interface BuildSingleInitialValuesArgs extends BuildInitialValuesCommonArgs {
  stock: StocksEvent
}

const buildSingleInitialValues = ({
  departementCode,
  stock,
  today,
  lastProviderName,
  offerStatus,
  priceCategoriesOptions,
}: BuildSingleInitialValuesArgs): StockEventFormValues => {
  const hiddenValues = {
    // FIXME: stock.id is never undefined
    stockId: stock.id as number,
    isDeletable: stock.isEventDeletable,
    readOnlyFields: setFormReadOnlyFields({
      beginningDate: stock.beginningDatetime
        ? new Date(stock.beginningDatetime)
        : null,
      today,
      lastProviderName: lastProviderName,
      offerStatus,
    }),
  }
  const defaultPriceCategoryOptionId =
    priceCategoriesOptions.length === 1 ? priceCategoriesOptions[0].value : ''

  return {
    ...hiddenValues,
    remainingQuantity:
      stock.quantity === null || stock.quantity === undefined
        ? ''
        : stock.quantity - stock.bookingsQuantity,
    bookingsQuantity: stock.bookingsQuantity,
    beginningDate: isDateValid(stock.beginningDatetime)
      ? format(
          getLocalDepartementDateTimeFromUtc(
            stock.beginningDatetime,
            departementCode
          ),
          FORMAT_ISO_DATE_ONLY
        )
      : '',
    beginningTime: stock.beginningDatetime
      ? format(
          getLocalDepartementDateTimeFromUtc(
            stock.beginningDatetime,
            departementCode
          ),
          FORMAT_HH_mm
        )
      : '',
    bookingLimitDatetime: stock.bookingLimitDatetime
      ? format(
          getLocalDepartementDateTimeFromUtc(
            stock.bookingLimitDatetime,
            departementCode
          ),
          FORMAT_ISO_DATE_ONLY
        )
      : '',
    priceCategoryId: stock.priceCategoryId
      ? String(stock.priceCategoryId) ?? defaultPriceCategoryOptionId
      : '',
  }
}

interface BuildInitialValuesArgs extends BuildInitialValuesCommonArgs {
  stocks: StocksEvent[]
}

export const buildInitialValues = ({
  departementCode,
  stocks,
  today,
  lastProviderName,
  offerStatus,
  priceCategoriesOptions,
}: BuildInitialValuesArgs): { stocks: StockEventFormValues[] } => {
  if (stocks.length === 0) {
    return {
      stocks: [
        {
          ...STOCK_EVENT_FORM_DEFAULT_VALUES,
          priceCategoryId:
            priceCategoriesOptions.length === 1
              ? String(priceCategoriesOptions[0].value)
              : '',
        },
      ],
    }
  }

  return {
    stocks: stocks
      .map((stock) =>
        buildSingleInitialValues({
          departementCode,
          stock,
          today,
          lastProviderName,
          offerStatus,
          priceCategoriesOptions,
        })
      )
      .sort(
        (firstStock, secondStock) =>
          Number(new Date(firstStock.beginningDate)) -
          Number(new Date(secondStock.beginningDate))
      ),
  }
}
