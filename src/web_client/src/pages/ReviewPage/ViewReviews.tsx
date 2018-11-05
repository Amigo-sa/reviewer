import * as React from "react";
import {
    Grid,
    Typography,
    LinearProgress,
} from "@material-ui/core";

import { withRouter, RouteComponentProps } from "react-router";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import { inject, observer } from "mobx-react";
import { ReviewsStore } from "src/stores/ReviewsStore";

import ReviewsApi from "src/server-api/reviews/ReviewsApi";
import FindReviewRequest from "src/server-api/reviews/FindReviewsRequest";
import FindReviewResponse from "src/server-api/reviews/FindReviewResponse";
import Person from "src/server-api/persons/Person";

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
}

interface IReviewsPageProps extends WithStyles<typeof styles> {
    reviewsStore?: ReviewsStore;
}

interface IReviewItemList {
    id: string;
    topic: string;
    description: string;
    value: string;
    reviewer: Person;
}
interface IState {
    reviews: IReviewItemList[];
    length: number;
    loading: boolean;
    loadingError: string;
}

@inject("reviewsStore")
@observer
class ViewReviews extends React.Component<IReviewsPageProps & RouteComponentProps<IDetailParams>, any> {

    public state: IState = {
        reviews: [],
        length: 0,
        loading: false,
        loadingError: "",
    };

    get injected() {
        return this.props as IReviewsPageProps;
    }

    public componentDidMount() {

        const { match } = this.props;
        const personId = match.params.id;
        this.setState({ loading: true });

        this._loadReviews(personId)
            .then((reviews) => {
                if (reviews) {
                    this.setState({ loading: false, reviews: reviews.list, length: reviews.length });
                } else {
                    this.setState({ loading: false });
                }
            })
            .catch((err: any) => console.error("Ошибка загрузки отзывов", err));
    }

    public render() {

        const { classes } = this.props;
        const { loading, loadingError, reviews, length } = this.state;

        return (
            <Grid container className={classes.root}>
                {loadingError ? { loadingError } : null}
                {loading ? <LinearProgress />
                    :
                    length &&
                    reviews.map((review, index) => {
                        return (
                            <Grid key={index} item container className={classes.root}>
                                <Grid item className={classes.row} xs={12}>
                                    <Typography
                                        component="h4" color="textPrimary" align="left" variant="h4" gutterBottom
                                    >
                                        Отзыв от {this._fio(review.reviewer)} по {review.id}
                                    </Typography>
                                </Grid>
                                <Grid item className={classes.row} xs={12}>
                                    <Typography
                                        component="p" color="textPrimary" align="left" variant="caption" gutterBottom
                                    >
                                        Тема {review.topic}
                                    </Typography>
                                </Grid>
                                <Grid item className={classes.row} xs={12}>
                                    <Typography
                                        component="p" color="textPrimary" align="left" variant="caption" gutterBottom
                                    >
                                        Описание: <br /> {review.description}
                                    </Typography>
                                </Grid>
                                <Grid item className={classes.row} xs={12}>
                                    <Typography
                                        component="p" color="textPrimary" align="left" variant="caption" gutterBottom
                                    >
                                        Оценка {review.value}
                                    </Typography>
                                </Grid>
                            </Grid>
                        );
                    })
                }
            </Grid>
        );
    }

    private _fio(reviewer: Person) {
        return reviewer.surname + " "
            + reviewer.first_name + " "
            + reviewer.middle_name;
    }

    // #TODO Получение информации о пользователе оставившем отзыв по ID
    /*
    private _loadPerson(id: string): void {
        const { usersStore } = this.injected;
        if (usersStore) {
            usersStore.get(id)
                .then((user) => {
                    this.setState({ reviewer: user, loading: true });
                })
                .catch(() => this.setState({ loading: false, loadingError: "Не загружен пользователь" }));
        }
    }
    */

    private _loadReviews(id: string): Promise<FindReviewResponse | null> {
        const findRequest = new FindReviewRequest();
        findRequest.person_id = id;
        findRequest.type = "specialization";
        return ReviewsApi.findSpecializationReview(findRequest)
            .then((reviews) => {
                if (reviews.length) {
                    return reviews;
                }
                return null;
            });
    }
}

export default withStyles(styles)(withRouter(ViewReviews));
