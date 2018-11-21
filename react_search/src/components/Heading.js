import React from 'react'

function Heading() {
    const  heading_img = {
          width: '4%',
    }
    const  heading_h = {
          lineHeight: '38px',
          fontSize: '46px',
          color: '#FFFFFF',
    }

  return (
    <div
  style = {{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '90%',
    marginTop: '2%',
  }}
    >
      <img src="img/search_attribute.png" alt="" style = {heading_img} />
      <h1 style = {heading_h} >Поиск по структуре</h1>
    </div>
    )
}

export default Heading
