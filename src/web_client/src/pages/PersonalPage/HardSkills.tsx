import * as React from "react";
import HardSkill from "./HardSkill";

class HardSkills extends React.Component {
    public render() {
        return (
            <div
                style={{
                    backgroundColor: "lawngreen",
                    width: "466px",
                    height: "177px",
                }}
            >
                <HardSkill />
                <HardSkill />
                <HardSkill />
            </div>
        );
    }
}

export default HardSkills;
