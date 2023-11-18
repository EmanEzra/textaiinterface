import React, {useState} from "react";
import "./KerasInputLayer.css"

function KerasInputLayer (props) {

    const tableItems = props.tableItems;
    return (
        <div className="input-layer">
            <table>
                {tableItems.map(row => (
                    <tr>
                      {row.map(cell => (
                          <td>{cell}</td>
                      ))}
                    </tr>
                ))}
            </table>

      </div>
    )
}

export default KerasInputLayer