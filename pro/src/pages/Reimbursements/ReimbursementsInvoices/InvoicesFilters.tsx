import React, { Dispatch, SetStateAction } from 'react'
import { useSWRConfig } from 'swr'

import { FormLayout } from 'components/FormLayout/FormLayout'
import { GET_INVOICES_QUERY_KEY } from 'config/swrQueryKeys'
import { SelectOption } from 'custom_types/form'
import fullRefreshIcon from 'icons/full-refresh.svg'
import { Button } from 'ui-kit/Button/Button'
import { ButtonVariant } from 'ui-kit/Button/types'
import { PeriodSelector } from 'ui-kit/form/PeriodSelector/PeriodSelector'
import { SelectInput } from 'ui-kit/form/Select/SelectInput'
import { FieldLayout } from 'ui-kit/form/shared/FieldLayout/FieldLayout'
import { getToday } from 'utils/date'

import styles from './InvoicesFilters.module.scss'
import { FiltersType } from './types'

interface ReimbursementsSectionHeaderProps {
  areFiltersDefault: boolean
  filters: FiltersType
  disable: boolean
  initialFilters: FiltersType
  selectableOptions: SelectOption[]
  setAreFiltersDefault: Dispatch<SetStateAction<boolean>>
  setFilters: Dispatch<SetStateAction<FiltersType>>
  setHasSearchedOnce: Dispatch<SetStateAction<boolean>>
}

export const InvoicesFilters = ({
  areFiltersDefault,
  filters,
  disable,
  initialFilters,
  selectableOptions,
  setAreFiltersDefault,
  setFilters,
  setHasSearchedOnce,
}: ReimbursementsSectionHeaderProps): JSX.Element => {
  const { mutate } = useSWRConfig()

  const {
    reimbursementPoint: selectedReimbursementPoint,
    periodStart: selectedPeriodStart,
    periodEnd: selectedPeriodEnd,
  } = filters

  async function resetFilters() {
    setAreFiltersDefault(true)
    setFilters(initialFilters)
    await mutate([GET_INVOICES_QUERY_KEY])
  }

  const setReimbursementPointFilter = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const reimbursementPointId = event.target.value
    setFilters((prevFilters: FiltersType) => ({
      ...prevFilters,
      reimbursementPoint: reimbursementPointId,
    }))
    setAreFiltersDefault(false)
  }

  const setStartDateFilter = (startDate: string) => {
    setFilters((prevFilters: FiltersType) => ({
      ...prevFilters,
      periodStart: startDate,
    }))
    setAreFiltersDefault(false)
  }

  const setEndDateFilter = (endDate: string) => {
    setFilters((prevFilters: FiltersType) => ({
      ...prevFilters,
      periodEnd: endDate,
    }))
    setAreFiltersDefault(false)
  }

  return (
    <>
      <div className={styles['header']}>
        <h2 className={styles['header-title']}>Affichage des justificatifs</h2>
        <Button
          className={styles['reset-filters']}
          disabled={areFiltersDefault}
          onClick={resetFilters}
          variant={ButtonVariant.TERNARYPINK}
          icon={fullRefreshIcon}
        >
          Réinitialiser les filtres
        </Button>
      </div>

      <FormLayout.Row inline>
        <FieldLayout
          label="Compte bancaire"
          name="reimbursementPoint"
          isOptional
        >
          <SelectInput
            defaultOption={{
              label: 'Tous les comptes bancaires',
              value: 'all',
            }}
            onChange={setReimbursementPointFilter}
            disabled={disable}
            name="reimbursementPoint"
            options={selectableOptions}
            value={selectedReimbursementPoint}
          />
        </FieldLayout>

        <fieldset>
          <legend>Période</legend>
          <PeriodSelector
            onBeginningDateChange={setStartDateFilter}
            onEndingDateChange={setEndDateFilter}
            isDisabled={disable}
            maxDateEnding={getToday()}
            periodBeginningDate={selectedPeriodStart}
            periodEndingDate={selectedPeriodEnd}
          />
        </fieldset>
      </FormLayout.Row>

      <div className={styles['button-group']}>
        <div className={styles['button-group-separator']} />
        <div className={styles['button-group-button']}>
          <Button
            variant={ButtonVariant.PRIMARY}
            className={styles['button-group-search-button']}
            disabled={!filters.periodStart || !filters.periodEnd || disable}
            onClick={async () => {
              setHasSearchedOnce(true)
              await mutate([GET_INVOICES_QUERY_KEY])
            }}
          >
            Lancer la recherche
          </Button>
        </div>
      </div>
    </>
  )
}
