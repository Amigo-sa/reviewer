import * as React from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

import { Switch, Route } from "react-router-dom";
import CreateReview from "./CreateReview";
import ViewReviews from "./ViewReviews";
import ViewReview from "./ViewReview";

class Reviews extends React.Component<any> {
    public render() {
        return (
            <>
                <Header
                    title={"Главная"}
                    size={"big"}
                />
                <Switch>
                    <Route path="/reviews/list" component={ViewReviews} />
                    <Route path="/reviews/view" component={ViewReview} />
                    <Route path="/reviews/new" component={CreateReview} />
                </Switch>
                <Footer />
            </>
        );
    }
}

export const urlReviewNew =
    (personalId: string, specializationId: string) => `/reviews/new?id=${personalId}&specid=${specializationId}`;
export const urlReviewView = (reviewId: string) => `/reviews/view?id=${reviewId}`;
export const urlReviewList = (personalId: string) => `/reviews/list?id=${personalId}`;

export default Reviews;
