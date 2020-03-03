import * as React from "react";
import SoftSkillComponent from "./SoftSkillComponent";
import { Typography, Grid } from "@material-ui/core";
import { SoftSkillModel } from "src/pages/PersonalPage/viewmodel/PersonalInfoVM";

interface IProps {
    softSkills: SoftSkillModel[];
}

class SoftSkillsComponent extends React.Component<IProps> {
    public render() {
        return (
            <Grid container xs={12} direction="column">
                <Typography variant="h5">Личностные качества</Typography>
                {this.props.softSkills.map((value: SoftSkillModel, index: number, array: SoftSkillModel[]) => {
                    return (<SoftSkillComponent key={index} skillName={value.name} likesCount={value.likesCount} />);
                })}

            </Grid>
        );
    }
}

export default SoftSkillsComponent;
