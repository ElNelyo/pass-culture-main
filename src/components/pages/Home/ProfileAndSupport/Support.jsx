import React from 'react'

import Icon from 'components/layout/Icon'

const Support = () => {
  return (
    <div className="h-support h-card h-card-secondary-hover">
      <div className="h-card-inner">
        <h3 className="h-card-title">
          {'Aide et support'}
        </h3>

        <div className="h-card-content">
          <ul className="hs-link-list">
            <li>
              <a
                className="hs-link"
                href="mailto:support@passculture.app"
                rel="noopener noreferrer"
                target="_blank"
              >
                <div className="ico-container">
                  <Icon
                    className="ico-mail"
                    svg="ico-mail"
                  />
                </div>
                {'Contacter le support'}
              </a>
            </li>

            <li>
              <a
                className="hs-link"
                href="https://pass.culture.fr/cgu-professionnels/"
                rel="noopener noreferrer"
                target="_blank"
              >
                <div className="ico-container">
                  <Icon svg="ico-external-site" />
                </div>
                {'Conditions Générales d’Utilisation'}
              </a>
            </li>

            <li>
              <a
                className="hs-link"
                href="https://aide.passculture.app/fr/category/acteurs-culturels-1t20dhs/"
                rel="noopener noreferrer"
                target="_blank"
              >
                <div className="ico-container">
                  <Icon svg="ico-external-site" />
                </div>
                {'Foire Aux Questions'}
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Support
