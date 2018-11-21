import React from 'react'
import Logo from './Logo'
import ReturnPage from './ReturnPage'
import SandwichMenu from './SandwichMenu'

function Heder() {

  return (
    <div
  style = {{
    display: 'flex',
    alignItems: 'center',
    width: '85%',
    margin: 'auto',
    marginBottom: '1%',
  }}
    >
      <Logo />
      <ReturnPage />
      <SandwichMenu />
    </div>
    )
}

export default Heder
