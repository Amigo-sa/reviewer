import * as React from "react";

// TODO:
// props:
// - hanle callback, process click on soft skill. send name or id of skill to parent component
// - name
// - count of likes
// - id?

class SoftSkill extends React.Component {
    public render() {
        return (
            <div
                style={{
                    backgroundColor: "darkgreen",
                    width: "100px",
                    height: "20px",
                }}
            >
                SoftSkill
            </div>
        );
    }
}

export default SoftSkill;
