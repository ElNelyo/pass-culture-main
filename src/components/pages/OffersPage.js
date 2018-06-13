import React, { Component } from 'react'
import { NavLink } from 'react-router-dom'
import { compose } from 'redux'
import { withRouter } from 'react-router'
import { connect } from 'react-redux'

import OccasionsList from '../OccasionsList'
import withLogin from '../hocs/withLogin'
import Icon from '../layout/Icon'
import SearchInput from '../layout/SearchInput'
import PageWrapper from '../layout/PageWrapper'
import selectOccasions from '../../selectors/occasions'


class OffersPage extends Component {
  handleRequestData = () => {
    this.props.requestData('GET', 'occasions')
  }

  componentDidMount() {
    this.props.user && this.handleRequestData()
  }

  componentDidUpdate(prevProps) {
    const { user } = this.props
    if (user && user !== prevProps.user) {
      this.handleRequestData()
    }
  }

  render() {
    const {
      location: { search },
      occasions
    } = this.props

    const notification = search === '?success=true' && {
      text: "L' ajout de l'offre a bien été prise en compte",
      type: 'success'
    }

    return (
      <PageWrapper name="offers" loading={!occasions.length} notification={
          search === '?success=true' && {
            text: 'Ca a fonctionné cest genial de la balle de francois miterrand',
            type: 'success'
          }
        }>
        <div className="section">
          <NavLink to={`/offres/evenements/nouveau`} className='button is-primary is-medium is-pulled-right'>
            + Ajouter une offre
          </NavLink>
          <h1 className='pc-title'>
            Vos offres
          </h1>
          <p className="subtitle">
            Voici toutes vos offres apparaissant dans le Pass Culture.
          </p>
        </div>
        <div className='section'>

          <label className="label">Rechercher une offre :</label>
          <div className="field is-grouped">
            <p className="control is-expanded">
              <SearchInput
                collectionNames={["events", "things"]}
                config={{
                  isMergingArray: false,
                  key: 'searchedOccasions'
                }}
                isLoading
              />
            </p>
            <p className="control">
              <button className='button is-primary is-outlined is-medium'>OK</button>
              {' '}
              <button className='button is-secondary is-medium'>&nbsp;<Icon svg='ico-filter' />&nbsp;</button>
            </p>
          </div>
        </div>
        {<div className='section load-wrapper'><OccasionsList /></div>}
      </PageWrapper>
    )
  }
}

export default compose(
  withRouter,
  withLogin({ isRequired: true }),
  connect(
    (state, ownProps) => ({
      occasions: selectOccasions(state, ownProps),
      user: state.user
    })
  )
)(OffersPage)
