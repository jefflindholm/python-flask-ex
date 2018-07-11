<template>
  <div class="container">
    <div class="row">
      <div class="col-md-4">
        <br/>
        <h1>All Users</h1>
        <hr><br>
        <add-user @formSubmit="handleSubmit"></add-user>
        <br>
        <users-list :users="users"></users-list>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AddUser from './components/add-user';
import UsersList from './components/users-list';

const URL = process.env.VUE_APP_USERS_SERVICE_URL || 'http://localhost:8080';

function sorter(u1, u2) {
  return u1.username.localeCompare(u2.username);
}

export default {
  name: 'app',
  components: {
    AddUser,
    UsersList,
  },
  data() {
    return {
      users: [],
    };
  },
  mounted() {
    axios.get(`${URL}/users`)
      .then((res) => { this.users = res.data.data.users.sort(sorter); })
      .catch((err) => { console.log(err); }); // eslint-disable-line no-console
  },
  methods: {
    handleSubmit(data) {
      axios.post(`${URL}/users`, data)
        .then(() => {
          this.getUsers();
          this.setState(() => ({ username: '', email: '' }))
        })
        .catch((err) => console.error(err)); // eslint-disable-line no-console
    },
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}
</style>
