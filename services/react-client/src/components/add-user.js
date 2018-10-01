import React from 'react';

const AddUser = ({ addUser, handleChange, username, email }) => {
  return (
    <form onSubmit={(event) => addUser(event)}>
      <div className="field">
        <input
          value={username}
          type="text"
          className="input is-large"
          name="username"
          placeholder="Enter username"
          onChange={handleChange}
          required/>
      </div>
      <div className="field">
        <input
          value={email}
          type="text"
          className="input is-large"
          name="email"
          placeholder="Enter email"
          onChange={handleChange}
          required/>
      </div>
      <div>
        <input type="submit" value="Submit" className="button is-primary is-large is-fullwidth"/>
      </div>
    </form>
  );
};
export default AddUser;
