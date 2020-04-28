<template>
  <div>
    <div id="logo-container">
      <p class="logo-top-blank"></p>
      <p id="logo">
        <span class="logo-a">A</span>
        <span class="logo-p">P</span>
        <span class="logo-i">I</span>
        <span class="logo-e">E</span>
        <span class="logo-e">E</span>
      </p>
    </div>
    <Card id="des">
      <p slot="title">Description</p>
      <p> {{description}} </p>
    </Card>
  </div>
</template>

<script>
export default {
  name: 'Description',
  data () {
    var des = this.$route.params.des
    return {
      description: des
    }
  },
  methods: {

  }
}
</script>

<style scoped>
.logo-top-blank {
  height: 100px;
}

#logo {
  text-align: center;
  margin: 0;
}

.logo-a {
  color: #EA4335;
  font-size: 80px;
  font-weight: 400;
  display: inline-block;
  width: 60px;
}

.logo-p {
  color: #34A853;
  font-size: 80px;
  font-weight: 400;
  display: inline-block;
  width: 60px;
}

.logo-i {
  color: #4285F4;
  font-size: 80px;
  font-weight: 400;
  display: inline-block;
  width: 60px;
}

.logo-e {
  color: #FBBC05;
  font-size: 80px;
  font-weight: 400;
  display: inline-block;
  width: 60px;
}

#des {
  width: 600px;
  min-height: 200px;
  margin: 20px auto 10px auto;
  color: rgb(108, 108, 108);
  font-size: 14px;
}

</style>
