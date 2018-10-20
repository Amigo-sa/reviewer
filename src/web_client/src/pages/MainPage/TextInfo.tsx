import * as React from "react";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";

// TODO:
// props:
// - handle callback to login and registration
interface ITextInfo extends WithStyles<typeof styles> {
    title: string;
}

const styles = (theme: Theme) => createStyles({
    registrations: {
        backgroundColor: "rgba(0, 0, 0, 0.16)",
        color: "#FFF",
        padding: "28px 37px 0 32px",
        alignSelf: "right",
        "& h1": {
            fontWeight: "bold",
            fontSize: "48px",
            marginBottom: "30px",
        },
        "& p": {
            lineHeight: "25px",
            fontSize: "24px",
        },
        "& button": {
            width: "199px",
            height: "56px",
            cursor: "pointer",
            fontWeight: "bold",
            lineHeight: "25px",
            fontSize: "24px",
            color: "#ffffff",
            marginTop: "50px",
            border: "0",
            "&:focus": {
                outline: "none",
            },
        },
    },
    go_into: {
        backgroundColor: "#008CDF",
        marginLeft: 110,
    },
    registr: {
        backgroundColor: "#DFA300",
        marginLeft: 36,
    },
});

class TextInfo extends React.Component<ITextInfo>{
    public render() {
        const { title, children, classes } = this.props;
        return (
            <div className={classes.registrations}>
                <h1>{title}</h1>
                {children}
                <button className={classes.go_into}>Войти</button>
                <button className={classes.registr}>Регистрация</button>
            </div>
        );
    }
}

export default withStyles(styles)(TextInfo);
