import * as React from "react";
import { Grid } from "@material-ui/core";
import PersonalInfo from "./PersonalInfo";
import LeftMenu from "src/pages/LeftMenu";
import Footer from "src/components/Footer";
import Header from "src/components/Header";

class PersonalPage extends React.Component {
    public render() {
        return (
            <Grid
                container={true}>
                <Header
                    title="Персональная страница"
                    size="default" />
                <Grid
                    container={true}
                    item={true}
                    xs={12}>
                    {/* Left menu + personal info */}
                    <Grid
                        container={true}
                        item={true}>
                        <Grid
                            item={true}>
                            <LeftMenu />
                        </Grid>
                        <Grid
                            item={true}>
                            <PersonalInfo />
                        </Grid>
                    </Grid>
                    {/* My surveys */}
                    {/* My reviews */}
                </Grid>
                <Footer />
            </Grid>
        );
    }
}

export default PersonalPage;
