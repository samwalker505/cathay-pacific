<template lang="jade">
  div.arrival_card_container
    div.arrival_card_image
    div.arrival_card_info
      div.last_name.fixed.left Cheng
      div.first_name.fixed.left Kok Hang
      div.nationality.fixed.left Chinese
      div.passport_number.fixed.left K12345678
      div.visa_number.fixed.left
      div.foreign_address.fixed.left Thanon Ram Inthra 97, Khan Na Yao, Bangkok 10230
      div.date_of_birth_day.fixed 30
      div.date_of_birth_month.fixed 01
      div.date_of_birth_year.fixed 1995
      div.flight_number_to.fixed CX 2016
</template>

<script>
  export default {
    data () {
      return {
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
  .last_name {
    top: 83px;
  }
  .first_name {
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
