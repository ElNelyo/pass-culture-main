/* eslint
  react/jsx-one-expression-per-line: 0 */
import React from 'react'
import PropTypes from 'prop-types'

import { FormError } from '../../forms'
import { InputField } from '../../forms/inputs'
import FormFooter from './FormFooter'
import withResetForm from './withResetForm'

class RequestEmailForm extends React.PureComponent {
  render() {
    const { canSubmit, isLoading, formErrors } = this.props
    return (
      <div
        id="reset-password-page-request"
        className="is-full-layout flex-rows"
      >
        <main role="main" className="pc-main is-white-text flex-1">
          <div className="pc-scroll-container">
            <div className="is-full-layout flex-rows flex-center padded-2x">
              <h2 className="mb36">
                <span className="is-block is-italic is-medium fs22">
                  Renseignez votre adresse e-mail pour réinitialiser votre mot
                  de passe.
                </span>
                <span className="is-block is-regular fs13 mt18">
                  <span>*</span>
                  &nbsp;Champs obligatoires
                </span>
              </h2>
              <div>
                <InputField
                  required
                  name="email"
                  theme="primary"
                  disabled={isLoading}
                  placeholder="Ex. : nom@domaine.fr"
                  label="Adresse e-mail"
                />
                {formErrors && <FormError customMessage={formErrors} />}
              </div>
            </div>
          </div>
        </main>
        <FormFooter
          cancel={{
            className: 'is-white-text',
            disabled: false,
            label: 'Annuler',
            url: '/connexion',
          }}
          submit={{
            className: 'is-bold is-white-text',
            disabled: !canSubmit,
            label: 'OK',
          }}
        />
      </div>
    )
  }
}

RequestEmailForm.defaultProps = {
  formErrors: false,
}

RequestEmailForm.propTypes = {
  canSubmit: PropTypes.bool.isRequired,
  formErrors: PropTypes.oneOfType([
    PropTypes.array,
    PropTypes.bool,
    PropTypes.string,
  ]),
  isLoading: PropTypes.bool.isRequired,
}

export default withResetForm(
  RequestEmailForm,
  null,
  '/users/reset-password',
  'POST'
)
