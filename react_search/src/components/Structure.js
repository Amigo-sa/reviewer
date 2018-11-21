import React from 'react'


function Structure() {
  const students = {
       marginLeft: '3%',
    }
    const faculties = {
      marginLeft: '4%',
    }
    const departments = {
      marginLeft: '5%',
    }
    const group_number = {
      marginLeft: '6%',
    }
    const students_list ={
      marginLeft: '7%',
      color: '#0FA5FE',
    }
  return (
    <div
    style = {{
      lineHeight: '30px',
      fontSize: '28px',
      color: '#5A5A5A',
    }}

    >
     <ul style = {students} className = "structure">
    <li><img src="img/polygon_open.png" alt="" />Студенты</li>
    <li>
      <ul style = {faculties}>
        <li><img src="img/polygon_open.png" alt="" />Факультет математики</li>
        <li>
          <ul style ={departments}>
            <li><img src="img/polygon_open.png" alt="" />Кафедра математики</li>
            <li>
              <ul style = {group_number}>
                <li><img src="img/polygon_open.png" alt="" />Группа 22-03-11</li>
                <li>
                  <ul style = {students_list}>
                    <li>Иванова Ирина Андреевна</li>
                    <li>Иванова Ирина Андреевна</li>
                    <li>Иванова Ирина Андреевна</li>
                  </ul>
                </li>
                <li><img src="img/polygon_close.png" alt="" />Группа 22-03-11</li>
              </ul>
            </li>
            <li><img src="img/polygon_close.png" alt="" />Факультет русского языка</li>
          </ul>
        </li>
        <li><img src="img/polygon_close.png" alt="" />Дополнительная группа</li>
      </ul>
    </li>
  </ul>
    </div>
    )
}

export default Structure
