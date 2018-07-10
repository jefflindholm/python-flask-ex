import React from 'react';
import PropTypes from 'prop-types';

const AddUser = (props) => {
  return (
    <form onSubmit={(e) => props.addUser(e)}>
      <div className="form-group">
        <input
          name="username"
          className="form-control input-lg"
          type="text"
          required
          placeholder="Enter a username"
          value={props.username}
          onChange={props.handleChange}
        />
        <input
          name="email"
          className="form-control input-lg"
          type="text"
          required
          placeholder="Enter an email address"
          value={props.email}
          onChange={props.handleChange}
        />
        <input
          className="btn btn-primary btn-lg btn-block"
          type="submit"
          value="Submit"
        />
      </div>
    </form>
  )
};
AddUser.propTypes = {
  addUser: PropTypes.func,
  handleChange: PropTypes.func,
  email: PropTypes.string,
  username: PropTypes.string,
}

export default AddUser;
