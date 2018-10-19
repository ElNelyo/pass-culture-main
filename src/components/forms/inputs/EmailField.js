/* eslint
  react/jsx-one-expression-per-line: 0 */
import React from 'react'
import PropTypes from 'prop-types'
import { Field } from 'react-final-form'

import { FormError } from '../FormError'
import { isEmpty } from '../../../utils/strings'

const DEFAULT_REQUIRED_ERROR = 'Ce champs est requis'

const validateRequiredField = value => {
  if (value && !isEmpty(value)) return undefined
  return DEFAULT_REQUIRED_ERROR
}

export const EmailField = ({
  autoComplete,
  className,
  disabled,
  label,
  name,
  placeholder,
  required,
}) => {
  const validateFunc =
    required && typeof required === 'function'
      ? required
      : (required && validateRequiredField) || undefined
  return (
    <Field
      name={name}
      validate={validateFunc || undefined}
      render={({ input, meta }) => (
        <p className={`${className}`}>
          <label htmlFor={name} className="pc-final-form-text">
            {label && (
              <span className="pc-final-form-label">
                <span>{label}</span>
                {required && <span className="pc-final-form-asterisk">*</span>}
              </span>
            )}
            <span className="pc-final-form-inner">
              <input
                {...input}
                id={name}
                type="email"
                disabled={disabled}
                required={!!required} // cast to boolean
                placeholder={placeholder}
                autoComplete={autoComplete ? 'on' : 'off'}
                className="pc-final-form-input is-block"
              />
            </span>
            <FormError meta={meta} />
          </label>
        </p>
      )}
    />
  )
}

EmailField.defaultProps = {
  autoComplete: false,
  className: '',
  disabled: false,
  label: '',
  placeholder: 'Identifiant (email)',
  required: false,
}

EmailField.propTypes = {
  autoComplete: PropTypes.bool,
  className: PropTypes.string,
  disabled: PropTypes.bool,
  label: PropTypes.string,
  name: PropTypes.string.isRequired,
  placeholder: PropTypes.string,
  required: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
}

export default EmailField
