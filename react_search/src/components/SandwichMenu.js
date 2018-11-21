import React from 'react'


function SandwichMenu() {
	const menuItem = {
    	    width: '40%',
    	    padding: '4%',
    	    marginTop: '8%',
    	    marginLeft: '20%',
    	    cursor: 'pointer',
    	    backgroundColor: '#E5E5E5',
    }
  return (
      <nav
      style = {{
      	display: 'flex',
      	flexFlow: 'column',
      	width: '15%',
      }}
      >
        <span style = {menuItem} ></span>
        <span style = {menuItem} ></span>
        <span style = {menuItem} ></span>
        
       </nav>
    )
}

export default SandwichMenu
