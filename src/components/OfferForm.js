import React from 'react'

import FormInput from './FormInput'
import FormTextarea from './FormTextarea'
import { API_URL } from '../utils/config'

const OfferForm = ({ description,
  name,
  thumbnailUrl,
  work
}) => {
  return (
    <div className='offer-form flex flex-wrap items-center justify-around mb2 p1'>
      <img alt='thumbnail'
        className='offer-form__content__img mb1'
        src={thumbnailUrl || `${API_URL}/thumbs/${work.id}`} />
      <div className='offer-form__content'>
        <FormInput className='input block mb1'
          collectionName='offers'
          defaultValue={name || work.name}
          name='name'
          placeholder="titre de l'offre"
        />
        <FormTextarea className='textarea offer-form__content__textarea'
          collectionName='offers'
          defaultValue={description || work.description}
          name='description'
          placeholder="Vous pouvez écrire une description ici" />
      </div>
    </div>
  )
}

export default OfferForm
