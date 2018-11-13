import * as React from "react";
import { Grid, Typography } from "@material-ui/core";
import Profession from "./Profession";
import { Link } from "react-router-dom";
import { urlReviewNew } from "../../ReviewPage";

interface IProps {
    isCurrentPerson: boolean;
    personId: string;
    professionList: Array<[string, number]>;
}

class ProfessionsRating extends React.Component<IProps> {
    public render() {
        return (
            <Grid container item xs={12}>
                <Grid container item xs={12}
                    direction="row"
                    alignItems="baseline">
                    <Typography variant="h5">Профессия</Typography>
                    {this.props.isCurrentPerson ? null :
                        <Link to={urlReviewNew(this.props.personId)}>Оставить отзыв</Link>}
                </Grid>
                <Grid container item>
                    {this.props.professionList.map(
                        (value: [string, number], index: number, array: Array<[string, number]>) => {
                            return (<Profession key={index} name={value[0]} rate={value[1]} />);
                        })}
                </Grid>
            </Grid>
        );
    }
}

export default ProfessionsRating;
