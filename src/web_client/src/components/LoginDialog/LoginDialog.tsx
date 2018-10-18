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

// #TODO перейти на другую схему, лишнее убрать
interface ILoginDialog {
    handleClose: (event: any) => void;
    handleAuth?: (event: any) => void;
    handleRegister?: (event: any) => void;
}

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

// #TODO Плохое решение подумать может просто скрывать поля по шагам, ломается
function _renderTextField(field: IField, callBack: (event: any) => void): JSX.Element {
    return (
        <TextField
            autoFocus={true}
            margin="normal"
            id={field.id}
            label={field.label}
            type={field.type}
            value={field.value}
            fullWidth={true}
            onChange={callBack}
        />
    );
}
class LoginDialog extends React.Component<ILoginDialog>{

    private steps: IStep[];

    public state = {
        step: 0,
    };

    private changeStepField = (e: any) => {
        const { step } = this.state;
        this.steps[step].field.value = e.target.value;
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

    public componentWillMount() {
        this.steps = [
            { field: { id: "phone", label: "Телефон", type: "text" }, text: "Введите номер телефона" },
            { field: { id: "password", label: "Пароль", type: "password" }, text: "Введите пароль" },
        ];
    }
    public render() {
        const { handleAuth } = this.props;
        const { step } = this.state;
        const { text, field } = this.steps[step];
        return (
            <>
                <DialogTitle id="form-dialog-title">Вход в Skill for life review</DialogTitle>
                <DialogContent>
                    <LinearProgress variant="determinate" value={this.completed} />
                    <DialogContentText>
                        Шаг {step + 1} из {this.steps.length}: {text}
                    </DialogContentText>
                    {_renderTextField(field, this.changeStepField)}
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
                        <Button onClick={handleAuth} color="primary">
                            Войти
                        </Button>
                    }
                </DialogActions>
            </>
        );
    }
}
export default LoginDialog;
