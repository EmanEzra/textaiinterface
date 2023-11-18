import './header.css'
import React, {useState, useEffect} from "react";

function Header () {
    const [data, setData] = useState([{}]);
    useEffect(() => {
    fetch('/home'
    ).then(res => res.json()
    ).then(data => {
      setData(data);
      console.log(data);
    })
  }, []);
    return (
        <div className="hello-world">
        {
          (typeof data.members === 'undefined') ? (
              <p>Loading...</p>
          ) : (
              data.members.map((member, i) => (
                <p key={i}>{member}</p>
              ))
          )
        }
      </div>
    )
}

export default Header