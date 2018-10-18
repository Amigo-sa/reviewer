import * as React from "react";
import { Link } from "react-router-dom";

import "./Logo.css";
interface IProps {
    title?: string;
}

class Logo extends React.Component<IProps> {
    public render() {
        const { title } = this.props;
        return (
            <Link to="/" className={"logo__link"} title={title}>
                <img src="img/logo.png" alt="logo" className={"logo__img"} />
                <div className={"logo__title"}>
                    <span className={"logo__title-main"}>Skill for life</span>
                    <span className={"logo__title-sec"}>reviewer</span>
                </div>
            </Link>
        );
    }
}
export default Logo;
