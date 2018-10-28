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
import { UsersStore } from "src/stores/UsersStore";

import ReviewsApi from "src/server-api/reviews/ReviewsApi";
import Review from "src/server-api/reviews/Review";

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
class ViewReview extends React.Component<IReviewPageProps & RouteComponentProps<any>, any> {

    public state = {
        review: new Review(),
        loading: false,
        loadingError: "",
    };

    get injected() {
        return this.props as IReviewPageProps;
    }

    public componentDidMount() {

        const query = qs.parse(this.props.location.search, {
            ignoreQueryPrefix: true,
        });
        const reviewId = query["id"];

        this._loadReview(reviewId)
            .then((review) => {
                this.setState({ review, loading: true });
            })
            .catch((err) => console.error("Ошибка загрузки отзыва", err));
    }

    public render() {

        const { classes } = this.props;
        const { review, loading, loadingError } = this.state;
        return (
            <Grid container className={classes.root}>
                {loadingError ? { loadingError } : null}
                {loading ? <LinearProgress /> :
                    <>
                        <Grid item className={classes.row} xs={12}>
                            <Typography component="h4" color="textPrimary" align="left" variant="h4" gutterBottom>
                                Отзыв от {review.reviewer_id} по {review.subject_id}
                            </Typography>
                        </Grid>
                        <Grid item className={classes.row} xs={12}>
                            <Typography component="p" color="textPrimary" align="left" variant="caption" gutterBottom>
                                Тема {review.topic}
                            </Typography>
                        </Grid>
                        <Grid item className={classes.row} xs={12}>
                            <Typography component="p" color="textPrimary" align="left" variant="caption" gutterBottom>
                                Описание: <br /> {review.description}
                            </Typography>
                        </Grid>
                        <Grid item className={classes.row} xs={12}>
                            <Typography component="p" color="textPrimary" align="left" variant="caption" gutterBottom>
                                Оценка {review.value}
                            </Typography>
                        </Grid>
                    </>
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

    private _loadReview(id: string): Promise<Review> {
        return ReviewsApi.getReview(id).then((review) => {
            return review.data;
        });
    }
}

export default withStyles(styles)(withRouter(ViewReview));
