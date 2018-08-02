import React from 'react'
import ReactMarkdown from 'react-markdown'

import { version } from '../../../package.json'

import Main from '../layout/Main'
import { ROOT_PATH } from '../../utils/config'

class TermsPage extends React.PureComponent {
  constructor(props) {
    super(props)
    this.state = { mdText: '' }
  }

  async componentDidMount() {
    const result = await fetch(`${ROOT_PATH}/MentionsLegalesPass.md`)
    const mdText = await result.text()
    this.setState({ mdText })
  }

  render() {
    const { mdText } = this.state
    return (
      <Main name="terms" footer={{ borderTop: true, colored: true }} backButton>
        <header>
          {'Mentions légales'}
        </header>
        <div className="content">
          <ReactMarkdown source={mdText} />
          <p className="version">
            <br />
            <br />
            {`Pass Culture version v${version}`}
          </p>
        </div>
      </Main>
    )
  }
}

export default TermsPage
