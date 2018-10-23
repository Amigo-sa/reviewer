import * as React from "react";
import HardSkill from "./HardSkill";
import { Typography, Grid } from "@material-ui/core";
import { HardSkillModel } from "./Model";

interface IProps {
    hardSkills: HardSkillModel[];
}

class HardSkills extends React.Component<IProps> {
    public render() {
        return (
            <Grid container xs={12} direction="column">
                <Typography variant="h5">Профессиональные качества</Typography>
                {this.props.hardSkills.map((value: HardSkillModel, index: number, array: HardSkillModel[]) => {
                    return (<HardSkill key={index} skillName={value.name} value={value.value} />);
                })}
            </Grid>
        );
    }
}

export default HardSkills;
