<template>
  <div class="arrival-card-container">
      <div class="arrival-card-image">
        <div class="arrival-card-info">
          <div class="diagonal diagonal-1"></div>
          <div class="diagonal diagonal-2"></div>
          <div class="diagonal diagonal-3"></div>
          <div class="diagonal diagonal-4"></div>
          <div class="firstname fixed left">
            {{trip.user_info.firstname}}
          </div>
          <div class="lastname fixed left">
            {{trip.user_info.lastname}}
          </div>
          <div class="nationality fixed left">
            {{trip.user_info.nationality | nationality}}
          </div>
          <div class="firstname_2 fixed left">
            {{trip.user_info.firstname}}
          </div>
          <div class="lastname_2 fixed left">
            {{trip.user_info.lastname}}
          </div>
          <div class="nationality_2 fixed left">
            {{trip.user_info.nationality | nationality}}
          </div>
          <div class="passport_number fixed left">
            {{trip.user_info.passport_number}}
          </div>
          <div class="foreign_address fixed left">
            {{trip.foreign_address}}
          </div>
          <div class="date_of_birth date_of_birth_day_1 fixed left">
            {{trip.user_info.date_of_birth | day}}
          </div>
          <div class="date_of_birth date_of_birth_day_2 fixed left">
            {{trip.user_info.date_of_birth | day}}
          </div>
          <div class="date_of_birth date_of_birth_month_1 fixed left">
            {{trip.user_info.date_of_birth | month}}
          </div>
          <div class="date_of_birth date_of_birth_month_2 fixed left">
            {{trip.user_info.date_of_birth | month}}
          </div>
          <div class="date_of_birth date_of_birth_year_1 fixed left">
            {{trip.user_info.date_of_birth | year}}
          </div>
          <div class="date_of_birth date_of_birth_year_2 fixed left">
            {{trip.user_info.date_of_birth | year}}
          </div>
          <div class="flight_number_to fixed">
            {{trip.flight_number_to}}
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  import moment from 'moment'
  import countries from './country.json'
  export default {
    data () {
      return {
        trip:{}
      }
    },
    beforeMount () {
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
        return moment(val, 'YYYY-MM-DDTHH:mm:ss').format('DD');
      },
      month: (val) => {
        return moment(val, 'YYYY-MM-DDTHH:mm:ss').format('MM');
      },
      year: (val) => {
        return moment(val, 'YYYY-MM-DDTHH:mm:ss').format('YY');
      },
      nationality: (val) => {
        for (let c of countries.result) {
          if (val == c.alpha2Code) {
            return c.demonym;
          }
        }
        return val;
      }
    }
  }
</script>
<style scoped lang="sass">
.arrival-card-container {
  font-size: 0.9em;
	width: 740px;
	height: 334px;
	.arrival-card-image {
		background: url('/public/img/jp_front.jpg') no-repeat left	top;
		background-size: cover;
		width: 100%;
		height: 100%;
		.arrival-card-info {
      div {
        margin-top: -41px;
        margin-left: 9px;
      }
			.diagonal{
			width:50px;
			height:30px;
			position:absolute;}

			.diagonal:after{
			content:"";
			position:absolute;
			border-top:1px solid black;
			width:50px;
			top: 20px;
			transform: rotate(-20deg);
			transform-origin: 0% 0%;
			}
			.fixed {
				position:absolute;
			}
			.diagonal-1 {
				left: 120px;
				top: 150px;
			}
			.diagonal-2 {
				left: 210px;
				top: 150px;
			}
			.diagonal-3 {
				left: 370px;
	 			top: 128px;
			}
			.diagonal-4 {
				top: 128px;
				left: 490px;
			}
			.firstname {
				left: 140px;
				top: 190px;
			}
			.lastname {
				left: 140px;
    		top: 170px;
			}
			.nationality {
				left: 120px;
				top: 210px;
			}
			.firstname_2 {
				left: 505px;
    		top: 152px;
			}
			.lastname_2 {
				left: 385px;
    		top: 152px;
			}
			.nationality_2 {
				left: 360px;
    		top: 175px;
			}
			.passport_number {
				top: 220px;
				left: 355px;
			}
			.flight_number_to {
				top: 220px;
				left: 550px;
			}
			.foreign_address {
				left: 350px;
				top: 285px;
			}
			.date_of_birth {
		    width: 27px;
		    max-height: 20px;
		    overflow: hidden;
			}
			.date_of_birth_day_1 {
				left: 215px;
				top: 213px;
				letter-spacing: 2px;
			}
			.date_of_birth_day_2 {
				left: 525px;
    		top: 178px;
				letter-spacing: 5px;
			}
			.date_of_birth_month_1 {
				left: 238px;
				top: 213px;
				letter-spacing: 2px;
			}
			.date_of_birth_month_2 {
				left: 563px;
    		top: 178px;
				letter-spacing: 5px;
			}
			.date_of_birth_year_1 {
				left: 261px;
				top: 213px;
				letter-spacing: 2px;
			}
			.date_of_birth_year_2 {
				left: 603px;
    		top: 178px;
				letter-spacing: 5px;
			}
		}
	}
}
</style>
