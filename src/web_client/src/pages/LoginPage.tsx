import * as React from "react";
import { Button } from "@material-ui/core";
import { Dialog } from "@material-ui/core";
import { AuthStore } from "../model/AuthStore";
import { inject, observer } from "mobx-react";
import { observable, action } from "mobx";
import { Redirect } from "react-router-dom";
import { REDIRECT_TO_AFTER_LOGIN } from "../constants";
import LoginDialog from "src/pages/components/LoginDialog";

interface IAuthProps {
    authStore: AuthStore;
}

interface IState {
    open: boolean;
    login: string;
    password: string;
}

@inject("authStore")
@observer
class LoginPage extends React.Component<IAuthProps, IState> {
    // TODO: remove hardcode really data
    @observable
    public user: object = {
        login: "78005553535",
        password: "12345678",
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

    public state: IState = {
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
        const { authStore } = this.injected;
        this.pending = true;
        this.isAuth = false;
        this.error = null;

        authStore.authenticate(this.user["login"].trim(), this.user["password"].trim())
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
            // TODO: need to redirect to page where we start login process.
            return <Redirect to={REDIRECT_TO_AFTER_LOGIN} />;
        }

        return (
            <>
                <Button onClick={this.handleClickOpen}>Войти</Button>
                <Dialog
                    open={this.state.open}
                    onClose={this.handleClose}
                    aria-labelledby="form-dialog-title"
                >
                    <LoginDialog
                        handleClose={this.handleClose}
                    />
                </Dialog>
            </>
        );
    }
}

export default LoginPage;
