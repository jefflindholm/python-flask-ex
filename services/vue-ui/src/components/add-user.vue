<template>
  <form @submit.prevent="onSubmit">
    <div class="form-group">
      <input
        type="text"
        class="form-control input-lg"
        required
        name="username"
        placeholder="Enter a username"
        v-model="username"
      >
      <input
        type="text"
        class="form-control input-lg"
        required
        name="email"
        placeholder="Enter an email address"
        v-model="email"
      >
      <input
        type="submit"
        class="btn btn-primary btn-lg btn-block"
        value="Submit"
      >
    </div>
  </form>
</template>
<script>
export default {
  data() {
    return {
      email: '',
      username: '',
    };
  },
  methods: {
    onSubmit() {
      this.$emit('formSubmit', {
        username: this.username,
        email: this.email,
      });
    },
  },
};
</script>
