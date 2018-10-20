import * as React from "react";
import { Link } from "react-router-dom";
import Grid from "@material-ui/core/Grid";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
// import Typography from "@material-ui/core/Typography";
import {
    Input,
    Badge,
    Menu,
    MenuItem,
} from "@material-ui/core";
import { fade } from "@material-ui/core/styles/colorManipulator";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";
import SearchIcon from "@material-ui/icons/Search";
import AccountCircle from "@material-ui/icons/AccountCircle";
import MailIcon from "@material-ui/icons/Mail";
import NotificationsIcon from "@material-ui/icons/Notifications";
import MoreIcon from "@material-ui/icons/MoreVert";
import Logo from "./elements/Logo";
import HeaderMenu from "./elements/Menu";
import { observer, inject } from "mobx-react";
import { AuthStore } from "../../stores/AuthStore";
import { Button, Dialog } from "@material-ui/core";
import LoginDialog from "src/components/LoginDialog";

// #TODO определиться как лучше писать стили так или в css
// такая струкутура позволяет обновлять тему
const styles = (theme: Theme) => createStyles({
    root: {
        width: "100%",
    },
    AppBar: {
        backgroundColor: "#ccc",
    },
    grow: {
        flexGrow: 1,
    },
    menuButton: {
        marginLeft: -12,
        marginRight: 20,
    },
    title: {
        display: "none",
        [theme.breakpoints.up("sm")]: {
            display: "flex",
            flex: "1 1 auto",
        },
    },
    search: {
        position: "relative",
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        "&:hover": {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginRight: theme.spacing.unit * 2,
        marginLeft: 0,
        width: "100%",
        [theme.breakpoints.up("sm")]: {
            marginLeft: theme.spacing.unit * 3,
            width: "auto",
        },
    },
    searchIcon: {
        width: theme.spacing.unit * 9,
        height: "100%",
        position: "absolute",
        pointerEvents: "none",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },
    inputRoot: {
        color: "inherit",
        width: "100%",
    },
    inputInput: {
        paddingTop: theme.spacing.unit,
        paddingRight: theme.spacing.unit,
        paddingBottom: theme.spacing.unit,
        paddingLeft: theme.spacing.unit * 10,
        transition: theme.transitions.create("width"),
        width: "100%",
        [theme.breakpoints.up("md")]: {
            width: 200,
        },
    },
    sectionDesktop: {
        display: "none",
        [theme.breakpoints.up("md")]: {
            display: "flex",
        },
    },
    sectionMobile: {
        display: "flex",
        [theme.breakpoints.up("md")]: {
            display: "none",
        },
    },
});

interface IAuthProps {
    authStore?: AuthStore;
}

interface IProps extends WithStyles<typeof styles>, IAuthProps {
    title: string;
    size: string;
}

@inject("authStore")
@observer
class Header extends React.Component<IProps>{
    public state = {
        anchorEl: null,
        mobileMoreAnchorEl: null,
        isLoginAnchorEl: null,
    };

    get injected() {
        return this.props as IAuthProps;
    }

    private handleProfileMenuOpen = (event: any) => {
        this.setState({ anchorEl: event.currentTarget });
    }

    private handleMenuClose = () => {
        this.setState({ anchorEl: null });
        this.handleMobileMenuClose();
    }

    private handleMobileMenuOpen = (event: any) => {
        this.setState({ mobileMoreAnchorEl: event.currentTarget });
    }

    private handleMobileMenuClose = () => {
        this.setState({ mobileMoreAnchorEl: null });
    }

    private handleLoginClickOpen = (event: any) => {
        this.setState({ isLoginAnchorEl: event.currentTarget });
    }

    private handleLoginClickClose = () => {
        this.setState({ isLoginAnchorEl: null });
    }

    public render() {
        const { anchorEl, mobileMoreAnchorEl, isLoginAnchorEl } = this.state;
        const { classes, title } = this.props;
        const { authStore } = this.injected;
        const isMenuOpen = Boolean(anchorEl);
        const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);
        const isLoginOpen = Boolean(isLoginAnchorEl);

        // #TODO менюшка у пользователя
        const renderMenu = (
            <Menu
                anchorEl={anchorEl}
                anchorOrigin={{ vertical: "top", horizontal: "right" }}
                transformOrigin={{ vertical: "top", horizontal: "right" }}
                open={isMenuOpen}
                onClose={this.handleMenuClose}
            >
                <Link to={"/personal"}><MenuItem >Профиль</MenuItem></Link>
                <MenuItem >Опросы</MenuItem>
                <MenuItem >Выход</MenuItem>
            </Menu>
        );

        // #TODO мобильная менюшка, как пример
        const renderMobileMenu = (
            <Menu
                anchorEl={mobileMoreAnchorEl}
                anchorOrigin={{ vertical: "top", horizontal: "right" }}
                transformOrigin={{ vertical: "top", horizontal: "right" }}
                open={isMobileMenuOpen}
                onClose={this.handleMobileMenuClose}
            >
                <MenuItem>
                    <IconButton color="inherit">
                        <Badge badgeContent={4} color="secondary">
                            <MailIcon />
                        </Badge>
                    </IconButton>
                    <p>Messages</p>
                </MenuItem>
                <MenuItem>
                    <IconButton color="inherit">
                        <Badge badgeContent={11} color="secondary">
                            <NotificationsIcon />
                        </Badge>
                    </IconButton>
                    <p>Notifications</p>
                </MenuItem>
                <MenuItem onClick={this.handleProfileMenuOpen}>
                    <IconButton color="inherit">
                        <AccountCircle />
                    </IconButton>
                    <p>Profile</p>
                </MenuItem>
            </Menu>
        );

        return (
            <Grid
                item={true}
                xs={12}
                className={classes.root}
            >
                <AppBar position="static" className={classes.AppBar}>
                    <Toolbar>
                        <Logo title={title} />
                        {/* #TODO определение страницы на которой находишься в title
                        <Typography className={classes.title} variant="title" color="inherit" noWrap={true}>
                            {title}
                        </Typography>
                        */}
                        <HeaderMenu />
                        <div className={classes.search}>
                            <div className={classes.searchIcon}>
                                <SearchIcon />
                            </div>
                            <Input
                                placeholder="Search…"
                                disableUnderline={true}
                                classes={{
                                    root: classes.inputRoot,
                                    input: classes.inputInput,
                                }}
                            />
                        </div>
                        <div className={classes.grow} />
                        {authStore && authStore.isAuth ?
                            <>
                                {/* Вывод для дестопа */}
                                <div className={classes.sectionDesktop}>
                                    <IconButton
                                        aria-owns={isMenuOpen ? "material-appbar" : undefined}
                                        aria-haspopup="true"
                                        onClick={this.handleProfileMenuOpen}
                                        color="inherit"
                                    >
                                        <AccountCircle />
                                    </IconButton>
                                </div>
                                {/* Вывод для мобильнх устройств */}
                                <div className={classes.sectionMobile}>
                                    <IconButton
                                        aria-haspopup="true"
                                        onClick={this.handleMobileMenuOpen}
                                        color="inherit"
                                    >
                                        <MoreIcon />
                                    </IconButton>
                                </div>
                            </>
                            :
                            <>
                                <Button onClick={this.handleLoginClickOpen}>Войти</Button>
                                <Dialog
                                    open={isLoginOpen}
                                    onClose={this.handleLoginClickClose}
                                    aria-labelledby="form-dialog-title"
                                >
                                    <LoginDialog
                                        handleClose={this.handleLoginClickClose}
                                    />
                                </Dialog>
                            </>
                        }
                    </Toolbar>
                </AppBar>
                {renderMenu}
                {renderMobileMenu}
            </Grid>
        );
    }
}

export default withStyles(styles)(Header);
