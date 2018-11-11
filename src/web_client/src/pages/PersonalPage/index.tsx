import * as React from "react";
import { Grid, LinearProgress } from "@material-ui/core";
import PersonalInfo from "./components/PersonalInfo";
import LeftMenu from "src/pages/LeftMenu";
import Footer from "src/components/Footer";
import Header from "src/components/Header";
import { match } from "react-router-dom";

import { observer } from "mobx-react";
import PersonalPageVM from "./viewmodel/PersonalPageVM";
import ReviewsComponent from "./components/ReviewsComponent";

interface IDetailParams {
    id: string;
}

interface IProps {
    match: match<IDetailParams>;
}

@observer
class PersonalPage extends React.Component<IProps> {

    public componentDidMount() {
        this._updatePerson();
    }

    public componentDidUpdate(prevProps: IProps) {
        if (prevProps.match.params.id !== this.props.match.params.id) {
            this._updatePerson();
        }
    }

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
                            {this._personalPageVM.loaded
                                ?
                                <PersonalInfo
                                    viewModel={this._personalPageVM.personalInfoVM}
                                    isCurrentPerson={this._personalPageVM.isCurrentPerson}
                                />
                                :
                                <LinearProgress />
                            }
                        </Grid>
                    </Grid>
                    <ReviewsComponent
                        isCurrentPerson={this._personalPageVM.isCurrentPerson}
                        viewModel={this._personalPageVM.reviewsVM} />
                </Grid>
                <Footer />
            </>
        );
    }

    // Private methods

    private _updatePerson() {
        this._personalPageVM.loadPersonInfo(this.props.match.params.id);
    }

    // Private fields

    /**
     * View model of page.
     */
    private _personalPageVM: PersonalPageVM = new PersonalPageVM();
}

export default PersonalPage;
