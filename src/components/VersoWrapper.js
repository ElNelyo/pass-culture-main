import get from 'lodash.get'
import React from 'react'
import { connect } from 'react-redux'

import ControlBar from './ControlBar'

import { ROOT_PATH } from '../utils/config';
import selectHeaderColor from '../selectors/headerColor'
import selectIsTuto from '../selectors/isTuto'
import selectSource from '../selectors/source'
import selectVenue from '../selectors/venue'

const Verso = ({
  children,
  className,
  hasControlBar,
  headerColor,
  isTuto,
  source,
  venue,
}) => {
  const contentStyle = {}
  if (isTuto) {
    contentStyle.backgroundColor = headerColor
  } else {
    contentStyle.backgroundImage = `url('${ROOT_PATH}/mosaic-k@2x.png')`
  }
  const author = get(source, 'extraData.author')
  return (
    <div className={`verso-wrapper ${className || ''}`}>
      <div className='verso-header' style={{ backgroundColor: headerColor }}>
        <h2> { source && source.name }{ author && (", de " + author) } </h2>
        <h6> { venue && venue.name } </h6>
      </div>
      {hasControlBar && <ControlBar />}
      <div className='content' style={{...contentStyle}} >
        {children}
      </div>
    </div>
  )
}

export default connect(
  state => ({
    headerColor: selectHeaderColor(state),
    isFlipped: state.verso.isFlipped,
    isTuto: selectIsTuto(state),
    source: selectSource(state),
    venue: selectVenue(state)
  }))(Verso)
