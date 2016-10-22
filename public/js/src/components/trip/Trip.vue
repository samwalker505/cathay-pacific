<template lang='jade'>
  h1 higigi
</template>
<script>
export default {
  name: 'trip',
  data () {
    return {}
  },
  created () {
    const accessToken = this.$route.query.access_token;
    const tokenId = this.$route.params.token_id;
    this.$http.get(`/api/v1/trips/${tokenId}?access_token=${accessToken}`).then((response) => {
  // success callback
      console.log(response.data)
      this.msg = response.data.main;
    }, (response) => {
      // error callback
      console.error(response);
    });

  }
}
</script>
