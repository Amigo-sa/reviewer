import * as React from 'react';

import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { Theme } from '@material-ui/core/styles/createMuiTheme';
import createStyles from '@material-ui/core/styles/createStyles';
import withStyles, { WithStyles } from '@material-ui/core/styles/withStyles';
import Typography from '@material-ui/core/Typography';
// import { inject, observer } from 'mobx-react';


const styles = (theme: Theme) =>
    createStyles({
        root: {
            textAlign: 'center'
        },
    });

interface IState {
    open: boolean;
}

class Profile extends React.Component<WithStyles<typeof styles>, IState> {
    public state = {
        open: false,
    };
    public componentDidMount() {
        console.log(this.props);
    }
    public handleClose = () => {
        this.setState({
            open: false,
        });
    };

    public handleClick = () => {
        this.setState({
            open: true,
        });
    };

    public render() {
        console.log("render Profile");
        return (
            <div className={this.props.classes.root}>
                <Dialog open={this.state.open} onClose={this.handleClose}>
                    <DialogTitle>Test 2</DialogTitle>
                    <DialogContent>
                        <DialogContentText>333</DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button color="primary" onClick={this.handleClose}>
                            OK
            </Button>
                    </DialogActions>
                </Dialog>
                <Typography variant="display1" gutterBottom={true}>
                    Profile
        </Typography>
                <Typography variant="subheading" gutterBottom={true}>
                    example project
        </Typography>
                <Button variant="raised" color="secondary" onClick={this.handleClick}>
                    Super Secret Password
        </Button>
            </div>
        );
    }
}

export default withStyles(styles)(Profile);