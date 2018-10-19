import * as React from "react";
import HardSkills from "./HardSkills";
import SoftSkills from "./SoftSkills";
import { Grid } from "@material-ui/core";
import PersonalNotes from "./PersonalNotes";
import ProfessionsRating from "./ProfessionsRating";

class PersonalInfo extends React.Component {
    public render() {
        return (
            <Grid
                container={true}
                xs={12}>
                {/* Avatar + full name, info, professions */}
                <Grid
                    container={true}
                    item={true}
                    xs={12}>
                    <Grid item={true} xs={3}>
                        <img src="static/img/icon_big.png" alt="" />
                    </Grid>
                    <Grid
                        container={true}
                        item={true}
                        xs={9}>
                        <Grid
                            container={true}
                            item={true}
                            xs={12}>
                            Иванова Анастасия Ивановна
                            online
                        </Grid>
                        <Grid item={true} xs={12}>
                            <ProfessionsRating />
                        </Grid>
                    </Grid>
                </Grid>

                <Grid
                    container={true}
                    xs={12}>
                    <Grid item={true} xs={6}>
                        <HardSkills />
                    </Grid>
                    <Grid item={true} xs={6}>
                        <SoftSkills />
                    </Grid>
                </Grid>
                <PersonalNotes />
            </Grid>
        );
    }
}

export default PersonalInfo;
