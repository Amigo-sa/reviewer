import * as React from "react";
import { ReviewsVM, ReviewInfo } from "../viewmodel/ReviewsVM";
import { Grid, Button, Paper, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";
import { urlReviewList, urlReviewView } from "src/pages/ReviewPage";
import { personUrlById } from "src/constants";
import { IPersonShort } from "src/server-api/reviews/Review";
import { observer } from "mobx-react";

interface IProps {
    viewModel: ReviewsVM;
    personId: string;
    isCurrentPerson: boolean;
}

@observer
export default class ReviewsComponent extends React.Component<IProps> {

    public render() {
        // const { viewModel } = this.props;
        if (!this.props.viewModel.loaded) {
            return null;
        }
        else {
            const { personId, viewModel, isCurrentPerson } = this.props;
            const reviewsLink = isCurrentPerson ? urlReviewList() : urlReviewList(personId);
            return (
                <Grid container xs={12} direction={"column"}>
                    <Grid item xs={12}>
                        <Typography variant="h5" component="h3">
                            {this.props.isCurrentPerson ?
                                "Отзывы обо мне"
                                :
                                "Отзывы"
                            }
                        </Typography>
                    </Grid>

                    <Grid item container xs={12}>
                        {viewModel.reviews.length === 0 ?
                            <Typography variant="h5" component="h3">Тут пока нету ни одного отзыва</Typography>
                            :
                            <>
                                {viewModel.reviews.map((item, index) => {
                                    return <ReviewItem key={index} reviewInfo={item} />;
                                })
                                }
                            </>
                        }
                    </Grid>
                    <Grid item xs={12}>
                        <Button><Link to={reviewsLink}>Показать все</Link></Button>
                    </Grid>
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
        const { reviewInfo } = this.props;
        return (
            <Grid item xs={12} md={4}>
                <Paper>
                    <Typography variant="h5" component="h3">
                        {this._fio(reviewInfo.reviewerName)}
                    </Typography>
                    <Typography component="i">
                        {reviewInfo.specializationDetail}
                    </Typography>
                    <Typography component="p">
                        {reviewInfo.reviewDescription}
                    </Typography>
                    <Typography component="h6" color="textPrimary" align="right" variant="h6" gutterBottom>
                        <Link to={urlReviewView(reviewInfo.reviewId)}>Подробнее</Link>
                    </Typography>
                </Paper>
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
}
