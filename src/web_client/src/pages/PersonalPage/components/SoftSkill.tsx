import * as React from "react";
import { Grid } from "@material-ui/core";

// TODO:
// props:
// - hanle callback, process click on soft skill. send name or id of skill to parent component
// - id?

interface IProps {
    skillName: string;
    likesCount: number;
}

class SoftSkill extends React.Component<IProps> {
    public render() {
        return (
            <Grid container xs={12}>
                <span>{this.props.skillName}</span>
                <img
                    src="static/img/heart.png"
                    style={{
                        width: "23px",
                        height: "23px",
                    }}
                />
                <span>{this.props.likesCount}</span>
            </Grid>
        );
    }
}

export default SoftSkill;
