import React from 'react';

const UserList = ({ users }) => {
  return (
    <div>
      {
        users.map((user) => {
          return (
            <h4 className="box title is-4" key={user.id}>
            {user.username}({user.email})
            </h4>
          )
        })
      }
    </div>
  )
}

export default UserList;
