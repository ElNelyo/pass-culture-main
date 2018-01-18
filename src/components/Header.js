import React from 'react'
import { connect } from 'react-redux'

import Hamburger from './Hamburger'

const Header = ({ user }) => {
  return (
    <div className='header flex items-center justify-start p2'>
      <Hamburger className='hamburger mr1'/>
      <div className='header__logo'>Pass Culture</div>
      <div className='flex-auto' />
      {
        user && user.seller && (
          <div className='header__seller flex items-center'>
            <span className='mx1'>
              {user.seller.name}
            </span>
            <img className='header__seller__image mr2'
              alt='seller'
              src={user.seller.thumbnailUrl} />
          </div>
        )
      }
      {
        user && (
          <img className='header__avatar'
            alt='avatar'
            src={user.thumbnailUrl} />
        ) || <img className='header__avatar' alt='' src='/dragon.png' />
      }
      {
        user && user.type === 'client' || !user && (
          <div className='header__account-balance'>
            100€
          </div>
        )
      }
    </div>
  )
}

export default connect(
  ({ user }) => ({ user })
)(Header)
