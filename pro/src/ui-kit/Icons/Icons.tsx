/* istanbul ignore file */
import React, { useState } from 'react'

import BaseInput from 'ui-kit/form/shared/BaseInput'
import { SvgIcon } from 'ui-kit/SvgIcon/SvgIcon'
import { Title } from 'ui-kit/typography'

import styles from './Icons.module.scss'

const fuzzyMatch = (pattern: string, str: string) => {
  pattern = '.*' + pattern.toLowerCase().split('').join('.*') + '.*'
  const re = new RegExp(pattern)
  return re.test(str.toLowerCase())
}

interface IconListItem {
  src: string
  viewBox?: string
}

// Cleaned !
// Those icons are put in the order of the design library here:
// https://www.figma.com/file/AEXCkb4KbUyPmB4BRFa88s/PRO---Library?type=design&node-id=8059-111986&t=sLfFXFbaXGFLjdhX-0
const fullIcons: IconListItem[] = [
  { src: 'icons/full-pause.svg' },
  { src: 'icons/full-play.svg' },
  { src: 'icons/full-validate.svg' },
  { src: 'icons/full-clear.svg' },
  { src: 'icons/full-info.svg' },
  { src: 'icons/full-error.svg' },
  { src: 'icons/full-help.svg' },
  { src: 'icons/full-link.svg' }, // TODO 17 uses left inside <ButtonLink> and <Banner> and <InternalBanner>
  { src: 'icons/full-more.svg' }, // TODO still in 2 ButtonLink and 1 Button
  { src: 'icons/full-mail.svg' }, // TODO 2 uses left inside ButtonLink, 1 use left inside SubmitButton
  { src: 'icons/full-edit.svg' }, // TODO 7 uses left in <ButtonLink>s
  { src: 'icons/full-duplicate.svg' }, // TODO still used in 1 Button
  { src: 'icons/full-hide.svg' },
  { src: 'icons/full-like.svg' },
  { src: 'icons/full-back.svg' },
  { src: 'icons/full-download.svg' }, // TODO 3 uses left inside <Button> and <ButtonLink>
  { src: 'icons/full-trash.svg' }, // TODO 2 left inside <Button>
  { src: 'icons/full-next.svg' }, // TODO still used
  { src: 'icons/full-wait.svg' },
  { src: 'icons/full-refresh.svg' }, // TODO still unsed in <Button>s
  { src: 'icons/full-other.svg' },
  { src: 'icons/full-download.svg' }, // TODO 3 uses left inside <Button> and <ButtonLink>
  { src: 'icons/full-parameters.svg' }, // TODO 1 use left inside a <Button>
  { src: 'icons/full-key.svg' }, // TODO 1 use left inside a <ButtonLink>
  { src: 'icons/full-plus.svg' }, // TODO still in 2 ButtonLink and 1 Button
  { src: 'icons/full-sort.svg' },
  { src: 'icons/full-logout.svg' }, // TODO 1 use left inside a <Button>
  { src: 'icons/full-code.svg' },
  { src: 'icons/full-down.svg' }, // TODO 1 use left inside a <Button>
  { src: 'icons/full-up.svg' }, // TODO 1 use left inside a <Button>
  { src: 'icons/full-right.svg' }, // TODO 2 use left inside a <Button>
  { src: 'icons/full-left.svg' }, // TODO 2 use left inside a <Button>
  { src: 'icons/full-arrow-right.svg' },
  { src: 'icons/full-disclosure-close.svg', viewBox: '0 0 16 16' }, // TODO clean viewbox
  { src: 'icons/full-disclosure-open.svg', viewBox: '0 0 16 16' }, // TODO clean viewbox
]

