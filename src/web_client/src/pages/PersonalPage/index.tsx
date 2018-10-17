import * as React from "react";
import { Grid } from "@material-ui/core";
import { Link } from "react-router-dom";
import PersonalInfo from "./PersonalInfo";
import LeftMenu from "src/pages/LeftMenu";

class PersonalPage extends React.Component {
    public render() {
        return (
            <Grid
                container={true}>
                {/* Header */}
                <Grid
                    item={true}
                    xs={12}>
                    {/* TODO: why when I setup spacing equels to 8 and greater, then line move to top */}
                    {/* Links in center */}
                    <Grid
                        container={true}
                        alignContent="center"
                        spacing={0}
                        justify="center">
                        <Link to="">
                            О проекте
                    </Link>
                        <Link to="">
                            Участики
                    </Link>
                        <Link to="">
                            Регистрация
                    </Link>
                    </Grid>
                </Grid>

                {/* Body */}
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

                {/* Footer */}
                <Grid
                    item={true}
                    xs={12}>
                    Footer
                </Grid>
            </Grid>
        );
    }
}

export default PersonalPage;
