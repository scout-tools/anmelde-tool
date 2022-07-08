<template>
  <v-card class="mx-auto" :color="color" dark>
    <v-container fluid>
      <v-row align="center" justify="center" v-if="!isLoading">
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title style="word-break: break-word">
              {{ data.header }}
            </v-list-item-title>
            <v-list-item-subtitle style="word-break: break-word">
              {{ data.subheader }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <div v-if="data.fieldType==='card'">
          <v-card-text>
            <v-row align="center">
              <v-col class="display-3" cols="12">
                {{ result }}
              </v-col>
            </v-row>
            <v-row align="center">
              <v-col cols="12">
                {{ data.dataOneName }}
              </v-col>
            </v-row>
          </v-card-text>
        </div>
        <div v-else-if="data.fieldType==='list'">
          <v-list-item dense v-for="(item, index) in result" :key="index">
            <v-list-item-icon>
              <v-icon>mdi-account-group</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-subtitle
                  class="font-weight-bold"
                  v-if="data.rankField === 'updatedAt'">
                {{ formatData(item) }}
              </v-list-item-subtitle>
              <v-list-item-subtitle
                  class="font-weight-bold"
                  v-if="data.rankField === 'participantCount'">
                {{ item.count }}
              </v-list-item-subtitle>
              <v-list-item-subtitle>
                {{
                  `${item.scoutOrganisation.name} (${item.scoutOrganisation.bund})`
                }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </div>
      </v-row>
      <v-row class="ma-3" align="center" justify="center" v-else>
        <v-progress-circular
            :size="80"
            :width="10"
            class="ma-5"
            color="primary"
            indeterminate/>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import serviceMixin from '@/mixins/serviceMixin';
import moment from 'moment';

export default {
  mixins: [serviceMixin],
  props: {
    data: {
      header: {
        default: 'Überschrift',
      },
      subheader: {
        default: 'Unter Überschrift',
      },
      dataOneName: {
        default: 'Datentyp',
      },
      lookUpPath: '',
    },
    color: {
      default: 'red lighten-1',
    },
    fieldType: {
      default: 'card',
    },
    rankField: {
      default: 'rankField',
    },
  },
  data: () => ({
    isLoading: false,
    result: null,
  }),
  methods: {
    getData() {
      this.isLoading = true;
      this.getSimpleService(this.data.lookUpPath)
        .then((res) => {
          this.result = res.data;
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message: 'Leider ist ein Problem beim runterladen der Daten aufgetreten,'
                  + ' bitte probiere es später nocheinmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    formatData(item) {
      return moment(item.createdAt)
        .format('DD.MM.YYYY');
    },
  },
  created() {
    this.getData();
  },
};
</script>
