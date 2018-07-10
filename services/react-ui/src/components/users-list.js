import React from 'react';
import PropTypes from 'prop-types';

const UsersList = (props) => {
  return (
    <div>
      {
        props.users.map(user => (
          <h4
            key={user.id}
            className="card card-body bg-light">
            {user.username}
          </h4>
        ))
      }
    </div>
  )
}
UsersList.propTypes = {
  users: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number,
    username: PropTypes.string,
  })),
}
export default UsersList;
