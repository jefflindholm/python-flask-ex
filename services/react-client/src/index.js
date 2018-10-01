import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import './index.css';

import AddUser from './components/add-user';
import UserList from './components/user-list';

const URL = process.env.REACT_APP_USERS_SERVICE_URL|| 'http://localhost';

class App extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      username: '',
      email: '',
    };
    this.getUsers = this.getUsers.bind(this);
    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    this.getUsers();
  }

  getUsers() {
    axios.get(`${URL}/users`)
      .then(res => this.setState({ users: res.data.data.users }))
      .catch(err => console.error(err));
  }

  addUser(event) {
    event.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email,
    };
    axios.post(`${URL}/users`, data)
      .then(() => {
        this.getUsers();
        this.setState({ username: '', email: '' });
      })
      .catch(err => console.error(err));
  }

  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-one-third">
              <br/>
              <h1 className="title is-1">All Users</h1>
              <br/>
              <AddUser
                username={this.state.username}
                email={this.state.email}
                addUser={this.addUser}
                handleChange={this.handleChange}
              />
              <br/><br/>
              <UserList users={this.state.users} />
            </div>
          </div>
        </div>
      </section>
    )
  }
}
ReactDOM.render(<App />, document.getElementById('root'));
