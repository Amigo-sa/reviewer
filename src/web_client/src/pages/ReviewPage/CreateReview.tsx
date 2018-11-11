import * as React from "react";
import { withRouter, RouteComponentProps } from "react-router";

import {
    Grid,
    Typography,
    Select,
    MenuItem,
    Button,
    TextField,
    LinearProgress,
    CircularProgress,
} from "@material-ui/core";

import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import Person from "src/server-api/persons/Person";

import { inject, observer } from "mobx-react";

import { UsersStore } from "src/stores/UsersStore";
import { SpecializationsStore } from "src/stores/SpecializationsStore";
import { ReviewsStore } from "src/stores/ReviewsStore";

import PersonSpecialization, { PersonSpecializationList } from "src/server-api/persons/PersonSpecialization";
import { urlReviewList } from ".";

const styles = (theme: Theme) => createStyles({
    root: {
        backgroundColor: "#017BC3",
        padding: "55px 70px 46px",
        color: "#FFF",
        marginBottom: 35,
    },
    row: {
        marginBottom: 35,
    },
});

interface IDetailParams {
    id: string;
    specid: string;
}

interface IReviewPageProps extends WithStyles<typeof styles> {
    usersStore?: UsersStore;
    specializationsStore?: SpecializationsStore;
    reviewsStore?: ReviewsStore;
}

interface IState {
    person?: Person;
    loading: boolean;
    submitInProgress: boolean;
    loadingError: string;
    specializationId: string;
    specializations?: PersonSpecializationList;
    loadingSpecialization: boolean;

    topic: string;
    description: string;
    value: string;
}

// TODO: add state interface
@inject("usersStore", "specializationsStore", "reviewsStore")
@observer
class CreateReview extends React.Component<IReviewPageProps & RouteComponentProps<IDetailParams>, IState> {

    public state: IState = {
        loading: false,
        submitInProgress: false,
        loadingError: "",
        specializationId: "",
        loadingSpecialization: false,
        topic: "",
        description: "",
        value: "",
    };

    get injected() {
        return this.props as IReviewPageProps;
    }

    public componentDidMount() {
        // Получение данных из строки бразуера
        // /personal/:id/review/:specid

        const { match } = this.props;
        const personId = match.params.id;
        const specializationId = match.params.specid;
        this.setState({ loading: true, specializationId });
        this._loadPerson(personId);
    }

    public render() {

        const { classes } = this.props;
        const {
            person,
            topic,
            description,
            value,
            specializationId,
            specializations,
            loading,
            loadingError,
            submitInProgress,
        } = this.state;
        return (
            <Grid container className={classes.root}>
                {loading ? <LinearProgress /> : null}
                {loadingError ? { loadingError } : null}
                <Grid item className={classes.row} xs={12}>
                    <Typography component="h4" color="textPrimary" align="left" variant="h4" gutterBottom>
                        Отзыв на пользователя {person && this._fio(person)}
                    </Typography>
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    <TextField
                        id="topic"
                        placeholder="Заголовок"
                        required={true}
                        value={topic}
                        onChange={(event) => this.setState({ topic: event.target.value })}
                    />
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    {specializations && specializations.list &&
                        <Select
                            id="specializationId"
                            value={specializationId || specializations.list[0].id}
                            onChange={(event: any) =>
                                this.setState({ specializationId: event.target.value })
                            }
                        >
                            {specializations.list.map((item: PersonSpecialization) => {
                                return (
                                    <MenuItem
                                        key={item.id}
                                        value={item.id}>
                                        {item.specialization_type}({item.department_name})
                                </MenuItem>
                                );
                            })}
                        </Select>
                    }
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    <TextField
                        id="description"
                        placeholder="Описание"
                        value={description}
                        required={true}
                        onChange={(event) => this.setState({ description: event.target.value })}
                    />
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    <Select
                        id="value"
                        value={value || false}
                        required={true}
                        onChange={(event) => {
                            this.setState({ value: event.target.value });
                        }}
                    >
                        <MenuItem value="">Выберите оценку</MenuItem>
                        <MenuItem value="1">1</MenuItem>
                        <MenuItem value="2">2</MenuItem>
                        <MenuItem value="3">3</MenuItem>
                        <MenuItem value="4">4</MenuItem>
                        <MenuItem value="5">5</MenuItem>
                        <MenuItem value="6">6</MenuItem>
                        <MenuItem value="7">7</MenuItem>
                        <MenuItem value="8">8</MenuItem>
                        <MenuItem value="9">9</MenuItem>
                        <MenuItem value="10">10</MenuItem>
                    </Select>
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    {submitInProgress ?
                        <CircularProgress />
                        :
                        <Button
                            onClick={this._submitReview}
                            color="primary"
                            variant="contained"
                        >
                            Добавить отзыв
                        </Button>
                    }
                </Grid>
            </Grid>
        );
    }

    // Private methods
    private _fio(reviewer: Person) {
        return reviewer.surname + " "
            + reviewer.first_name + " "
            + reviewer.middle_name;
    }

    // Получение информации о пользователе по ID
    private _loadPerson(id: string): void {
        const { usersStore, specializationsStore } = this.injected;
        let { specializationId } = this.state;

        // загрузка пользователя на которого оставляют отзыв
        if (usersStore) {
            usersStore.get(id)
                .then((user) => {
                    this.setState({ person: user, loading: false });
                })
                .catch(() => this.setState({ loading: false, loadingError: "Не загружен пользователь" }));
        }

        // загрузка списка специализаций по которым можно оставить отзыв
        if (specializationsStore) {
            specializationsStore.get(id)
                .then((res) => {
                    if (!specializationId) {
                        specializationId = res && res.list[0].id || "";
                    }
                    this.setState({
                        specializations: res,
                        loadingSpecialization: true,
                        specializationId,
                    });
                });
        }
    }

    // #TODO check fields error before submit
    private _checkErrors(): boolean {
        const { topic, description, value } = this.state;
        if (!topic || !description || !value) {
            return true;
        }
        return false;
    }

    private _submitReview = (): void => {
        const { topic, description, value, specializationId } = this.state;
        const { reviewsStore } = this.injected;
        if (this._checkErrors() !== false) {
            // #TODO подсветка полей с ошибками
            alert("Ошибки при запонлении отзыва");
        }

        this.setState({ submitInProgress: true, loadingError: "" });
        // #TODO переделать на вызов ReviewsStore add review
        if (reviewsStore) {

            reviewsStore.addReview(specializationId, topic, description, parseInt(value, 10))
                .then((id: string) => {
                    console.log("Успешно оставлен отзыв", id);
                    const { person } = this.state;
                    if (person) {
                        this.props.history.push(urlReviewList(person.id));
                    }
                    this.setState({ submitInProgress: false });
                })
                .catch((err: any) => {
                    console.log(`Something go wrong!`, err);
                    this.setState({ submitInProgress: false, loadingError: err });
                });
        } else {
            this.setState({ submitInProgress: false, loadingError: "невозможно отправить отзыв" });
        }
    }

}

export default withStyles(styles)(withRouter(CreateReview));
