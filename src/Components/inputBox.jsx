import './InputBox.css';
import React, {useState} from "react";
import KerasInputLayer from "./KerasInputLayer";

function InputBox() {

  const [text, setText] = useState("");
  const [tableItems, setTableItems] = useState([[1, 2], [3, 4]])
  function getInputLayer(event) {
      event.preventDefault();
      fetch('/input_layer', {
          method: 'POST',
          headers: {'Content-type': 'application/json'},
          body: JSON.stringify({'text': text})
      }
        ).then(res => res.json()
        ).then(data => {
            console.log(data.members);
            setTableItems(data.members);
        })
  }
  return (
    <div className="input-box">
      <div className="input-container">
        <form onSubmit={getInputLayer}>
          <textarea value={text} onChange={e => (setText(e.target.value))}/>
            <br/>
          <button>Start</button>
        </form>
      </div>
      <KerasInputLayer tableItems={tableItems}/>
    </div>
  );
}

export default InputBox;