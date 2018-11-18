import * as React from "react";
import {
    Grid,
    Typography,
    // Select,
    // InputLabel,
    // MenuItem,
    LinearProgress,
} from "@material-ui/core";
import FoundPerson from "../../components/FoundPerson";

import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import Person from "../../server-api/persons/Person";

// #TODO использовать функции реализованные сверху и убрать необязательность параметров
interface ISearchProps extends WithStyles<typeof styles> {
    handleSort?: (e: any) => void;
    sort?: string;
    results: Person[];
    loading?: boolean;
}

const styles = (theme: Theme) => createStyles({
    block1: {
        backgroundColor: "#FFF",
        display: "flex",
        padding: "55px 70px 46px",
    },
    fullWidth: {
        width: "100%",
    },
});
/*
** Component SearchResult
** -- sort - переменная опередяющая сортировку
** -- handleSort -  функция родительского компонента реагирует на изменение сортировки
** -- results -  массив результатов в формате ISearchData
*/

class SearchResult extends React.Component<ISearchProps> {

    public render() {
        // #TODO функция сортировки внутри SearchStore
        const { classes, /*sort, handleSort, */results, loading } = this.props;
        console.log("Results ", results);
        return (
            <Grid container className={classes.block1}>
                <Grid container item alignItems="center">
                    <Grid item xs={12} md={4}>
                        <Typography component="h4" variant="h5" gutterBottom>
                            Результаты поиска
                            </Typography>
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Typography variant="h6">
                            Найдено совпадений: {results.length}
                        </Typography>
                    </Grid>
                    {/* <Grid item xs={12} md={4}>
                        <InputLabel htmlFor="sort">Сортировать по</InputLabel>
                        <Select
                            value={sort || "rating"}
                            onChange={handleSort}
                            inputProps={{
                                name: "sort",
                                id: "sort",
                            }}
                        >
                            <MenuItem value="rating">Рейтингу</MenuItem>
                            <MenuItem value="faculty">Фактультету</MenuItem>
                        </Select>
                    </Grid> */}
                </Grid>
                <Grid container item alignItems="center" justify="space-between">
                    {loading &&
                        <LinearProgress className={classes.fullWidth} />
                    }
                    {results &&
                        results.map((item) => {
                            return (
                                <FoundPerson
                                    key={item.id}
                                    id={item.id}
                                    isPersonPhotoExist={item.photo}
                                    firstName={item.first_name}
                                    surname={item.surname}
                                    middleName={item.middle_name}
                                    organizationName={item.organization_name}
                                    departamentName={item.department_name}
                                    specialization={item.specialization_display_text}
                                />
                            );
                        })
                    }
                </Grid>
            </Grid>
        );
    }
}

export default withStyles(styles)(SearchResult);
