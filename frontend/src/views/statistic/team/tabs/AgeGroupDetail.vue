<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <RegistrationFilter
                :eventId="eventId"
                @onFilterSelected="onFilterSelected"
              />
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-card flat v-if="!loading">
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Alter</th>
                <th class="text-left">Männlich</th>
                <th class="text-left">Weiblich</th>
                <th class="text-left">Führung</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>6 und Jünger</td>
                <td> {{ data['p6-MNo'] }} </td>
                <td> {{ data['p6-FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>7</td>
                <td> {{ data['p07MNo'] }} </td>
                <td> {{ data['p07FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>8</td>
                <td> {{ data['p08MNo'] }} </td>
                <td> {{ data['p08FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>9</td>
                <td> {{ data['p09MNo'] }} </td>
                <td> {{ data['p09FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>10</td>
                <td> {{ data['p10MNo'] }} </td>
                <td> {{ data['p10FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>11</td>
                <td> {{ data['p11MNo'] }} </td>
                <td> {{ data['p11FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>12</td>
                <td> {{ data['p12MNo'] }} </td>
                <td> {{ data['p12FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>13</td>
                <td> {{ data['p13MNo'] }} </td>
                <td> {{ data['p13FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>14</td>
                <td> {{ data['p14MNo'] }} </td>
                <td> {{ data['p14FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>15</td>
                <td> {{ data['p15MNo'] }} </td>
                <td> {{ data['p15FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>16</td>
                <td> {{ data['p16MNo'] }} </td>
                <td> {{ data['p16FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>17</td>
                <td> {{ data['p17MNo'] }} </td>
                <td> {{ data['p17FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>18</td>
                <td> {{ data['p18MNo'] }} </td>
                <td> {{ data['p18FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>19</td>
                <td> {{ data['p19MNo'] }} </td>
                <td> {{ data['p19FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>20</td>
                <td> {{ data['p20MNo'] }} </td>
                <td> {{ data['p20FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>21</td>
                <td> {{ data['p21MNo'] }} </td>
                <td> {{ data['p21FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>22</td>
                <td> {{ data['p22MNo'] }} </td>
                <td> {{ data['p22FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>23</td>
                <td> {{ data['p23MNo'] }} </td>
                <td> {{ data['p23FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>24</td>
                <td> {{ data['p24MNo'] }} </td>
                <td> {{ data['p24FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>25</td>
                <td> {{ data['p25MNo'] }} </td>
                <td> {{ data['p25FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>26</td>
                <td> {{ data['p26MNo'] }} </td>
                <td> {{ data['p26FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>27 und Älter</td>
                <td> {{ data['p26+MNo'] }} </td>
                <td> {{ data['p26+FNo'] }} </td>
                <td>Nein</td>
              </tr>
              <tr>
                <td>Unter 16</td>
                <td> {{ data['p16-MYes'] }} </td>
                <td> {{ data['p16-FYes'] }} </td>
                <td>Ja</td>
              </tr>
              <tr>
                <td>16-17</td>
                <td> {{ data['p16-17MYes'] }} </td>
                <td> {{ data['p16-17FYes'] }} </td>
                <td>Ja</td>
              </tr>
              <tr>
                <td>18-26</td>
                <td> {{ data['p18-26MYes'] }} </td>
                <td> {{ data['p18-26FYes'] }} </td>
                <td>Ja</td>
              </tr>
              <tr>
                <td>27-44</td>
                <td> {{ data['p27-44MYes'] }} </td>
                <td> {{ data['p27-44FYes'] }} </td>
                <td>Ja</td>
              </tr>
              <tr>
                <td>45 und Älter</td>
                <td> {{ data['p45+MYes'] }} </td>
                <td> {{ data['p45+FYes'] }} </td>
                <td>Ja</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card>
      <v-card v-else flat>
        <div class="text-center ma-5">
          <p>Lade Daten ...</p>
          <v-progress-circular
            :size="80"
            :width="10"
            class="ma-5"
            color="primary"
            indeterminate
          />
          <p>Bitte hab etwas Geduld.</p>
        </div>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import RegistrationFilter from '@/components/common/RegistrationFilter.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    RegistrationFilter,
  },
  data: () => ({
    data: [],
    mapping: {
      woelfling: 'Wölfling (bis 12)',
      pfadfinder: 'Pfadfinder (13-17)',
      rover: 'Rover (18-24)',
      altRover: 'Altrover (25+)',
    },
    loading: false,
  }),
  methods: {
    getString(key) {
      return this.mapping[key];
    },
    getData(params) {
      this.loading = true;

      this.getEventAgeGroupsDetail(this.eventId, params)
        .then((result) => {
          this.data = result.data; //eslint-disable-line
          debugger;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected(params) {
      this.getData(params);
    },
  },
  created() {
    const param = new URLSearchParams();
    param.append('confirmed', 'true');
    this.getData(param);
  },
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    ageGroups() {
      if (this.data) {
        return this.data;
      }
      return [];
    },
    options() {
      return {
        chart: {
          type: 'bar',
          height: 500,
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            horizontal: true,
          },
        },
        dataLabels: {
          enabled: false,
        },
        xaxis: {
          categories: Object.values(this.mapping),
        },
      };
    },
    series() {
      return [
        {
          name: 'Personen',
          data: Object.keys(this.mapping).map((item) => {
            if (this.ageGroups && this.ageGroups.length === 0) {
              return 0;
            }
            return this.ageGroups[item];
          }),
        },
      ];
    },
  },
};
</script>
