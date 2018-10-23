import * as React from "react";
import { Grid } from "@material-ui/core";
import PersonalInfo from "./PersonalInfo";
import LeftMenu from "src/pages/LeftMenu";
import Footer from "src/components/Footer";
import Header from "src/components/Header";

class PersonalPage extends React.Component {
    public render() {
        return (
            <>
                <Header
                    title="Персональная страница"
                    size="default" />
                <Grid container item xs={12}>
                    {/* Left menu + personal info */}
                    <Grid container item spacing={24}>
                        <Grid item xs={2}>
                            <LeftMenu />
                        </Grid>
                        <Grid item xs={10}>
                            <PersonalInfo />
                        </Grid>
                    </Grid>
                    {/* My surveys */}
                    {/* My reviews */}
                </Grid>
                <Footer />
            </>
        );
    }
}

export default PersonalPage;
