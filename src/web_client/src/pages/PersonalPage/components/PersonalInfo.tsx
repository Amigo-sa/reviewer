import * as React from "react";
import HardSkills from "./HardSkillsComponent";
import SoftSkills from "./SoftSkillsComponent";
import { Grid, Typography, Divider } from "@material-ui/core";
import PersonalNotes from "./PersonalNotes";
import ProfessionsRating from "./ProfessionsRating";
// import { urlReviewNew } from "../ReviewPage";
// import { Link } from "react-router-dom";
import PersonalInfoVM from "src/pages/PersonalPage/viewmodel/PersonalInfoVM";
import { observer } from "mobx-react";

interface IProps {
    viewModel: PersonalInfoVM;
    isCurrentPerson: boolean;
}

@observer
class PersonalInfo extends React.Component<IProps> {
    public render() {

        const { viewModel } = this.props;

        return (
            <Grid container xs={12}>
                {/* Avatar + full name, info, professions */}
                <Grid container item xs={12}>
                    <Grid item xs={3}>
                        <img
                            src={viewModel.photoUrl}
                            alt=""
                            width="100%"
                            height="100%" />
                    </Grid>
                    <Grid container item xs={9}>
                        <Grid container item xs={12}>
                            <Typography variant="h4">{viewModel.fullName}</Typography>
                        </Grid>
                        <Grid item container direction="column">
                            <span>Статус: {viewModel.status}</span>
                            <span>Организация: {viewModel.organizationName}</span>
                        </Grid>
                        {/* <Grid item container direction="column">
                            {this._renderReviewLink(this.props.isCurrentPerson)}
                        </Grid> */}
                        <Divider />
                        <Grid item xs={12}>
                            <ProfessionsRating
                                isCurrentPerson={this.props.isCurrentPerson}
                                personId={viewModel.personId}
                                professionList={viewModel.professionLists} />
                        </Grid>
                    </Grid>
                </Grid>
                <Grid container xs={12}>
                    <Grid item xs={6}>
                        <HardSkills hardSkills={viewModel.hardSkills} />
                    </Grid>
                    <Grid item xs={6}>
                        <SoftSkills softSkills={viewModel.softSkills} />
                    </Grid>
                </Grid>
                <PersonalNotes notesText={viewModel.personalNotes} />
            </Grid>
        );
    }

    // private _renderReviewLink(isCurrentUser: boolean) {
    //     const specializations = this.props.viewModel.specializationList;

    //     if (specializations.list && specializations.list.length > 1) {
    //         // const specialization = specializations.list[0];
    //         return specializations.list.map((specialization) => (
    //             <Grid item>
    //                 <b>{specialization.specialization_type}({specialization.department_name})</b>
    //                 {!isCurrentUser &&
    //                     <Link to={urlReviewNew(this.props.viewModel.personId,
    // specialization.id)}>Оставить отзыв</Link>}
    //             </Grid>
    //         ));
    //     }
    //     return (<></>); // (<Link to={urlReviewNew(person.id)}>Оставить отзыв</Link>);
    // }
}

export default PersonalInfo;
