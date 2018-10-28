
import * as React from "react";
import * as qs from "qs";
import {
    Grid,
    Typography,
    FormControl,
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
import ReviewsApi from "src/server-api/reviews/ReviewsApi";
import PostReviewRequest from "src/server-api/reviews/PostReviewRequest";
import PostReviewResponce from "src/server-api/reviews/PostReviewResponce";
import { withRouter, RouteComponentProps } from "react-router";

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

interface IReviewPageProps extends WithStyles<typeof styles> {
    usersStore?: UsersStore;
}

@inject("usersStore")
@observer
class CreateReview extends React.Component<IReviewPageProps & RouteComponentProps<any>, any> {

    public state = {
        person: new Person(),
        loading: false,
        submitInProgress: false,
        loadingError: "",
        specializationId: "",
        review: new PostReviewRequest(),
    };

    get injected() {
        return this.props as IReviewPageProps;
    }

    public componentDidMount() {

        const query = qs.parse(this.props.location.search, {
            ignoreQueryPrefix: true,
        });
        const personId = query["id"];
        const specializationId = query["specid"];
        this.setState({ loading: true, specializationId });
        this._loadPerson(personId);
    }

    public handleChange = (name: string) => (event: any) => {
        const { review } = this.state;
        review[name] = event.target.value;
        this.setState({ review });
    }

    public submitReview(): boolean {
        const { review, specializationId } = this.state;

        if (this._checkErrors() !== false) {
            alert("Ошибки при запонлении отзыва");
            return false;
        }

        this.setState({ submitInProgress: true, loadingError: "" });

        ReviewsApi.addReview(specializationId, review)
            .then((res: PostReviewResponce) => {
                console.log(`Create new review with id ${res.id}`);
                if (res.id) {
                    this.props.history.replace(`/reviews/view?id=${res.id}`);
                } else {
                    this.props.history.goBack();
                }
            })
            .catch((err: any) => {
                console.log(`Something go wrong!`, err);
                this.setState({ submitInProgress: false, loadingError: err });
            });
        return true;
    }

    public render() {

        const { classes } = this.props;
        const { person, review, loading, loadingError, submitInProgress } = this.state;
        return (
            <Grid container className={classes.root}>
                {loading ? <LinearProgress /> : null}
                {loadingError ? { loadingError } : null}
                <Grid item className={classes.row} xs={12}>
                    <Typography component="h4" color="textPrimary" align="left" variant="h4" gutterBottom>
                        Отзыв на пользователя {person.surname} {person.first_name} {person.middle_name}
                    </Typography>
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    <FormControl>
                        <TextField
                            id="topic"
                            placeholder="Заголовок"
                            value={review.topic}
                            onChange={this.handleChange("topic")}
                        />
                    </FormControl>
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    <FormControl>
                        <TextField
                            id="description"
                            placeholder="Описание"
                            value={review.description}
                            onChange={this.handleChange("description")}
                        />
                    </FormControl>
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    <FormControl>
                        <Select
                            id="value"
                            value={review.value}
                            onChange={this.handleChange("value")}
                        >
                            <MenuItem value="">Выберите оценку</MenuItem>
                            <MenuItem value="0">0</MenuItem>
                            <MenuItem value="20">1</MenuItem>
                            <MenuItem value="40">2</MenuItem>
                            <MenuItem value="60">3</MenuItem>
                            <MenuItem value="80">4</MenuItem>
                            <MenuItem value="100">5</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item className={classes.row} xs={12}>
                    {submitInProgress ?
                        <CircularProgress />
                        :
                        <Button
                            onClick={this.submitReview}
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

    // Получение информации о пользователе по ID
    private _loadPerson(id: string): void {
        const { usersStore } = this.injected;
        if (usersStore) {
            usersStore.get(id)
                .then((user) => {
                    this.setState({ person: user, loading: false });
                })
                .catch(() => this.setState({ loading: false, loadingError: "Не загружен пользователь" }));
        }
    }

    // #TODO check fields error before submit
    private _checkErrors(): boolean {
        // const { review } = this.state;
        return true;
    }
}

export default withStyles(styles)(withRouter(CreateReview));
