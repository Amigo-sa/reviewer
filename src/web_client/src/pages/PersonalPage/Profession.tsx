import * as React from "react";
import { Grid } from "@material-ui/core";

interface IProps {
    name: string;
    rate: number;
}

class Profession extends React.Component<IProps> {
    public render() {
        return (
            <Grid
                container={true}
                direction="column"
                xs={12}>
                {this.props.rate}
                {this.props.name}
            </Grid>
        );
    }
}

export default Profession;
