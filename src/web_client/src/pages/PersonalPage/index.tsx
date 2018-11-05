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
    authStore?: AuthStore;
    specializationsStore: SpecializationsStore;
}

@inject("usersStore", "authStore", "specializationsStore")
@observer
class PersonalPage extends React.Component<IProps> {

    public person: Person;
    public specializations: PersonSpecializationList;

    public state = {
        loadingPerson: false,
        loadingSpecialization: false,
    };

    get injected() {
        return this.props as IProps;
    }

    public componentDidMount() {
        // tslint:disable-next-line:no-shadowed-variable
        const { match } = this.props;
        const { usersStore, specializationsStore, authStore } = this.injected;
        let personId;
        if (match.params.id) {
            // it is parameterized case
            console.log("ID", match.params.id);
            personId = match.params.id;
        }
        else {
            // there is not parameters info, so show personal info for current user
            console.log("current user");
            personId = authStore && authStore.user.uid;
        }

        if (personId) {
            usersStore.get(personId).then((res) => {
                this.person = res || new Person();
            }).then(() => this.setState({ loadingPerson: true }));
            specializationsStore.get(personId).then((res) => {
                this.specializations = res || new PersonSpecializationList();
            }).then(() => this.setState({ loadingSpecialization: true }));
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
                            {this.person && this.specializations ?
                                <PersonalInfo
                                    person={this.person}
                                    specializations={this.specializations}
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
}

export default PersonalPage;
