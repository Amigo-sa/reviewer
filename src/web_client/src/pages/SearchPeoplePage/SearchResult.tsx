
import * as React from "react";
import {
    Grid,
    Typography,
    FormControl,
    Select,
    InputLabel,
    MenuItem,
} from "@material-ui/core";
import RatingItem from "../../elements/RatingItem";

import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import { ISearchData } from "src/stores/SearchStore";

// #TODO использовать функции реализованные сверху и убрать необязательность параметров
interface ISearchProps extends WithStyles<typeof styles> {
    handleSort?: (e: any) => void;
    sort?: string;
    results: ISearchData[];
}

const styles = (theme: Theme) => createStyles({
    block1: {
        backgroundColor: "#FFF",
        display: "flex",
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
        const { classes, sort, handleSort, results } = this.props;
        return (
            <Grid container={true}>
                <Grid item={true} xs={12} className={classes.block1}>
                    <Grid>
                        <Typography component="h4" variant="headline" gutterBottom={true}>
                            Результаты поиска
                        </Typography>
                        <Typography variant="title">
                            Найдено совпадений: 45
                            </Typography>
                        <FormControl>
                            <InputLabel htmlFor="sort">Сортировать по</InputLabel>
                            <Select
                                value={sort}
                                onChange={handleSort}
                                inputProps={{
                                    name: "sort",
                                    id: "sort",
                                }}
                            >
                                <MenuItem value="rating">Рейтингу</MenuItem>
                                <MenuItem value="faculty">Фактультету</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid container={true} justify="center" spacing={16}>
                        {results}
                        <RatingItem
                            img={"static/img/img-1.png"}
                            fullname={"Петров Иван Алексеевич"}
                            university={"ITMO"}
                            course={5}
                            rating={"9,5"}
                        />
                        <RatingItem
                            img={"static/img/img-2.png"}
                            fullname={"Иванов Юрий Петрович"}
                            university={"ITMO"}
                            course={5}
                            rating={"8,5"}
                        />
                        <RatingItem
                            img={"static/img/img-3.png"}
                            fullname={"Петров Иван Алексеевич"}
                            university={"ITMO"}
                            course={5}
                            rating={"6,5"}
                        />
                        <RatingItem
                            img={"static/img/img-1.png"}
                            fullname={"Иванов Юрий Петрович"}
                            university={"ITMO"}
                            course={5}
                            rating={"8,5"}
                        />
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default withStyles(styles)(SearchResult);
