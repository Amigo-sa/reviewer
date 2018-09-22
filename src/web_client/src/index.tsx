import { Provider } from "mobx-react";
import * as React from "react";
import * as ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";
import registerServiceWorker from "./registerServiceWorker";
import AuthStore from "./stores/AuthStore";
const stores = {
    AuthStore,
};

ReactDOM.render(
    <Provider {...stores}>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
registerServiceWorker();
