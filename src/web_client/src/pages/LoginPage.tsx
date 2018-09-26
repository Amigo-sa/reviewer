import * as React from "react";
import { Button, TextField } from "@material-ui/core";
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from "@material-ui/core";
import { AuthStore } from "../stores/AuthStore";
import { inject, observer } from "mobx-react";
import { observable, action } from "mobx";
import { Redirect } from "react-router-dom";

interface IAuthProps {
    auth: AuthStore;
}

interface IState {
    open: boolean;
    login: string;
    password: string;
}

@inject("auth")
@observer
class LoginPage extends React.Component<IAuthProps, IState> {
    @observable
    public user: object = {
        login: "",
        password: "",
    };

    get injected() {
        return this.props as IAuthProps;
    }

    @observable
    public isAuth = false;
    @observable
    public error = null;
    @observable
    public pending = false;

    @action
    public loginChangeHandler = (event: any) => {
        this.user["login"] = event.target.value;
    }

    @action
    public passwordChangeHandler = (event: any) => {
        this.user["password"] = event.target.value;
    }

    public state = {
        open: false,
        login: "",
        password: "",
    };

    public handleClose = () => {
        this.setState({
            open: false,
        });
    }

    public handleClickOpen = () => {
        this.setState({
            open: true,
        });
    }

    public handleAuth = (event: any) => {
        event.preventDefault();
        const { auth } = this.injected;
        this.pending = true;
        this.isAuth = false;
        this.error = null;

        auth.authenticate(this.user["login"].trim(), this.user["password"].trim())
            .then(action(() => { this.isAuth = true; this.pending = false; }))
            .catch((err: any) => { this.error = err; this.pending = false; });
        // TODO: check why finally doesn't support.
        // .finally(() => { this.pending = false; });
    }

    public handleChange(e: any) {
        this.setState({
            login: e.target.value,
        });
    }

    public render() {
        // let errText = !!this.error && this.error.userMessage;
        if (!this.pending && this.isAuth) {
            return <Redirect to="/" />;
        }

        return (
            <div>
                <Button onClick={this.handleClickOpen}>Войти</Button>
                <Dialog
                    open={this.state.open}
                    onClose={this.handleClose}
                    aria-labelledby="form-dialog-title"
                >
                    <DialogTitle id="form-dialog-title">Subscribe</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            Войдите для доступа к страницам.
                    </DialogContentText>
                        <TextField
                            autoFocus={true}
                            margin="dense"
                            id="phone"
                            label="Телефон"
                            type="text"
                            fullWidth={true}
                            onChange={this.loginChangeHandler}
                        />
                        <TextField
                            autoFocus={true}
                            margin="dense"
                            id="password"
                            label="Пароль"
                            type="password"
                            fullWidth={true}
                            onChange={this.passwordChangeHandler}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                            закрыть
                        </Button>
                        <Button onClick={this.handleAuth} color="primary">
                            Войти
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default LoginPage;
