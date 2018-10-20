import * as React from "react";
import Typography from "@material-ui/core/Typography";
import { Grid } from "@material-ui/core";

interface IProps {
    notesText: string;
}

class PersonalNotes extends React.Component<IProps> {
    public render() {
        return (
            <Grid container={true} xs={12}
            >
                <Typography variant="h5">Заметки о себе</Typography>
                <Typography variant="body1">{this.props.notesText}</Typography>
            </Grid>
        );
    }
}

export default PersonalNotes;
