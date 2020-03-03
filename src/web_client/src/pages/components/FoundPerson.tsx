import * as React from "react";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import { ButtonBase, Grid, Typography } from "@material-ui/core";
import { personUrlById, DUMMY_AVATAR_URL } from "src/constants";
import { Link } from "react-router-dom";
import PersonsApi from "src/server-api/persons/PersonsApi";

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

// TODO:
// props:
// - add person info to props
// - add mode identificator: for show in rating list, for show as found person in search page
interface IProps extends WithStyles<typeof styles> {
    id: string;
    isPersonPhotoExist: boolean;
    firstName: string;
    surname: string;
    middleName?: string;
    organizationName?: string;
    departamentName?: string;
    specialization?: string;
}

class FoundPerson extends React.Component<IProps>{

    public render() {
        const {
            id,
            firstName,
            surname,
            middleName,
            organizationName,
            specialization,
            departamentName,
            classes,
        } = this.props;

        // Determine url of person photo
        let photoUrl: string = DUMMY_AVATAR_URL;
        if (this.props.isPersonPhotoExist) {
            photoUrl = PersonsApi.personPhotoUrlById(id);
        }

        const linkId = id || "";
        return (
            <Grid container item justify="center" className={classes.profile}>
                <Link to={personUrlById(linkId)} className={classes.link}>
                    <ButtonBase className={classes.image}>
                        <img src={photoUrl}
                            className={classes.img}
                            alt={this._firstInitial}
                            title={this._fio}
                        />
                    </ButtonBase>
                    <ul className={classes.fullname}>
                        <li>{surname}</li>
                        <li>{firstName}</li>
                        {middleName &&
                            <li>{middleName}</li>
                        }
                    </ul>
                    <div className={classes.rat}>
                        <Typography variant="caption">
                            {organizationName}
                        </Typography>
                        <Typography variant="caption">
                            {departamentName}
                        </Typography>
                        <Typography variant="caption">
                            {specialization}
                        </Typography>
                    </div>
                </Link>
            </Grid>
        );
    }

    // Private properties

    private get _firstInitial() {
        return this.props.firstName[0];
    }

    private get _fio() {
        return this.props.surname + " "
            + this.props.firstName + " "
            + this.props.middleName;
    }
}

export default withStyles(styles)(FoundPerson);
