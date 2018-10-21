
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

/*
** Component SearchForm
** - props
** -- handleFind - функция родительского компонента реагирует на нажатие кнопки поиск
*/

// #TODO использовать функции реализованные сверху
export interface ISearchFields {
    surname: string;
    name: string;
    lastname: string;
    category: string;
    org: string;
}
interface ISearchFormProps extends WithStyles<typeof styles> {
    handleFind: (e: ISearchFields) => void;
}

const styles = (theme: Theme) => createStyles({
    root: {
        backgroundColor: "#017BC3",
    },
});

class SearchForm extends React.Component<ISearchFormProps> {

    public state = {
        surname: "",
        name: "",
        lastname: "",
        category: "",
        org: "",
    };

    public handleFind() {
        const { handleFind } = this.props;
        handleFind(this.state);
    }
    public handleChange = (name: string) => (event: any) => {
        this.setState({
            [name]: event.target.value,
        });
    }

    public render() {
        const { classes } = this.props;
        const { surname, name, lastname, category, org } = this.state;
        return (
            <Grid container={true} className={classes.root}>
                <Grid item={true} xs={12}>
                    <Typography component="h1" color="textPrimary" align="center" variant="h2" gutterBottom={true}>
                        Поиск по персоналиям
                    </Typography>
                </Grid>
                <Grid
                    alignItems={"center"}
                    container={true}
                    item={true}
                    md={12}
                    lg={12}
                >
                    <Grid item={true} xs={12} md={3} lg={3}>
                        <FormControl>
                            <TextField
                                id="surname"
                                placeholder="Фамилия"
                                value={surname}
                                onChange={this.handleChange("surname")}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item={true} xs={12} md={3} lg={3}>
                        <FormControl>
                            <TextField
                                id="name"
                                placeholder="Имя"
                                value={name}
                                onChange={this.handleChange("name")}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item={true} xs={12} md={3} lg={3}>
                        <FormControl>
                            <TextField
                                id="lastname"
                                placeholder="Отчество"
                                value={lastname}
                                onChange={this.handleChange("lastname")}
                            />
                        </FormControl>
                    </Grid>
                    <Grid item={true} xs={12} md={3} lg={3}>
                        <FormControl>
                            <Select
                                value={category}
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
                <Grid container={true} item={true} xs={12} md={12} lg={12}>
                    <Grid item={true} xs={12} md={12} lg={6}>
                        <FormControl>
                            <TextField
                                id="org"
                                placeholder="Полное название организации"
                                value={org}
                                onChange={this.handleChange("org")}
                            />
                        </FormControl>
                    </Grid>
                </Grid>
                <Grid container={true} item={true} xs={12} md={12} lg={12}>
                    <Button
                        onClick={this.handleFind}
                    >
                        Найти
                        </Button>
                </Grid>
            </Grid>
        );
    }
}

export default withStyles(styles)(SearchForm);
