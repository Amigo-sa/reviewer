import * as React from "react";
import { ReviewsVM, ReviewInfo } from "../viewmodel/ReviewsVM";
import { Grid, Button } from "@material-ui/core";

interface IProps {
    viewModel: ReviewsVM;
    isCurrentPerson: boolean;
}

export default class ReviewsComponent extends React.Component<IProps> {

    public render() {
        // const { viewModel } = this.props;

        if (this.props.viewModel.reviews.length === 0) {
            return null;
        }
        else {
            return (
                <Grid container xs={12}>
                    {this.props.isCurrentPerson
                        ?
                        "Отзывы обо мне"
                        :
                        "Отзывы"}

                    {this.props.viewModel.reviews.map((item, index) => {
                        return <ReviewItem key={index} reviewInfo={item} />;
                    })}

                    {this.props.viewModel.canShowMoreReviews
                        ?
                        <Button> Показать еще </Button>
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
