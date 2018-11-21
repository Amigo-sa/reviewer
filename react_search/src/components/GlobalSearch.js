import React from 'react'
import Heading from './Heading'
import Organization from './Organization'
import SearchPerson from './SearchPerson'


function GlobalSearch() {
 
  return (
    <div
  style = {{
    backgroundColor: '#008CDF',
    display: 'flex',
    flex: '1 0 auto',
    flexFlow: 'column',
    alignItems: 'center',
  }}
    >
      <Heading />
      <Organization />
      <SearchPerson />
    </div>
    )
}

export default GlobalSearch
