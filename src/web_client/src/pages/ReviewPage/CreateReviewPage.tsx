import * as React from "react";
import { Grid } from "@material-ui/core";
import LeftMenu from "src/pages/components/LeftMenu";
import Footer from "src/pages/components/Footer";
import Header from "src/pages/components/Header";

import CreateReview from "./CreateReview";

class CreateReviewPage extends React.Component {

    public render() {
        return (
            <>
                <Header
                    title="Cтраница отзыва"
                    size="default" />
                <Grid container item xs={12}>
                    {/* Left menu + personal info */}
                    <Grid container item spacing={24}>
                        <Grid item xs={2}>
                            <LeftMenu />
                        </Grid>
                        <Grid item xs={10}>
                            <CreateReview />
                        </Grid>
                    </Grid>
                </Grid>
                <Footer />
            </>
        );
    }
}

export default CreateReviewPage;
