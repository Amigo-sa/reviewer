
import * as React from "react";
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

import ReviewsApi from "src/server-api/reviews/ReviewsApi";
import PostReviewRequest from "src/server-api/reviews/PostReviewRequest";
import PostReviewResponse from "src/server-api/reviews/PostReviewResponse";
import { withRouter, RouteComponentProps } from "react-router";
import PersonSpecialization, { PersonSpecializationList } from "src/server-api/persons/PersonSpecialization";

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
}

interface IState {
    person?: Person;
    loading: boolean;
    submitInProgress: boolean;
    loadingError: string;
    specializationId: string;
    review: PostReviewRequest;
    specializations?: PersonSpecializationList;
    loadingSpecialization: boolean;
}

// TODO: add state interface
@inject("usersStore", "specializationsStore")
@observer
class CreateReview extends React.Component<IReviewPageProps & RouteComponentProps<IDetailParams>, IState> {

    public state: IState = {
        loading: false,
        submitInProgress: false,
        loadingError: "",
        specializationId: "",
        review: new PostReviewRequest(),
        loadingSpecialization: false,
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
            review,
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
                        value={review.topic}
                        onChange={this._handleChange("topic")}
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
                        value={review.description}
                        required={true}
                        onChange={this._handleChange("description")}
                    />
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    <Select
                        id="value"
                        value={review.value || false}
                        required={true}
                        onChange={this._handleChange("value")}
                    >
                        <MenuItem value="">Выберите оценку</MenuItem>
                        <MenuItem value="0">0</MenuItem>
                        <MenuItem value="20">1</MenuItem>
                        <MenuItem value="40">2</MenuItem>
                        <MenuItem value="60">3</MenuItem>
                        <MenuItem value="80">4</MenuItem>
                        <MenuItem value="100">5</MenuItem>
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
        const { review } = this.state;
        if (!review.topic || !review.description || !review.value) {
            return true;
        }
        return false;
    }

    private _handleChange = (name: string) => (event: any) => {
        const { review } = this.state;
        review[name] = event.target.value;
        this.setState({ review });
    }

    private _submitReview = (): boolean => {
        const { review, specializationId } = this.state;
        if (this._checkErrors() !== false) {
            // #TODO подсветка полей с ошибками
            alert("Ошибки при запонлении отзыва");
            return false;
        }

        this.setState({ submitInProgress: true, loadingError: "" });
        // #TODO переделать на вызов ReviewsStore add review
        ReviewsApi.addReview(specializationId, review)
            .then((res: PostReviewResponse) => {
                console.log(`Create new review with id ${res.id}`);
                /*if (res.id) {
                    this.props.history.replace(`/reviews/view/${res.id}`);
                } else {
                    this.props.history.goBack();
                }*/
            })
            .catch((err: any) => {
                console.log(`Something go wrong!`, err);
                this.setState({ submitInProgress: false, loadingError: err });
            });
        return true;
    }

}

export default withStyles(styles)(withRouter(CreateReview));
