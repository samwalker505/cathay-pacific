<template lang="jade">
  div.arrival_card_container {{trip}}
    div.arrival_card_image
    div.arrival_card_info
      div.lastname.fixed.left {{trip.user_info.firstname}}
      div.firstname.fixed.left {{trip.user_info.lastname}}
      div.nationality.fixed.left {{trip.user_info.nationality | nationality}}
      div.passport_number.fixed.left K12345678
      div.visa_number.fixed.left
      div.foreign_address.fixed.left Thanon Ram Inthra 97, Khan Na Yao, Bangkok 10230
      div.date_of_birth_day.fixed 30
      div.date_of_birth_month.fixed 01
      div.date_of_birth_year.fixed 1995
      div.flight_number_to.fixed CX 2016
</template>

<script>
  import countries from '~public/countries.json'
  export default {
    data () {
      return {
        trip:{}
      }
    },
    created () {
      const accessToken = this.$route.query.access_token;
      const tripId = this.$route.params.trip_id;
      console.log(accessToken);
      console.log(tripId);
      this.$http.get(`/api/v1/trips/${tripId}?access_token=${accessToken}`).then((response) => {
        console.log(response.body);
        this.trip = response.body;
      }, (response) => {
        // error callback
        console.error(response);
      });
    },
    filters: {
      day: (val) => {
        console.log(val);
        return ;
      },
      nationality: (val) => {
        console.log(val);
        console.log(countries);
      }
    }
  }
</script>
<style scoped>
  .left {
    left: 125px;
  }
  .fixed {
    letter-spacing: 6px;
    position: absolute;
    width: 200px;
  }
  .lastname {
    top: 83px;
  }
  .firstname {
    top:116px;
  }
  .nationality {
    top: 146px;
  }
  .passport_number {
    top: 176px;
  }
  .visa_number {
    top: 206px;
  }
  .foreign_address {
    top: 242px;
    width: 420px;
    line-height: 21px;
  }
  .date_of_birth_day {
    left: 385px;
    top: 179px;
  }
  .date_of_birth_month {
    top: 179px;
    left: 423px;
  }
  .date_of_birth_year {
    top: 179px;
    left:463px;
  }
  .flight_number_to {
    top: 100px;
    left: 540px;
  }
  .arrival_card_container {
    position: relative;
  }
  .arrival_card_image {
    position: absolute;
    background-image: url('/public/img/thai_front.jpg');
    background-size: cover;
    width: 740px;
    height: 329px;
  }
  .arrival_card_info {
    position: absolute;
  }

</style>
