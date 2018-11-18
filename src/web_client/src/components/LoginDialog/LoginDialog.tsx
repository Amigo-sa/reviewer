import * as React from "react";
import {
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    TextField,
    LinearProgress,
    Button,
} from "@material-ui/core";
import { computed } from "mobx";
import { observer, inject } from "mobx-react";
import { AuthStore } from "../../model/AuthStore";

// #TODO перейти на другую схему, лишнее убрать
interface IAuthProps {
    authStore?: AuthStore;
    handleClose: (event: any) => void;
}

/* TODO временно упростим логику
interface IField {
    value?: string;
    id: string;
    label: string;
    type: string;
}

interface IStep {
    field: IField;
    text: string;
}
*/

interface IState {
    step: number;
    login: string;
    password: string;
    isAuth: boolean;
    error: string;
}

@inject("authStore")
@observer
class LoginDialog extends React.Component<IAuthProps, IState>{

    private steps: string[];

    public state = {
        step: 0,
        login: "",
        password: "",
        isAuth: false,
        error: "",
    };

    private changeStepLoginField = (e: any) => {
        this.setState({ login: e.target.value });
    }

    private changeStepPasswordField = (e: any) => {
        this.setState({ password: e.target.value });
    }

    private handleNextStep = () => {
        const { step } = this.state;
        this.setState({ step: step + 1 });
    }

    private handlePrevStep = () => {
        const { step } = this.state;
        this.setState({ step: step - 1 });
    }

    @computed
    get completed() {
        return Math.round((this.state.step + 1) / this.steps.length * 100);
    }

    @computed
    get isCompleted() {
        return (this.state.step + 1) === this.steps.length;
    }

    get injected() {
        return this.props as IAuthProps;
    }

    public componentWillMount() {
        this.steps = [
            "Введите номер телефона",
            "Введите пароль",
        ];
    }

    public handleAuth = () => {
        const { authStore } = this.injected;
        const { login, password } = this.state;

        if (authStore) {
            authStore.authenticate(login.trim(), password.trim())
                .then(() => { this.setState({ isAuth: true }); })
                .catch((err: any) => {
                    console.log("Error", err);
                    this.setState({ error: "Неверный вход, попробуйте еще раз" });
                });
        }
        // TODO: check why finally doesn't support.
        // .finally(() => { this.pending = false; });
    }

    public render() {
        const { step, error, isAuth } = this.state;
        const text = this.steps[step];
        return (
            <>
                <DialogTitle id="form-dialog-title">Вход в Skill for life review</DialogTitle>
                <DialogContent>
                    <LinearProgress variant="determinate" value={this.completed} />
                    {error &&
                        <DialogContentText color="error">{error}</DialogContentText>
                    }
                    {isAuth ?
                        <DialogContentText>Вы успешно вошли в аккаунт</DialogContentText>
                        :
                        <>
                            <DialogContentText>
                                Шаг {step + 1} из {this.steps.length}: {text}
                            </DialogContentText>
                            {step === 0 &&
                                <TextField
                                    autoFocus
                                    margin="normal"
                                    id={"login"}
                                    label={"Телефон"}
                                    type={"text"}
                                    value={this.state.login}
                                    fullWidth
                                    onChange={this.changeStepLoginField}
                                />
                            }
                            {step === 1 &&
                                <TextField
                                    autoFocus
                                    margin="normal"
                                    id={"password"}
                                    label={"Пароль"}
                                    type={"password"}
                                    value={this.state.password}
                                    fullWidth
                                    onChange={this.changeStepPasswordField}
                                />
                            }
                        </>
                    }
                </DialogContent>
                <DialogActions>
                    {step !== 0 ?
                        <Button onClick={this.handlePrevStep} color="primary">
                            Назад
                        </Button>
                        :
                        null
                    }
                    {!this.isCompleted ?
                        <Button onClick={this.handleNextStep} color="primary">
                            Далее
                        </Button>
                        :
                        <Button onClick={() => this.handleAuth()} color="primary">
                            Войти
                        </Button>
                    }
                </DialogActions>
            </>
        );
    }
}
export default LoginDialog;
