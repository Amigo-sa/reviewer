import React, {Component} from 'react'
import Heder from './Heder'
import ContentSearch from './ContentSearch'
import Footer from './Footer'


class App extends Component {
	render(){
		return (
			<div className = "wrapper">
				<Heder />
				<ContentSearch />
				<Footer />
			</div>
			)
		}
	}

export default App
