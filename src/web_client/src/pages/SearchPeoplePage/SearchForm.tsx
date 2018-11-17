
import * as React from "react";
import {
    Grid,
    Typography,
    FormControl,
    Select,
    MenuItem,
    Button,
    TextField,
} from "@material-ui/core";

import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import FindPersonsRequest from "../../server-api/persons/FindPersonsRequest";
import commonStore from "src/stores/CommonStore";

/*
** Component SearchForm
** - props
** -- handleFind - функция родительского компонента реагирует на нажатие кнопки поиск
*/

// #TODO использовать функции реализованные сверху
export interface ISearchFields {
    surname?: string;
    first_name?: string;
    middle_name?: string;
    department_id?: string;
    organization_id?: string;
}

interface ISearchFormProps extends WithStyles<typeof styles> {
    handleSearchPeople: (e: FindPersonsRequest) => void;
}

interface IState {
    surname: string;
    firstName: string;
    middleName: string;
    specializationId: string;
    organizationId: string;
}

const styles = (theme: Theme) => createStyles({
    root: {
        backgroundColor: "#017BC3",
        padding: "55px 70px 46px",
        color: "#FFF",
        marginBottom: 35,
    },
    row: {
        marginBottom: 35,
    },
});

class SearchForm extends React.Component<ISearchFormProps, IState> {

    public state: IState = {
        surname: "",
        firstName: "",
        middleName: "",
        specializationId: SearchForm.SPECIALIZATION_NONE_VALUE,
        organizationId: "",
    };

    public render() {
        const { classes } = this.props;
        const { surname, firstName, middleName, specializationId, organizationId } = this.state;
        return (
            <Grid container className={classes.root}>
                <Grid item xs={12}>
                    <Typography component="h1" color="textPrimary" align="center" variant="h2" gutterBottom>
                        Поиск по персоналиям
                    </Typography>
                </Grid>
                <Grid
                    alignItems={"center"}
                    container
                    item
                    className={classes.row}
                    md={12}
                    lg={12}
                >
                    <Grid item xs={12} md={3} lg={3}>
                        <FormControl>
                            <TextField
                                id="surname"
                                placeholder="Фамилия"
                                value={surname}
                                onChange={(event: any) =>
                                    this.setState({ surname: event.target.value })
                                }
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} md={3} lg={3}>
                        <FormControl>
                            <TextField
                                id="name"
                                placeholder="Имя"
                                value={firstName}
                                onChange={(event: any) =>
                                    this.setState({ firstName: event.target.value })
                                }
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} md={3} lg={3}>
                        <FormControl>
                            <TextField
                                id="lastname"
                                placeholder="Отчество"
                                value={middleName}
                                onChange={(event: any) =>
                                    this.setState({ middleName: event.target.value })
                                }
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} md={3} lg={3}>
                        <FormControl>
                            <Select
                                autoWidth
                                native={false}
                                value={specializationId}
                                onChange={(event: any) =>
                                    this.setState({ specializationId: event.target.value })
                                }
                            >
                                <MenuItem value={SearchForm.SPECIALIZATION_NONE_VALUE}>
                                    <em>None</em>
                                </MenuItem>
                                {commonStore.specializationList.map((specialization) => {
                                    return (
                                        <MenuItem
                                            key={specialization.id}
                                            value={specialization.id}>
                                            {specialization.display_text}
                                        </MenuItem>);
                                })}
                            </Select>
                        </FormControl>
                    </Grid>
                </Grid>
                <Grid
                    container
                    item
                    className={classes.row}
                    xs={12} md={12} lg={12}
                >
                    <Grid item xs={12} md={12} lg={6}>
                        <FormControl>
                            <TextField
                                id="org"
                                placeholder="Полное название организации"
                                style={{
                                    width: 230,
                                }}
                                value={organizationId}
                                onChange={(event: any) =>
                                    this.setState({ organizationId: event.target.value })
                                }
                            />
                        </FormControl>
                    </Grid>
                </Grid>
                <Grid
                    container
                    item
                    alignContent={"center"}
                    xs={12} md={12} lg={12}>
                    <Button
                        onClick={this._handleSearchPeolple}
                        color="primary"
                        variant="contained"
                    >
                        Найти
                        </Button>
                </Grid>
            </Grid>
        );
    }

    // Private constants

    private static SPECIALIZATION_NONE_VALUE: string = "";

    private _handleSearchPeolple = () => {
        const { surname, firstName, middleName, specializationId, organizationId } = this.state;
        const request = new FindPersonsRequest();
        if (surname) {
            request.surname = surname;
        }
        if (firstName) {
            request.first_name = firstName;
        }
        if (middleName) {
            request.middle_name = middleName;
        }
        if (specializationId !== SearchForm.SPECIALIZATION_NONE_VALUE) {
            request.specialization_id = specializationId;
        }
        if (organizationId) {
            request.organization_id = organizationId;
        }
        this.props.handleSearchPeople(request);
    }
}

export default withStyles(styles)(SearchForm);
