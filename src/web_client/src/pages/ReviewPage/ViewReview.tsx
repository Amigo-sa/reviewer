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

import { IPersonShort } from "src/server-api/reviews/Review";
import { ReviewSpecializationInfo, ReviewsStore } from "src/model/ReviewsStore";
import { personUrlById } from "src/constants";
import { Link } from "react-router-dom";
import { AuthStore } from "src/model/AuthStore";

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

interface IReviewPageProps extends WithStyles<typeof styles> {
    authStore?: AuthStore;
    reviewsStore?: ReviewsStore;
}

interface IState {
    review: ReviewSpecializationInfo;
    loading: boolean;
    loadingError: string;
}

@inject("authStore", "reviewsStore")
@observer
class ViewReview extends React.Component<IReviewPageProps & RouteComponentProps<IDetailParams>, IState> {

    public state: IState = {
        review: new ReviewSpecializationInfo(),
        loading: false,
        loadingError: "",
    };

    get injected() {
        return this.props as IReviewPageProps;
    }

    public componentDidMount() {

        const { match } = this.props;
        const reviewId = match.params.id;
        this.setState({ loading: true });
        this._loadReview(reviewId)
            .then((review) => {
                if (review) {
                    this.setState({ review, loading: false });
                }
            })
            .catch((err) => console.error("Ошибка загрузки отзыва", err));
    }

    public render() {
        const { classes } = this.props;
        const { review, loading, loadingError } = this.state;
        return (
            <Grid container className={classes.root}>
                {loadingError ? { loadingError } : null}
                {loading ? <LinearProgress /> : null}
                {review.isLoaded && this._renderReview()}
            </Grid>
        );
    }

    private _renderReview() {
        const { classes } = this.props;
        const { review } = this.state;
        if (!review.isLoaded) {
            return;
        }
        return (
            <Grid item className={classes.row} xs={12}>
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
                    <Typography component="h6" color="textPrimary" align="right" variant="h6" gutterBottom>
                        {this._fio(review.reviewerName)}
                    </Typography>
                </Paper>
            </Grid>
        );
    }

    private _fio(reviewer: IPersonShort, full?: boolean) {
        const { authStore } = this.injected;
        const link = authStore && authStore.user.uid === reviewer.id ? personUrlById() : personUrlById(reviewer.id);
        return (
            <Link to={link} >
                {reviewer.surname} {reviewer.first_name} {full && reviewer.middle_name}
            </Link>
        );
    }

    private _loadReview(id: string): Promise<ReviewSpecializationInfo | undefined> {
        const { reviewsStore } = this.injected;
        if (reviewsStore) {
            return reviewsStore.get(id);
        }
        return Promise.reject(undefined);
    }
}

export default withStyles(styles)(withRouter(ViewReview));
