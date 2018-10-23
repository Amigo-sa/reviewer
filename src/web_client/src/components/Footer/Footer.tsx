
import * as React from "react";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import Typography from "@material-ui/core/Typography";

const styles = (theme: Theme) => createStyles({
    root: {
        width: "100%",
        alignContent: "center",
        backgroundColor: "#ccc",
    },
});

class Footer extends React.Component<WithStyles<typeof styles>>{

    public render() {
        const { classes } = this.props;
        const year = new Date().getFullYear();
        return (
            <Grid
                item
                xs={12}
                className={classes.root}>
                <Typography variant="title" color="inherit" noWrap align="center">
                    Skill for life team {year}
                </Typography>
            </Grid>
        );
    }
}

export default withStyles(styles)(Footer);
