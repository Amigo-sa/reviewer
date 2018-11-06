import * as React from "react";
import {
    Paper, Grid, Avatar, Typography, Divider,
    Button, createStyles, WithStyles, Theme, withStyles,
} from "@material-ui/core";
import "typeface-roboto";
import { Link } from "react-router-dom";
import Person from "src/server-api/persons/Person";
import { inject, observer } from "mobx-react";
import { UsersStore } from "src/stores/UsersStore";
import { AuthStore } from "src/stores/AuthStore";

const styles = (theme: Theme) =>
    createStyles({
        buttonLink: {
            textTransform: "none",
        },
        divider: {
            margin: "0px 30px 0px 30px",
        },
    });

interface IProps extends WithStyles<typeof styles> {
    authStore?: AuthStore;
    usersStore?: UsersStore;
}

@inject("authStore", "usersStore")
@observer
class LeftMenu extends React.Component<IProps> {

    public state = {
        user: null,
    };

    get inject() {
        return this.props as IProps;
    }

    public componentDidMount() {
        const {
            authStore,
            usersStore,
        } = this.inject;

        if (authStore && authStore.user.uid && usersStore) {
            usersStore.get(authStore.user.uid)
                .then((user) => this.setState({ user }));
        }
    }

    public render() {
        return (
            <Paper>
                <Grid
                    container
                    direction="column">
                    <div
                        style={{
                            justifyContent: "center",
                        }}>
                        <Avatar
                            alt="icon"
                            src="/static/img/icon_min.png"
                            style={{
                                width: 108,
                                height: 108,
                                marginTop: 20,
                                marginBottom: 10,
                            }} />
                    </div>
                    <Typography
                        variant="h6"
                        style={{
                            marginLeft: 50,
                            marginRight: 50,
                            alignContent: "center",
                        }}>
                        {this._renderFio()}
                    </Typography>
                    <Divider className={this.props.classes.divider} />
                    <Button className={this.props.classes.buttonLink}>
                        <Link to={"/personal"}>
                            Мой профиль
                        </Link>
                    </Button>
                    <Button className={this.props.classes.buttonLink}>
                        Опросы
                    </Button>
                    <Button className={this.props.classes.buttonLink}>
                        Сообщения
                    </Button>
                    <Button className={this.props.classes.buttonLink}>
                        Поиск
                    </Button>
                    <Button className={this.props.classes.buttonLink}>
                        Рейтинг
                    </Button>
                    <Button className={this.props.classes.buttonLink}>
                        <Link to={"/reviews"}>
                            Отзывы
                        </Link>
                    </Button>
                    <Button className={this.props.classes.buttonLink}>
                        Настройки
                    </Button>
                    <Divider className={this.props.classes.divider} />
                    <Button
                        className={this.props.classes.buttonLink}
                        style={{
                            marginBottom: 83,
                        }}
                        href="/">
                        Выход
                    </Button>
                </Grid>
            </Paper>
        );
    }

    public _renderFio() {
        const { user } = this.state;
        if (user) {
            const uInfo = user as Person;
            return uInfo.surname + " " + uInfo.first_name + " " + uInfo.middle_name;
        }
        return;
    }
    // TODO:
    // handle buttons click and go to needed page
    // use the same technic as in Link component in ReactRouter,
    // but with Materail UI appearence
    // https://stackoverflow.com/questions/29244731/react-router-how-to-manually-invoke-link
    // https://github.com/ReactTraining/react-router/blob/master/packages/react-router-dom/modules/Link.js
}

export default withStyles(styles)(LeftMenu);
