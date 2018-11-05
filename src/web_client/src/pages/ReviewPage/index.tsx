import * as React from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

import { Switch, Route } from "react-router-dom";
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
                    <Route exact path="/reviews/list" component={ViewReviews} />
                    <Route path="/reviews/list/:id" component={ViewReviews} />
                    <Route path="/reviews/view/:id" component={ViewReview} />
                </Switch>
                <Footer />
            </>
        );
    }
}

export const urlReviewNew =
    (personalId: string, specializationId?: string) => `/personal/${personalId}/review/${specializationId || ""}`;
export const urlReviewView = (reviewId: string) => `/reviews/view/${reviewId}`;
export const urlReviewList = (personalId: string) => `/reviews/list/${personalId}`;

export default Reviews;
