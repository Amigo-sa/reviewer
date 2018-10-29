import * as React from "react";

import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import createStyles from "@material-ui/core/styles/createStyles";
import withStyles, { WithStyles } from "@material-ui/core/styles/withStyles";
import Typography from "@material-ui/core/Typography";

const styles = (theme: Theme) =>
    createStyles({
        root: {
            textAlign: "center",
        },
    });

interface IState {
    open: boolean;
}

class Main extends React.Component<WithStyles<typeof styles>, IState> {
    public state = {
        open: false,
    };

    public handleClose = () => {
        this.setState({
            open: false,
        });
    }

    public handleClick = () => {
        this.setState({
            open: true,
        });
    }

    public render() {
        console.log("render Main");
        return (
            <div className={this.props.classes.root}>
                <Dialog open={this.state.open} onClose={this.handleClose}>
                    <DialogTitle>Super Secret Password</DialogTitle>
                    <DialogContent>
                        <DialogContentText>1-2-3-4-5</DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button color="primary" onClick={this.handleClose}>
                            OK
                </Button>
                    </DialogActions>
                </Dialog>
                <Typography variant="h4" gutterBottom={true}>
                    Main material UI
        </Typography>
                <Typography variant="subtitle1" gutterBottom={true}>
                    example project
        </Typography>
                <Button variant="raised" color="secondary" onClick={this.handleClick}>
                    Super Secret Password
        </Button>
            </div>
        );
    }
}
export default withStyles(styles)(Main);
