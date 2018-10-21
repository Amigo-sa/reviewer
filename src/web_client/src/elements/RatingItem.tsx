import * as React from "react";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import classNames from "classnames";
import { ButtonBase } from "@material-ui/core";

// TODO:
// props:
// - add user info to props
interface IRatingItem extends WithStyles<typeof styles> {
    img: string;
    fullname: string;
    university: string;
    course: number;
    rating: string;
}

const styles = (theme: Theme) => createStyles({
    profile: {
        flexGrow: 1,
        display: "flex",
    },
    fullname: {
        margin: "7px 0 8px 0",
        "& li": {
            alignContent: "left",
            lineHeight: "25px",
            color: "#000",
        },
    },
    rat: {
        textAlign: "left",
    },
    property: {
        lineHeight: "25px",
        fontSize: "24px",
        color: "#767676",
    },
    rating: {
        color: "#000000",
    },
    course: {
        color: "#FF0000",
    },
    image: {
        width: 215,
        height: 215,
    },
    img: {
        margin: "auto",
        display: "block",
        maxWidth: "100%",
        maxHeight: "100%",
    },
});

class RatingItem extends React.Component<IRatingItem>{

    get name() {
        return this.props.fullname.split(" ")[1];
    }

    get surname() {
        return this.props.fullname.split(" ")[0];
    }

    get lastname() {
        return this.props.fullname.split(" ")[2];
    }
    public render() {
        const { img, university, course, rating, classes } = this.props;
        const courseClasses = classNames(classes.property, classes.course);
        const ratingClasses = classNames(classes.property, classes.rating);
        return (
            <div className={classes.profile}>
                <ButtonBase className={classes.image}>
                    <img src={img} className={classes.img} alt="" />
                </ButtonBase>
                <ul className={classes.fullname}>
                    <li>{this.surname}</li>
                    <li>{this.name}</li>
                    <li>{this.lastname}</li>
                </ul>
                <div className={classes.rat}>
                    <span className={classes.property}>{university},</span>
                    <span className={courseClasses}> {course} курс</span>
                    <div className={classes.rating}>
                        <span className={classes.property}>Рейтинг: </span>
                        <span className={ratingClasses}>{rating}</span>
                    </div>
                </div>
            </div>
        );
    }
}

export default withStyles(styles)(RatingItem);
