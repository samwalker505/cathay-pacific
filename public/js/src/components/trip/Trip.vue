<template>
</template>
<script>
export default {
  beforeCreate () {
    const accessToken = this.$route.query.access_token;
    const tripId = this.$route.params.trip_id;
    console.log(accessToken);
    console.log(tripId);
    this.$http.get(`/api/v1/trips/${tripId}?access_token=${accessToken}`).then((response) => {
      this.$router.push(`/trips/${tripId}/${response.body.destination}?access_token=${accessToken}`)
    }, (response) => {
      // error callback
      console.error(response);
    });
  }
}
</script>
