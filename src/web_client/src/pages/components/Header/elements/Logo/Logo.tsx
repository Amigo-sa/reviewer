import * as React from "react";
import { Link } from "react-router-dom";
import { Theme, createStyles, withStyles, WithStyles } from "@material-ui/core";

const styles = (theme: Theme) =>
    createStyles({
        link: {
            display: "flex",
            flex: "1 1 auto",
            textDecoration: "none",
        },
        img: {
            width: "96px",
            height: "96px",
        },
        titleSection: {
            height: "64px",
        },
        title: {
            display: "block",
            fontSize: "30px",
            color: "#000000",
        },
        subtitle: {
            display: "block",
            fontSize: "20px",
            color: "#02588A",
        },
    });

interface IProps extends WithStyles<typeof styles> {
    title?: string;
}

class Logo extends React.Component<IProps> {
    public render() {
        const { title } = this.props;
        const { classes } = this.props;
        return (
            <Link to="/" className={classes.link} title={title}>
                <img src="/static/img/logo.png" alt="logo" className={classes.img} />
                <div className={classes.titleSection}>
                    <span className={classes.title}>Skill for life</span>
                    <span className={classes.subtitle}>reviewer</span>
                </div>
            </Link>
        );
    }
}
export default withStyles(styles)(Logo);
