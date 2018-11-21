import React from 'react'


function Footer() {
 
  const footer = {
  	display: 'block',
    marginTop: '15px',
  }
  return (
    <div
    style = {{
    	width: '100%',
      height: '50px',
      float: 'left',
      textAlign: 'center',
      background: '#FFFFFF',
      lineHeight: '19px',
      fontSize: '18px',
      color: '#C9C9C9',
    }}
    >
      <span style = {footer}>Skill for life team, 2018 г.</span>
    </div>
    )
}

export default Footer