const strokeIcons: IconListItem[] = [
  { src: 'icons/stroke-user.svg' }, // TODO 4 uses left inside <Tabs>
  { src: 'icons/stroke-fraud.svg' },
  { src: 'icons/stroke-error.svg' },
  { src: 'icons/stroke-warning.svg' },
  { src: 'icons/stroke-info.svg' },
  { src: 'icons/stroke-clock.svg' },
  { src: 'icons/stroke-valid.svg' }, // TODO 1 use left inside <Banner>
  { src: 'icons/stroke-wrong.svg' },
  { src: 'icons/stroke-more.svg' }, // TODO 1 use left inside a <Button>
  { src: 'icons/stroke-check.svg' },
  { src: 'icons/stroke-double-check.svg' },
  { src: 'icons/stroke-offers.svg' }, // TODO 1 use left inside a <Tab>
  { src: 'icons/stroke-offer.svg' }, // TODO 1 use left inside a <Tab>
  { src: 'icons/stroke-repayment.svg' },
  { src: 'icons/stroke-euro.svg' }, // TODO 3 use left inside a <TextInput>
  { src: 'icons/stroke-price.svg' },
  { src: 'icons/stroke-events.svg' },
  { src: 'icons/stroke-thing.svg' },
  { src: 'icons/stroke-duo.svg' },
  { src: 'icons/stroke-virtual-event.svg' },
  { src: 'icons/stroke-virtual-thing.svg' },
  { src: 'icons/stroke-template-offer.svg' },
  { src: 'icons/stroke-booked.svg' },
  { src: 'icons/stroke-mail.svg' },
  { src: 'icons/stroke-phone.svg' },
  { src: 'icons/stroke-home.svg' },
  { src: 'icons/stroke-building.svg' },
  { src: 'icons/stroke-desk.svg' },
  { src: 'icons/stroke-calendar.svg' },
  { src: 'icons/stroke-date.svg' },
  { src: 'icons/stroke-hourglass.svg' },
  { src: 'icons/stroke-show.svg' }, // TODO 1 use left inside Button (PasswordInput)
  { src: 'icons/stroke-hide.svg' }, // TODO 1 use left inside Button (PasswordInput)
  { src: 'icons/stroke-like.svg' }, // TODO 1 use left inside Button
  { src: 'icons/stroke-logout.svg' },
  { src: 'icons/stroke-download.svg' }, // TODO 1 use left inside ButtonLink (AddActivationCodeForm)
  { src: 'icons/stroke-search.svg' }, // TODO 1 use left inside SubmitButton (CollectiveOfferSelectionDuplicationScreen)
  { src: 'icons/stroke-trash.svg' },
  { src: 'icons/stroke-draft.svg' },
  { src: 'icons/stroke-code.svg' },
  { src: 'icons/stroke-accessibility-eye.svg' },
  { src: 'icons/stroke-accessibility-ear.svg' },
  { src: 'icons/stroke-accessibility-leg.svg' },
  { src: 'icons/stroke-accessibility-brain.svg' },
  { src: 'icons/stroke-pie.svg' },
  { src: 'icons/stroke-party.svg' },
  { src: 'icons/stroke-new-offer.svg' },
  { src: 'icons/stroke-duplicate-offer.svg' },
  { src: 'icons/stroke-close.svg' },
  { src: 'icons/stroke-left.svg' },
  { src: 'icons/stroke-right.svg' },
  { src: 'icons/stroke-up.svg' },
  { src: 'icons/stroke-pass.svg' },
  { src: 'icons/stroke-library.svg' },
  { src: 'icons/stroke-venue.svg' },
  { src: 'icons/stroke-wip.svg' },
  { src: 'icons/stroke-no-booking.svg' },
]

const shadowIcons: IconListItem[] = [
  { src: 'icons/shadow-tips-help.svg' },
  { src: 'icons/shadow-tips-warning.svg' },
  { src: 'icons/shadow-trophee.svg' },
  { src: 'icons/shadow-calendar.svg' },
]

