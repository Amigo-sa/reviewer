import * as React from "react";
import HardSkills from "./HardSkills";
import SoftSkills from "./SoftSkills";
import { Grid, Typography, Divider } from "@material-ui/core";
import PersonalNotes from "./PersonalNotes";
import ProfessionsRating from "./ProfessionsRating";
import { PersonalInfoModel } from "./Model";

const personalInfoModel = new PersonalInfoModel();

class PersonalInfo extends React.Component {
    public render() {
        return (
            <Grid container={true} xs={12}>
                {/* Avatar + full name, info, professions */}
                <Grid container={true} item={true} xs={12}>
                    <Grid item={true} xs={3}>
                        <img src="static/img/icon_big.png" alt="" />
                    </Grid>
                    <Grid container={true} item={true} xs={9}>
                        <Grid container={true} item={true} xs={12}>
                            <Typography variant="h4">Иванова Анастасия Ивановна</Typography>
                            online
                        </Grid>
                        <Grid item={true} container={true} direction="column">
                            <span>Статус: Сотрудник</span>
                            <span>Организация: ИТМО (Полное название организации)</span>
                            <span>Направление: Экономика</span>
                        </Grid>
                        <Divider />
                        <Grid item={true} xs={12}>
                            <ProfessionsRating />
                        </Grid>
                    </Grid>
                </Grid>
                <Grid container={true} xs={12}>
                    <Grid item={true} xs={6}>
                        <HardSkills hardSkills={personalInfoModel.hardSkills} />
                    </Grid>
                    <Grid item={true} xs={6}>
                        <SoftSkills softSkills={personalInfoModel.softSkills} />
                    </Grid>
                </Grid>
                <PersonalNotes notesText={personalInfoModel.personalNotes} />
            </Grid>
        );
    }
}

export default PersonalInfo;
