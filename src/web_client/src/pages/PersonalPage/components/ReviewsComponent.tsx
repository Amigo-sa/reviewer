import * as React from "react";
import { ReviewsVM, ReviewInfo } from "../viewmodel/ReviewsVM";
import { Grid, Button } from "@material-ui/core";
import { Link } from "react-router-dom";
import { urlReviewList } from "src/pages/ReviewPage";

interface IProps {
    viewModel: ReviewsVM;
    personId: string;
    isCurrentPerson: boolean;
}

export default class ReviewsComponent extends React.Component<IProps> {

    public render() {
        // const { viewModel } = this.props;
        if (this.props.viewModel.reviews.length === 0) {
            return null;
        }
        else {
            const { personId, viewModel, isCurrentPerson } = this.props;
            const reviewsLink = isCurrentPerson ? urlReviewList() : urlReviewList(personId);
            return (
                <Grid container xs={12}>
                    {this.props.isCurrentPerson
                        ?
                        "Отзывы обо мне"
                        :
                        "Отзывы"}

                    {viewModel.reviews.map((item, index) => {
                        return <ReviewItem key={index} reviewInfo={item} />;
                    })}

                    {viewModel.canShowMoreReviews
                        ?
                        <Button><Link to={reviewsLink}>Показать еще </Link> </Button>
                        :
                        null}

                </Grid>
            );
        }
    }
}

interface IReviewItemProps {
    reviewInfo: ReviewInfo;
}

class ReviewItem extends React.Component<IReviewItemProps> {

    public render() {
        return (
            <Grid container xs={12}>
                text
            </Grid>
        );
    }
}
