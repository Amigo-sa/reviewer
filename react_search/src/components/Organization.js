import React from 'react'


function Organization() {
    const organization_text = {
        lineHeight: '25px',
        fontSize: '24px',
        color: '#FFFFFF',
    }
    const organization_button = {
        backgroundColor: '#FFB801',
        width: '30%',
        height: '15%',
        border: 'none',
        lineHeight: '25px',
        fontSize: '24px',
        color: '#FFFFFF',
        padding: '1%',
        marginTop: '2%',
    }
    const organization = {
      width: '40%',
      padding: '1%',
      margin: '1%',
    }

  return (
    <form
  style = {{
    textAlign: 'center',
    width: '90%',
    marginTop: '2%',
  }}
    >
      <ul>
        <li>
          <label for="organization" style = {organization_text}>Организация</label>
        <select id="organization" placeholder="Полное название организации" style = {organization} >
          <option value="">Московский государственный университет технологий и управления им. К.Г. Разумовского</option>
          <option value=""> Московский институт телевидения и радиовещания Останкино (МИТРО)</option>
          <option value="">Московский региональный социально-экономический институт</option>
          <option value=""> Московский государственный университет имени М.В. Ломоносова</option>
        </select>
      </li>
        <li>
          <button type="submit" style = {organization_button}>Показать структуру</button>
        </li>
      </ul>
    </form>
    )
}

export default Organization
