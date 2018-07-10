import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import AddUser from './components/add-user';
import UsersList from './components/users-list';

const URL = process.env.REACT_APP_USERS_SERVICE_URL || 'http://localhost:8080';

function sorter(u1, u2) {
  return u1.username.localeCompare(u2.username);
}

class App extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      username: '',
      email: '',
    };
    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }
  componentDidMount() {
    this.getUsers();
  }
  getUsers() {
    axios.get(`${URL}/users`)
      .then((res) => { this.setState(() => ({ users: res.data.data.users.sort(sorter) })); })
      .catch((err) => { console.log(err); }); // eslint-disable-line
  }
  addUser(e) {
    e.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email,
    }
    axios.post(`${URL}/users`, data)
      .then((res) => console.log(res))
      .catch((err) => console.error(err))
  }
  handleChange(e) {
    const obj = {};
    obj[e.target.name] = e.target.value;
    this.setState(() => ({...obj}));
  }
  render() {
    return (
      <div className="container">
        <div className="row">
        <div className="col-md-4">
          <br/>
          <h1>All Users</h1>
          <hr/><br/>
          <AddUser
            addUser={this.addUser}
            handleChange={this.handleChange}
            username={this.state.username}
            email={this.state.email}
          />
          <br/>
          <UsersList users={this.state.users}/>
        </div>
        </div>
      </div>
    )
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
