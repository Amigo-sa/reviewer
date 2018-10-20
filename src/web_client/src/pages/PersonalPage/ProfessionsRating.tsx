import * as React from "react";
import { Grid, Typography } from "@material-ui/core";
import Profession from "./Profession";

class ProfessionsRating extends React.Component {
    public render() {
        return (
            <Grid container={true} item={true} xs={12}>
                <Typography variant="h5">Профессия</Typography>
                <Grid container={true} item={true}>
                    <Profession name="менеджер" rate={8.5} />
                    <Profession name="экономист" rate={7.2} />
                </Grid>
            </Grid>
        );
    }
}

export default ProfessionsRating;
