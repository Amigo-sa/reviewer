
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
    handleSearchPeolple: (e: FindPersonsRequest) => void;
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

class SearchForm extends React.Component<ISearchFormProps> {

    public state = {
        surname: "",
        first_name: "",
        middle_name: "",
        department_id: "",
        organization_id: "",
    };

    public handleSearchPeolple = () => {
        const { handleSearchPeolple } = this.props;
        const { surname, first_name, middle_name, department_id, organization_id } = this.state;
        const request = new FindPersonsRequest();
        if (surname) {
            request.surname = surname;
        }
        if (first_name) {
            request.first_name = first_name;
        }
        if (middle_name) {
            request.middle_name = middle_name;
        }
        if (department_id) {
            request.department_id = department_id;
        }
        if (organization_id) {
            request.organization_id = organization_id;
        }
        handleSearchPeolple(request);
    }

    public handleChange = (name: string) => (event: any) => {
        this.setState({
            [name]: event.target.value,
        });
    }

    public render() {
        const { classes } = this.props;
        const { surname, first_name, middle_name, department_id, organization_id } = this.state;
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
                                onChange={this.handleChange("surname")}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} md={3} lg={3}>
                        <FormControl>
                            <TextField
                                id="name"
                                placeholder="Имя"
                                value={first_name}
                                onChange={this.handleChange("name")}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} md={3} lg={3}>
                        <FormControl>
                            <TextField
                                id="lastname"
                                placeholder="Отчество"
                                value={middle_name}
                                onChange={this.handleChange("lastname")}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} md={3} lg={3}>
                        <FormControl>
                            <Select
                                value={department_id}
                                onChange={this.handleChange("category")}
                                inputProps={{
                                    name: "category",
                                    id: "category",
                                }}
                            >
                                <MenuItem value="">Категория</MenuItem>
                                <MenuItem value="1">Категория 1</MenuItem>
                                <MenuItem value="2">Категория 2</MenuItem>
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
                                value={organization_id}
                                onChange={this.handleChange("org")}
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
                        onClick={this.handleSearchPeolple}
                        color="primary"
                        variant="contained"
                    >
                        Найти
                        </Button>
                </Grid>
            </Grid>
        );
    }
}

export default withStyles(styles)(SearchForm);
