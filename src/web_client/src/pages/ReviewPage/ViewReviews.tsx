import * as React from "react";
import * as qs from "qs";
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
import FindReviewResponce from "src/server-api/reviews/FindReviewResponce";

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

interface IReviewsPageProps extends WithStyles<typeof styles> {
    reviewsStore?: ReviewsStore;
}

@inject("reviewsStore")
@observer
class ViewReviews extends React.Component<IReviewsPageProps & RouteComponentProps<any>, any> {

    public state = {
        loading: false,
        loadingError: "",
    };

    get injected() {
        return this.props as IReviewsPageProps;
    }

    public componentDidMount() {

        const query = qs.parse(this.props.location.search, {
            ignoreQueryPrefix: true,
        });
        const personId = query["id"];
        const { reviewsStore } = this.injected;
        this._loadReviews(personId)
            .then((reviews) => {
                if (reviewsStore && reviews && reviews.list) {
                    reviews.list.forEach((el) => reviewsStore.get(el.id));
                }
                this.setState({ loading: true });
            })
            .catch((err: any) => console.error("Ошибка загрузки отзывов", err));
    }

    public render() {

        const { classes } = this.props;
        const { reviewsStore } = this.injected;
        const { loading, loadingError } = this.state;
        return (
            <Grid container className={classes.root}>
                {loadingError ? { loadingError } : null}
                {loading ? <LinearProgress />
                    :
                    reviewsStore &&
                    reviewsStore.reviews.map((review, index) => {
                        return (
                            <Grid key={index} item container className={classes.root}>
                                <Grid item className={classes.row} xs={12}>
                                    <Typography
                                        component="h4" color="textPrimary" align="left" variant="h4" gutterBottom
                                    >
                                        Отзыв от {review.reviewer_id} по {review.subject_id}
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

    private _loadReviews(id: string): Promise<FindReviewResponce | null> {
        const findRequest = new FindReviewRequest();
        findRequest.person_id = id;
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
