import * as React from "react";
import { Grid, LinearProgress } from "@material-ui/core";
import PersonalInfo from "./PersonalInfo";
import LeftMenu from "src/pages/LeftMenu";
import Footer from "src/components/Footer";
import Header from "src/components/Header";
import { match } from "react-router-dom";

import { inject, observer } from "mobx-react";
import { UsersStore } from "src/stores/UsersStore";
import { AuthStore } from "src/stores/AuthStore";
import { SpecializationsStore } from "src/stores/SpecializationsStore";
import Person from "src/server-api/persons/Person";
import { PersonSpecializationList } from "src/server-api/persons/PersonSpecialization";

interface IDetailParams {
    id: string;
}

interface IProps {
    match: match<IDetailParams>;
    usersStore: UsersStore;
    authStore: AuthStore;
    specializationsStore: SpecializationsStore;
}

interface IState {
    personalId: string;
    isCurrentUser: boolean; // TODO: we can make checking by auth store in render method
    loadingPerson: boolean;
    loadingSpecialization: boolean;
}

@inject("usersStore", "authStore", "specializationsStore")
@observer
class PersonalPage extends React.Component<IProps, IState> {

    // TODO: we can use _person ans specialization instead of it
    public state = {
        personalId: "",
        isCurrentUser: true,
        loadingPerson: false,
        loadingSpecialization: false,
    };

    get injected() {
        return this.props as IProps;
    }

    public componentDidMount() {
        this._updatePerson();
    }

    public componentDidUpdate(prevProps: IProps) {
        if (prevProps.match.params.id !== this.props.match.params.id) {
            this._updatePerson();
        }
    }

    public render() {
        if (this.props.match.params.id) {
            // it is parameterized case
            console.log(this.props.match.params.id);
        }
        else {
            // there is not parameters info, so show personal info for current user
            console.log("current user");
        }

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
                            {this._person && this._specializations ?
                                <PersonalInfo
                                    isPersonalPage={this._isPersonalPage}
                                    person={this._person}
                                    specializations={this._specializations}
                                />
                                :
                                <LinearProgress />
                            }
                        </Grid>
                    </Grid>
                    {/* My surveys */}
                    {/* My reviews */}
                </Grid>
                <Footer />
            </>
        );
    }

    // Private methods

    private _updatePerson() {
        // tslint:disable-next-line:no-shadowed-variable
        const { match } = this.props;
        const { usersStore, specializationsStore, authStore } = this.injected;

        let personId: string = "";
        let isCurrentUser: boolean = false;
        if (match.params.id) {
            // it is parameterized case
            personId = match.params.id;
            isCurrentUser = false;
        }
        else {
            // there is not parameters info, so show personal info for current user
            personId = authStore!.user.uid!;
            isCurrentUser = true;
        }

        this.setState({
            personalId: personId,
            isCurrentUser,
        });

        usersStore.get(personId).then((res) => {
            this._person = res || new Person();
        }).then(() => this.setState({ loadingPerson: true }));

        specializationsStore.get(personId).then((res) => {
            this._specializations = res || new PersonSpecializationList();
        }).then(() => this.setState({ loadingSpecialization: true }));
    }

    // Private fields

    private _person: Person;
    private _specializations: PersonSpecializationList;

    /**
     * Indicates if we show page for current user.
     */
    private _isPersonalPage: boolean = true;
}

export default PersonalPage;
