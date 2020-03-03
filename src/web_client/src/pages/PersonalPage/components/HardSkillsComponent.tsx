import * as React from "react";
import HardSkillComponent from "./HardSkillComponent";
import { Typography, Grid } from "@material-ui/core";
import { HardSkillModel } from "src/pages/PersonalPage/viewmodel/PersonalInfoVM";

interface IProps {
    hardSkills: HardSkillModel[];
}

class HardSkillsComponent extends React.Component<IProps> {
    public render() {
        return (
            <Grid container xs={12} direction="column">
                <Typography variant="h5">Профессиональные качества</Typography>
                {this.props.hardSkills.map((value: HardSkillModel, index: number, array: HardSkillModel[]) => {
                    return (<HardSkillComponent key={index} skillName={value.name} value={value.value} />);
                })}
            </Grid>
        );
    }
}

export default HardSkillsComponent;
