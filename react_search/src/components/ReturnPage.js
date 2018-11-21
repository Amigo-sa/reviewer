import React from 'react'


function ReturnPage() {
  const ava = {
  	    width: '20%',
  	    borderRadius: '50%'
  }
  const user = {
  	lineHeight: '21px',
    fontSize: '20px',
    color: '#B2B2B2',
    marginLeft: '5%',
  }
  return (
    <div
    style = {{
    	display: 'flex',
    	justifyContent: 'flex-end',
    	alignItems: 'center',
    }}
    >
      <img src="img/user_photo_min.png" alt="" style = {ava} />
      <span style = {user}>Иванова Анастасия Ивановна</span>
    </div>
    )
}

export default ReturnPage
