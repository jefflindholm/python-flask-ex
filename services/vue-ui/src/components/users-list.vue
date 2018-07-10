<template>
  <div>
    <h4
      v-for="user in users"
      :key="user.id"
      class="card card-body bg-light">
      {{user.username}}
    </h4>
  </div>
</template>
<script>
export default {
  props: ['users'],
}
</script>
