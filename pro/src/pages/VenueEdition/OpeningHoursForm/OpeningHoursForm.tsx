import { useFormikContext } from 'formik'

import { mapDayToFrench } from 'pages/VenueEdition/OpeningHoursReadOnly/utils'
import { DayCheckbox } from 'screens/IndividualOffer/StocksEventCreation/DayCheckbox'

import { VenueEditionFormValues, Day } from '../types'

import { HourLine } from './HourLine'
import styles from './OpeningHoursForm.module.scss'

const daysOfWeek: Day[] = [
  'monday',
  'tuesday',
  'wednesday',
  'thursday',
  'friday',
  'saturday',
  'sunday',
]

export function OpeningHoursForm() {
  const {
    values: { days },
    setFieldValue,
  } = useFormikContext<VenueEditionFormValues>()

  return (
    <>
      <fieldset className={styles['inputs-line']}>
        <legend className={styles['legend-days']}>
          Sélectionner vos jours d’ouverture :
        </legend>
        {daysOfWeek?.map((day) => {
          const dayLabel = mapDayToFrench(day)
          return (
            <DayCheckbox
              letter={dayLabel[0]}
              label={dayLabel}
              name="days"
              value={day.toLowerCase()}
              className={styles['day-checkbox']}
              key={day}
              checked={days.includes(day)}
              onClick={async () => {
                await setFieldValue(`${day}.morningStartingHour`, '')
                await setFieldValue(`${day}.morningEndingHour`, '')
                await setFieldValue(`${day}.afternoonStartingHour`, '')
                await setFieldValue(`${day}.afternoonEndingHour`, '')
              }}
            />
          )
        })}
      </fieldset>
      {days.length > 0 && (
        <table>
          <thead>
            <tr>
              <th scope="col" className={styles['column-header']}></th>
              <th scope="col" className={styles['column-header']}>
                Ouvre à
              </th>
              <th scope="col" className={styles['column-header']}>
                Ferme à
              </th>
            </tr>
          </thead>

          <tbody>
            {days
              .sort((a, b) => daysOfWeek.indexOf(a) - daysOfWeek.indexOf(b))
              .map((day) => (
                <HourLine day={day} key={day} />
              ))}
          </tbody>
        </table>
      )}
    </>
  )
}
