import * as React from "react";
import Header from "src/pages/components/Header";
import Footer from "src/pages/components/Footer";

import { Switch, Route } from "react-router-dom";
import ViewReviews from "./ViewReviewsPage";
import ViewReview from "./ViewReview";
import { Grid } from "@material-ui/core";
import LeftMenu from "src/pages/components/LeftMenu";

class Reviews extends React.Component<any> {
    public render() {
        return (
            <>
                <Header
                    title={"Главная"}
                    size={"big"}
                />
                <Grid container item spacing={24}>
                    <Grid item xs={2}>
                        <LeftMenu />
                    </Grid>
                    <Grid item xs={10}>
                        <Switch>
                            <Route exact path="/reviews" component={ViewReviews} />
                            <Route exact path="/reviews/:id" component={ViewReviews} />
                            <Route path="/reviews/view/:id" component={ViewReview} />
                        </Switch>
                    </Grid>
                </Grid>
                <Footer />
            </>
        );
    }
}

export const urlReviewNew =
    (personalId: string, specializationId?: string) => `/personal/${personalId}/review/${specializationId || ""}`;
export const urlReviewView = (reviewId: string) => `/reviews/view/${reviewId}`;
export const urlReviewList = (personalId?: string) => `/reviews/${personalId || ""}`;

export default Reviews;
