import * as React from "react";
import Header from "src/pages/components/Header";
import Footer from "src/pages/components/Footer";

import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import { SearchStore } from "../../model/SearchStore";

import SearchResult from "./SearchResult";
import { observer, inject } from "mobx-react";
import SearchForm from "./SearchForm";
import FindPersonsRequest from "../../server-api/persons/FindPersonsRequest";
import { SpecializationsStore } from "src/model/SpecializationsStore";

interface ISearchPageProps extends WithStyles<typeof styles> {
    searchStore?: SearchStore;
    specializationsStore?: SpecializationsStore;
}

const styles = (theme: Theme) => createStyles({
    root: {
        backgroundColor: "#017BC3",
        display: "flex",
    },
});

interface IState {
    loading: boolean;
}

@inject("searchStore")
@observer
class SearchPeople extends React.Component<ISearchPageProps, IState> {

    public state: IState = {
        loading: false,
    };

    get injected() {
        return this.props as ISearchPageProps;
    }

    public render() {
        // #TODO вставить стили когда понадобяться
        // const { classes } = this.props;
        const { searchStore } = this.injected;
        // #TODO правильно получение данных так как searchStore может быть undefined
        const { resultList } = searchStore || { resultList: [] };
        return (
            <>
                <Header
                    title={"Главная"}
                    size={"big"}
                />
                <SearchForm
                    handleSearchPeople={this._handleSearchPeople}
                />
                <SearchResult
                    results={resultList}
                    loading={this.state.loading}
                />
                <Footer />
            </>
        );
    }

    // Private methods

    private _handleSearchPeople = (fields: FindPersonsRequest) => {
        // #TODO сделать поиск через searchStore
        const { searchStore } = this.injected;
        this.setState({ loading: true });
        return searchStore &&
            searchStore.sendSeacrhPeople(fields)
                .then(() => {
                    this.setState({ loading: false });
                })
                .then(() => searchStore.getPeopleSpecializations());
    }
}

export default withStyles(styles)(SearchPeople);