const notCleandIcons: IconListItem[] = [
  // Not cleaned
  { src: 'icons/checkbox-check.svg', viewBox: '0 0 10 8' },
  { src: 'icons/ico-eye-open-filled-black.svg' },
  { src: 'icons/linear-gradient.svg', viewBox: '0 0 623 1024' }, // TODO replace by a jpg/png
  { src: 'icons/loader.svg', viewBox: '0 0 32 32' },
  { src: 'icons/location.svg', viewBox: '0 0 24 24' },
  { src: 'icons/logo-pass-culture.svg', viewBox: '0 0 114 84' },
  { src: 'icons/logo-pass-culture-header.svg', viewBox: '0 0 119 40' },
  { src: 'icons/ico-no-bookings.svg', viewBox: '0 0 124 124' },
  { src: 'icons/ico-404.svg', viewBox: '0 0 308 194' },
  { src: 'icons/ico-notification-success.svg', viewBox: '0 0 20 20' },
  { src: 'icons/open-dropdown.svg', viewBox: '0 0 20 20' },
  { src: 'icons/ico-radio-off.svg', viewBox: '0 0 16 16' },
  { src: 'icons/ico-radio-on.svg', viewBox: '0 0 16 16' },
  { src: 'icons/ico-star.svg', viewBox: '0 0 38 36' },
  { src: 'icons/ico-status-pending.svg', viewBox: '0 0 16 16' },
  { src: 'icons/ico-unavailable-page-white.svg', viewBox: '0 0 317 198' },
  { src: 'icons/ico-warning.svg', viewBox: '0 0 16 16' },
  { src: 'icons/logo-pass-culture-dark.svg', viewBox: '0 0 71 24' },
  { src: 'icons/ico-institution.svg', viewBox: '0 0 18 18' },
  { src: 'icons/logo-pass-culture-adage.svg', viewBox: '0 0 120 39' },
]

const iconsSections = [
  { title: 'Full icons', icons: fullIcons },
  { title: 'Stroke icons', icons: strokeIcons },
  { title: 'Shadow icons', icons: shadowIcons },
  { title: 'Not cleaned icons', icons: notCleandIcons },
]

export const Icons = () => {
  const [searchInput, setSearchInput] = useState('')
  const [fillColorInput, setFillColorInput] = useState('#000000')
  const [backgroundColorInput, setBackgroundColorInput] = useState('#ffffff')

  const onClick: React.MouseEventHandler<HTMLDivElement> = e => {
    e.persist()
    const target = e.currentTarget as Element

    navigator.clipboard.writeText(target.getAttribute('data-src') ?? '')

    target.classList.add(styles['copy-to-clipboard'])
    const timeoutId = setTimeout(() => {
      target.classList.remove(styles['copy-to-clipboard'])
      clearTimeout(timeoutId)
    }, 600)
  }

  return (
    <div className={styles['icon-stories']}>
      <div className={styles['search-input-container']}>
        <BaseInput
          name="search"
          onChange={event => setSearchInput(event.target.value)}
          placeholder="Rechercher ..."
          value={searchInput}
        />

        <BaseInput
          type="color"
          name="fillColor"
          onChange={event => setFillColorInput(event.target.value)}
          placeholder="#000000, red...."
          value={fillColorInput}
          className={styles['color-input']}
        />

        <BaseInput
          type="color"
          name="backgroundColor"
          onChange={event => setBackgroundColorInput(event.target.value)}
          placeholder="#000000, red...."
          value={backgroundColorInput}
          className={styles['color-input']}
        />
      </div>

      {iconsSections.map(section => {
        const filteredIcons = section.icons.filter(iconListItem =>
          fuzzyMatch(searchInput, iconListItem.src)
        )

        if (filteredIcons.length === 0) {
          return null
        }

        return (
          <div key={section.title}>
            <Title level={2}>{section.title}</Title>

            <div className={styles['icon-list']}>
              {filteredIcons.map(icon => {
                const fileNameParts = icon.src.split('/')
                const iconName = fileNameParts[fileNameParts.length - 1]
                  .split('.')[0]
                  .replace('full-', '')
                  .replace('stroke-', '')
                  .replace('shadow-', '')

                return (
                  <div
                    key={icon.src}
                    className={styles['container']}
                    onClick={onClick}
                    data-src={icon.src}
                  >
                    <div className={styles['copy-to-clipboard-wrapper']}>
                      <span className={styles['copy-to-clipboard-name']}>
                        Copié !
                      </span>
                    </div>

                    <div className={styles['icon-container']}>
                      <SvgIcon
                        src={icon.src}
                        alt={icon.src}
                        viewBox={icon.viewBox}
                        className={styles['icon']}
                        style={{
                          fill: fillColorInput,
                          color: fillColorInput,
                          backgroundColor: backgroundColorInput,
                        }}
                      />
                    </div>

                    <div className={styles['name-container']}>
                      <span className={styles['name']}>{iconName}</span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )
      })}
    </div>
  )
}
