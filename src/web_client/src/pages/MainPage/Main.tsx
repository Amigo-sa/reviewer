import * as React from "react";
import Grid from "@material-ui/core/Grid";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import TextInfo from "./TextInfo";
import RatingItem from "../../elements/RatingItem";

import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";

// #TODO вынести в общую компоненту layout и использовать хеадер и футер по умолчанию
// чтобы не указывать постоянно при создании новых страниц, возможно определить шаблоны

const styles = (theme: Theme) => createStyles({
    block1: {
        backgroundColor: "#017BC3",
        display: "flex",
    },
    slide: {
        margin: "55px 100px 0 100px",
        flex: "2 1 auto",
    },
    block2: {
        flexGrow: 1,
        height: 554,
        "& h4": {
            marginBottom: "30px",
            marginTop: "50px",
        },
    },
});
class Main extends React.Component<WithStyles<typeof styles>> {
    public render() {
        const { classes } = this.props;
        return (
            <>
                <Header
                    title={"Главная"}
                    size={"big"}
                />
                <Grid container={true}>
                    <Grid item={true} xs={12} className={classes.block1}>
                        <Grid className={classes.slide}>
                            <img src="static/img/skills-color.png" alt="skills-color" />
                        </Grid>
                        <TextInfo title={"Skill for life reviewer"}>
                            <p>
                                Предназначен для сбора отзывов, проведения опросов и
                                тестирования студентов и сотрудников образовательного учреждения,
                                 в частности, применение проекта планируется в университете ИТМО.
                                Проект призван продемонстрировать подход и перспективы развития платформы
                                 Skill for life.
                            </p>
                        </TextInfo>
                    </Grid>
                </Grid>
                <Grid container={true}>
                    <Grid item={true} xs={12} className={classes.block2}>
                        <Grid className={classes.slide}>
                            <h4>Рейтинг участников</h4>
                        </Grid>
                        <Grid container={true} justify="center" spacing={16}>
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
                <Footer />
            </>
        );
    }
}

export default withStyles(styles)(Main);
