import * as React from "react";
import SoftSkill from "./SoftSkill";

// TODO: input
// - array of soft skill objects.
// - or maybe user store?

class SoftSkills extends React.Component {
    public render() {
        return (
            <div
                style={{
                    backgroundColor: "yellow",
                    width: "466px",
                    height: "177px",
                }}
            >
                <>
                    <SoftSkill />
                    <SoftSkill />
                    <SoftSkill />
                </>
            </div>
        );
    }
}

export default SoftSkills;
