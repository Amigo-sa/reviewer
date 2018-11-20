import * as React from "react";

import {
    Grid,
    Typography,
    Paper,
} from "@material-ui/core";
import { withStyles, createStyles, WithStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles/createMuiTheme";

import { Link } from "react-router-dom";

import { ReviewSpecializationInfo } from "src/model/ReviewsStore";
import { IPersonShort } from "src/server-api/reviews/Review";
import { personUrlById } from "src/constants";

interface IProps {
    review: ReviewSpecializationInfo;
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
    dateLabel: {
        fontSize: "12px",
        fontWeight: "normal",
        textAlign: "left",
        lineHeight: "16px",
        color: "#9B9B9B",
    },
    specializationLabel: {
        fontSize: "16px",
        lineHeight: "22px",
        color: "#212529",
        textAlign: "left",
        fontStyle: "italic",
    },
});

class ReviewCard extends React.Component<WithStyles<typeof styles> & IProps> {

    public render() {
        const { classes } = this.props;
        const { review } = this.props;
        return (
            <Grid item className={classes.row} xs={12}>
                <Paper>
                    <Typography className={classes.dateLabel}>
                        {review.reviewDate.toLocaleDateString()}
                    </Typography>
                    <Typography variant="h5" component="h3">
                        {review.reviewTopic}
                    </Typography>
                    <Typography className={classes.specializationLabel}>
                        Специализация: {review.specializationDetail}
                    </Typography>
                    <Typography component="p">
                        {review.reviewDescription}
                    </Typography>
                    <Typography component="h6" align="right" variant="h6" gutterBottom>
                        {this._fio(review.reviewerName)}
                    </Typography>
                </Paper>
            </Grid>
        );
    }

    private _fio(reviewer: IPersonShort, full?: boolean) {
        return (
            <Link to={personUrlById(reviewer.id)} >
                {reviewer.surname} {reviewer.first_name} {full && reviewer.middle_name}
            </Link>
        );
    }
}

export default withStyles(styles)(ReviewCard);
