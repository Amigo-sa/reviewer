import * as React from "react";

import Button from "@material-ui/core/Button";
import { Link } from "react-router-dom";

class HeaderMenu extends React.Component{
    public render() {
        console.log("render Menu");
        return (
            <div>
                <Button><Link to="/">Main</Link></Button>
                <Button><Link to="/add-survey">Survey</Link></Button>
                <Button><Link to="/personal">Profile</Link></Button>
                <Button><Link to="/login">Login</Link></Button>
            </div>
        );
    }
}
export default HeaderMenu;
