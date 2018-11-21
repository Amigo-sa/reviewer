import React from 'react'


function SearchPerson() {
  const search_person = {
        display: 'flex',
        border: '1px solid #FFFFFF',
        alignItems: 'center',
        width: '25%',
        padding: '1%',
        lineHeight: '25px',
        fontSize: '24px',
        color: '#FFFFFF',
        }

  return (
    <div
  style = {{
    display: 'flex',
    justifyContent: 'flex-end',
    marginBottom: '2%',
    width: '90%',
    marginTop: '2%',
  }}
    >
      <div style ={search_person}>
        <img src="img/persones.png" alt="persones_icon" />
        <span>Поиск по персоналиям</span>
      </div>
    </div>
    )
}

export default SearchPerson
