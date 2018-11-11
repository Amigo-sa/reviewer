import * as React from "react";
import {
    Grid,
    Typography,
    LinearProgress,
    Paper,
} from "@material-ui/core";

import { withRouter, RouteComponentProps } from "react-router";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import { inject, observer } from "mobx-react";
import { ReviewsStore, ReviewSpecializationInfo, FindReviewsViews } from "src/stores/ReviewsStore";

import Person from "src/server-api/persons/Person";
import { AuthStore } from "src/stores/AuthStore";
import { Link } from "react-router-dom";
import { personUrlById } from "src/constants";
import { IPersonShort } from "src/server-api/reviews/Review";
import { UsersStore } from "src/stores/UsersStore";

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
    dateLabel: {
        fontSize: "12px",
        fontWeight: "normal",
        textAlign: "left",
        lineHeight: "16px",
        color: "#9B9B9B",
    },
    specializationLabel: {
        fontSize: "16px",
        lineHeight: "22px",
        color: "#212529",
        textAlign: "left",
        fontStyle: "italic",
    },
});

interface IDetailParams {
    id: string;
}

interface IReviewsPageProps extends WithStyles<typeof styles> {
    reviewsStore?: ReviewsStore;
    authStore?: AuthStore;
    usersStore?: UsersStore;
}

interface IState {
    person: Person | null;
    isCurrentPerson: boolean;
    reviews: ReviewSpecializationInfo[];
    length: number;
    loading: boolean;
    loadingError: string;
}

@inject("authStore", "reviewsStore", "usersStore")
@observer
class ViewReviews extends React.Component<IReviewsPageProps & RouteComponentProps<IDetailParams>, any> {

    public state: IState = {
        person: null,
        isCurrentPerson: false,
        reviews: [],
        length: 0,
        loading: false,
        loadingError: "",
    };

    get injected() {
        return this.props as IReviewsPageProps;
    }

    public componentDidMount() {
        const { authStore } = this.injected;
        const { match } = this.props;
        let personId = match.params.id;
        let isCurrentPerson = false;
        if (!personId && authStore) {
            personId = authStore.user.uid || "";
            isCurrentPerson = true;
        }
        this.setState({ loading: true, isCurrentPerson });

        this._loadPerson(personId)
            .then(() => this._loadReviews(personId))
            .then((reviews) => this.setState({ reviews: reviews.list, length: reviews.length, loading: false }))
            .catch(() => this.setState({ loading: false }));
    }

    public render() {

        const { classes } = this.props;
        const { person, isCurrentPerson, loading, loadingError, reviews, length } = this.state;

        return (
            <Grid container className={classes.root}>
                {loadingError ? { loadingError } : null}
                {loading ? <LinearProgress />
                    :
                    null
                }
                {person ?

                    <Grid item xs={12}>
                        <Typography
                            component="h4" color="textPrimary" align="left" variant="h4" gutterBottom
                        >
                            {isCurrentPerson ? "Отзывы обо мне" : "Отзывы о пользователе "}
                            {!isCurrentPerson && this._fio(person, true)}
                        </Typography>
                    </Grid>
                    :
                    null
                }
                {length ?
                    reviews.map((review, index) => {
                        return (
                            <Grid key={index} item className={classes.row} xs={12}>
                                <Paper>
                                    <Typography className={classes.dateLabel}>
                                        {review.reviewDate.toLocaleDateString()}
                                    </Typography>
                                    <Typography variant="h5" component="h3">
                                        {review.reviewTopic}
                                    </Typography>
                                    <Typography className={classes.specializationLabel}>
                                        Специализация: {review.specializationDetail}
                                    </Typography>
                                    <Typography component="p">
                                        {review.reviewDescription}
                                    </Typography>
                                    <Typography component="h6" align="right" variant="h6" gutterBottom>
                                        {this._fio(review.reviewerName)}
                                    </Typography>
                                </Paper>
                            </Grid>
                        );
                    })
                    :
                    "Пока не оставлено ни одного отзыва"
                }
            </Grid>
        );
    }

    private _fio(reviewer: IPersonShort, full?: boolean) {
        return (
            <Link to={personUrlById(reviewer.id)} >
                {reviewer.surname} {reviewer.first_name} {full && reviewer.middle_name}
            </Link>
        );
    }

    // #TODO Получение информации о пользователе оставившем отзыв по ID
    private _loadPerson(id: string): Promise<void> {
        const { usersStore } = this.injected;
        if (usersStore) {
            return usersStore.get(id)
                .then((user) => {
                    this.setState({ person: user });
                })
                .catch(() => {
                    this.setState({ loadingError: "Не загружен пользователь" });
                });
        }
        return Promise.reject();
    }

    private _loadReviews(id: string): Promise<FindReviewsViews> {
        const { reviewsStore } = this.injected;
        if (reviewsStore) {
            return reviewsStore.getList(id)
                .then((reviews) => {
                    if (reviews && reviews.length && reviews.list) {
                        return reviews;
                    }
                    throw new Error("Ошибка загрузки отзывов");
                }).catch(() => { throw new Error("Ошибка загрузки отзывов"); });
        }
        throw new Error("Ошибка загрузки отзывов");
    }
}

export default withStyles(styles)(withRouter(ViewReviews));
