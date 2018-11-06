import * as React from "react";
import SoftSkill from "./SoftSkill";
import { Typography, Grid } from "@material-ui/core";
import { SoftSkillModel } from "./PersonalInfoVM";

interface IProps {
    softSkills: SoftSkillModel[];
}

class SoftSkills extends React.Component<IProps> {
    public render() {
        return (
            <Grid container xs={12} direction="column">
                <Typography variant="h5">Личностные качества</Typography>
                {this.props.softSkills.map((value: SoftSkillModel, index: number, array: SoftSkillModel[]) => {
                    return (<SoftSkill key={index} skillName={value.name} likesCount={value.likesCount} />);
                })}

            </Grid>
        );
    }
}

export default SoftSkills;
