/* eslint
  react/jsx-one-expression-per-line: 0 */
import PropTypes from 'prop-types'
import React from 'react'

import FormFooter from './FormFooter'

const renderRequestSuccessMessage = () => (
  <React.Fragment>
    <p className="is-medium">
      Vous allez recevoir un e-mail avec les instructions de réinitialisation.
    </p>
    <p className="is-medium mt28">
      Si vous n&apos;avez rien reçu d&apos;ici une heure, merci de vérifier
      votre e-mail et de le saisir à nouveau.
    </p>
  </React.Fragment>
)
const renderResetSuccessMessage = () => (
  <React.Fragment>
    <p className="is-medium">
      Votre mode de passe a bien été enregistré, vous pouvez l&apos;utiliser
      pour vous connecter
    </p>
  </React.Fragment>
)

const SuccessView = ({ token }) => {
  const renderSuccessMessage = token
    ? renderResetSuccessMessage
    : renderRequestSuccessMessage
  return (
    <div id="reset-password-page-success" className="is-full-layout flex-rows">
      <main
        role="main"
        className="pc-main padded-2x flex-rows flex-center flex-1"
      >
        <div className="is-italic fs22 is-white-text">
          {renderSuccessMessage()}
        </div>
      </main>
      <FormFooter
        cancel={
          (!token && {
            className: 'is-white-text',
            disabled: false,
            label: 'Recommencer',
            url: '/mot-de-passe-perdu',
          }) ||
          null
        }
        submit={{
          className: 'is-bold is-white-text',
          disabled: false,
          label: 'Connexion',
          url: '/connexion',
        }}
      />
    </div>
  )
}

SuccessView.defaultProps = {
  token: null,
}

SuccessView.propTypes = {
  token: PropTypes.string,
}

export default SuccessView
