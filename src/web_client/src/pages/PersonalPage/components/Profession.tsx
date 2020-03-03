import * as React from "react";
import { Grid, Typography } from "@material-ui/core";

interface IProps {
    name: string;
    rate: number;
}

class Profession extends React.Component<IProps> {
    public render() {
        return (
            <Grid container direction="column" xs={12}>
                <Typography variant="h5">{this.props.rate}</Typography>
                <Typography variant="h5">{this.props.name}</Typography>
            </Grid>
        );
    }
}

export default Profession;
