import * as React from "react";
import { Grid } from "@material-ui/core";
import Profession from "./Profession";

class ProfessionsRating extends React.Component {
    public render() {
        return (
            <Grid
                container={true}
                item={true}
                direction="column">
                Профессия
                    <Grid
                    container={true}
                    item={true}>

                    <Profession name="менеджер" rate={8.5} />
                    <Profession name="экономист" rate={7.2} />
                </Grid>
            </Grid>
        );
    }
}

export default ProfessionsRating;
