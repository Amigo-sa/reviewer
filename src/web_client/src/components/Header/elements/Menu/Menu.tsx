import * as React from "react";
import { Link } from "react-router-dom";
import { createStyles, Theme, withStyles, WithStyles } from "@material-ui/core";

const styles = (theme: Theme) =>
    createStyles({
        menu: {
            display: "flex",
            flex: "2 1 auto",
            "& ul": {
                listStyleType: "none",
                display: "flex",
                fles: "1 1 auto",
                "& li": {
                    display: "flex",
                    flex: "1 1 auto",
                    "& a": {
                        fontSize: "20px",
                        color: "#02588A",
                        textDecoration: "none",
                    },
                },
            },
        },
    });

class HeaderMenu extends React.Component<WithStyles<typeof styles>> {
    public render() {
        const { classes } = this.props;
        return (
            <div className={classes.menu}>
                <ul>
                    <li><Link to="/">О проекте</Link></li>
                    <li><Link to="/add-survey">Участники</Link></li>
                    <li><Link to="/login">Регистрация</Link></li>
                </ul>
            </div>
        );
    }
}
export default withStyles(styles)(HeaderMenu);
