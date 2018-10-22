import * as React from "react";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import classNames from "classnames";
import { ButtonBase, Grid, Typography } from "@material-ui/core";
import { SERVER_HOST } from "src/constants";
import { Link } from "react-router-dom";
import { urlPersonById } from "src/server-api/persons/Person";

// TODO:
// props:
// - add user info to props
// - add mode identificator: for show in rating list, for show as found person in search page
interface IProps extends WithStyles<typeof styles> {
    id?: string;
    first_name: string;
    surname: string;
    middle_name?: string;
    university: string;
    specialization: string;
    course: number;
    rating: string;
}

const styles = (theme: Theme) => createStyles({
    profile: {
        flex: "1 1 20%",
        marginBottom: 70,
    },
    link: {
        textDecoration: "none",
    },
    fullname: {
        margin: "7px 0 8px 0",
        padding: 0,
        "& li": {
            alignContent: "left",
            lineHeight: "25px",
            color: "#000",
            listStyle: "none",
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
        width: 200,
        height: 200,
        borderRadius: "100%",
        border: "1px solid #ccc",
        backgroundColor: "#FFF",
        overflow: "hidden",
    },
    img: {
        margin: "auto",
        display: "block",
        maxWidth: "100%",
        maxHeight: "100%",
    },
});

class FoundPerson extends React.Component<IProps>{

    get firstInitial() {
        return this.props.first_name[0];
    }

    get fio() {
        const { first_name, surname, middle_name } = this.props;
        return surname + " " + first_name + " " + middle_name;
    }

    public render() {
        const {
            id,
            first_name,
            surname,
            middle_name,
            university,
            specialization,
            course,
            rating,
            classes,
        } = this.props;
        // const courseClasses = classNames(classes.property, classes.course);
        const ratingClasses = classNames(classes.property, classes.rating);
        const linkId = id || "";
        return (
            <Grid item={true} justify="center" className={classes.profile}>
                <Link to={urlPersonById(linkId)} className={classes.link}>
                    <ButtonBase className={classes.image}>
                        <img src={SERVER_HOST + "/persons/" + id + "/photo"}
                            className={classes.img}
                            alt={this.firstInitial}
                            title={this.fio}
                        />
                    </ButtonBase>
                    <ul className={classes.fullname}>
                        <li>{surname}</li>
                        <li>{first_name}</li>
                        {middle_name &&
                            <li>{middle_name}</li>
                        }
                    </ul>
                    <div className={classes.rat}>
                        <Typography variant="caption">
                            {university},{specialization}
                        </Typography>
                        <Typography variant="caption">
                            {specialization},{course} курс
                        </Typography>
                        {rating &&
                            <div className={classes.rating}>
                                <span className={classes.property}>Рейтинг: </span>
                                <span className={ratingClasses}>{rating}</span>
                            </div>
                        }
                    </div>
                </Link>
            </Grid>
        );
    }
}

export default withStyles(styles)(FoundPerson);
