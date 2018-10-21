import { Provider } from "mobx-react";
import * as React from "react";
import * as ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";
import registerServiceWorker from "./registerServiceWorker";
import authStore from "./stores/AuthStore";
import searchStore from "./stores/SearchStore";
import { MuiThemeProvider } from "@material-ui/core/styles";
import theme from "./Theme";
import CssBaseline from "@material-ui/core/CssBaseline";

const stores = {
    authStore,
    searchStore,
};

ReactDOM.render(
    <Provider {...stores}>
        <BrowserRouter>
            <MuiThemeProvider theme={theme}>
                <CssBaseline />
                <App />
            </MuiThemeProvider>
        </BrowserRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
registerServiceWorker();
