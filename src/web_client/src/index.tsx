import { Provider } from "mobx-react";
import * as React from "react";
import * as ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import HeaderMenu from "./components/Menu";
import "./index.css";
import registerServiceWorker from "./registerServiceWorker";
import authStore from "./stores/AuthStore";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";

const stores = {
    authStore,
};

ReactDOM.render(
    <Provider {...stores}>
        <BrowserRouter>
            <Grid
                container={true}
                spacing={24}
            >
                <Grid
                    item={true}
                    xs={12}
                >
                    <HeaderMenu/>
                </Grid>
                <Grid
                    item={true}
                    xs={12}
                >
                    <Paper><App /></Paper>
                </Grid>
            </Grid>
        </BrowserRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
registerServiceWorker();
