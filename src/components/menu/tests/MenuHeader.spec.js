import React from 'react'
import { shallow } from 'enzyme'

import MenuHeader from '../MenuHeader'

describe('src | components | menu | MenuHeader', () => {
  describe('snapshot', () => {
    it('should match snapshot', () => {
      // given
      const props = {
        user: true,
      }

      // when
      const wrapper = shallow(<MenuHeader {...props} />)

      // then
      expect(wrapper).toBeDefined()
      expect(wrapper).toMatchSnapshot()
    })
  })
})
