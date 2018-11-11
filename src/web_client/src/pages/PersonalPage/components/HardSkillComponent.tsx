import * as React from "react";
import { Grid } from "@material-ui/core";

// TODO:
// props:
// - hanle callback, process click on hard skill. send name or id of skill to parent component
// - id?

interface IProps {
    skillName: string;
    value: number;
}

class HardSkillComponent extends React.Component<IProps> {
    public render() {
        return (
            <Grid container xs={12}>
                <Grid item xs={6}>
                    <span>{this.props.skillName}</span>
                </Grid>
                <Grid item xs={6}>
                    <progress value={this.props.value} max="100" />
                </Grid>
            </Grid>
        );
    }
}

export default HardSkillComponent;
