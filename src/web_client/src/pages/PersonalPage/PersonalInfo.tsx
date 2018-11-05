import * as React from "react";
import HardSkills from "./HardSkills";
import SoftSkills from "./SoftSkills";
import { Grid, Typography, Divider } from "@material-ui/core";
import PersonalNotes from "./PersonalNotes";
import ProfessionsRating from "./ProfessionsRating";
import { PersonalInfoModel } from "./Model";
import Person from "src/server-api/persons/Person";
import { PersonSpecializationList } from "src/server-api/persons/PersonSpecialization";
import { urlReviewNew } from "../ReviewPage";
import { Link } from "react-router-dom";

const personalInfoModel = new PersonalInfoModel();
interface IProps {
    person: Person;
    specializations: PersonSpecializationList;
}
class PersonalInfo extends React.Component<IProps> {
    public render() {
        return (
            <Grid container xs={12}>
                {/* Avatar + full name, info, professions */}
                <Grid container item xs={12}>
                    <Grid item xs={3}>
                        <img src="static/img/icon_big.png" alt="" />
                    </Grid>
                    <Grid container item xs={9}>
                        <Grid container item xs={12}>
                            <Typography variant="h4">Иванова Анастасия Ивановна</Typography>
                            online
                        </Grid>
                        <Grid item container direction="column">
                            <span>Статус: Сотрудник</span>
                            <span>Организация: ИТМО (Полное название организации)</span>
                            <span>Направление: Экономика</span>
                        </Grid>
                        <Grid item container direction="column">
                            {this._renderReviewLink()}
                        </Grid>
                        <Divider />
                        <Grid item xs={12}>
                            <ProfessionsRating />
                        </Grid>
                    </Grid>
                </Grid>
                <Grid container xs={12}>
                    <Grid item xs={6}>
                        <HardSkills hardSkills={personalInfoModel.hardSkills} />
                    </Grid>
                    <Grid item xs={6}>
                        <SoftSkills softSkills={personalInfoModel.softSkills} />
                    </Grid>
                </Grid>
                <PersonalNotes notesText={personalInfoModel.personalNotes} />
            </Grid>
        );
    }

    private _renderReviewLink() {
        const { person, specializations } = this.props;

        if (specializations.list.length > 1) {
            // const specialization = specializations.list[0];
            return specializations.list.map((specialization) => (
                <Grid item>
                    <b>{specialization.specialization_type}({specialization.department_name})</b>
                    <Link to={urlReviewNew(person.id, specialization.id)}>Оставить отзыв</Link>
                </Grid>
            ));
        }
        return (<Link to={urlReviewNew(person.id)}>Оставить отзыв</Link>);
    }
}

export default PersonalInfo;
