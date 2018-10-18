import * as React from "react";
import Grid from "@material-ui/core/Grid";
import Header from "../components/Header";
import Footer from "../components/Footer";

// #TODO вынести в общую компоненту layout и использовать хеадер и футер по умолчанию
// чтобы не указывать постоянно при создании новых страниц, возможно определить шаблоны

class Main extends React.Component {
    public render() {
        return (
            <>
                <Header
                    title={"Главная"}
                    size={"default"}
                />
                <Grid
                    item={true}
                    xs={12}
                >
                    {"Main page"}
                </Grid>
                <Footer />
            </>
        );
    }
}

export default Main;
