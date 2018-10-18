import * as React from "react";
import { Link } from "react-router-dom";

import "./Menu.css";

class HeaderMenu extends React.Component {
    public render() {
        console.log("render Menu");
        return (
            <div className={"header__menu"}>
                <ul>
                    <li><Link to="/">О проекте</Link></li>
                    <li><Link to="/add-survey">Участники</Link></li>
                    <li><Link to="/login">Регистрация</Link></li>
                </ul>
            </div>
        );
    }
}
export default HeaderMenu;
