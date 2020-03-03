import * as React from "react";
import {
    Grid,
    LinearProgress,
} from "@material-ui/core";

import { withRouter, RouteComponentProps } from "react-router";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import { inject, observer } from "mobx-react";

import { ReviewSpecializationInfo, ReviewsStore } from "src/model/ReviewsStore";
import { AuthStore } from "src/model/AuthStore";
import FullReviewCard from "./components/FullReviewCard";

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
        const { authStore } = this.injected;
        const { review } = this.state;
        if (!review.isLoaded) {
            return;
        }
        return (
            <FullReviewCard
                review={review}
                currentUserId={authStore!.user.uid}
            />
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
