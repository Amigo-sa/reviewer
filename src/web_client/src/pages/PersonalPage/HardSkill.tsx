import * as React from "react";

// TODO:
// props:
// - hanle callback, process click on hard skill. send name or id of skill to parent component
// - name
// - percent value
// - id?

class HardSkill extends React.Component {
    public render() {
        return (
            <div
                style={{
                    backgroundColor: "darkkhaki",
                    width: "100px",
                    height: "20px",
                }}
            >
                HardSkill
            </div>
        );
    }
}

export default HardSkill;
