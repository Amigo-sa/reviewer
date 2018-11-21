import React from 'react'


function Logo() {
  const log = {
        display: 'flex',
        flex: '1',
    }
    const log_img = {
      width: '65%',
      height: 'auto',
      marginTop: '11px',
    }
  return (
    <div  style = {log}>
      <a>
      <img src="img/logo.png" alt="" style = {log_img} />
      </a>
    </div>
    )
}

export default Logo
