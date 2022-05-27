<template>
  <v-container fluid class="mt-12" style="min-height: 90vh;">
    <v-layout fill-height>
    <v-row>
      <v-col cols="3" class="mt-3 pa-0 max-width" style="background:#f5f5f5;">
        <v-list style="background:#f5f5f5;">
          <template v-for="(link, i) in links">
          <v-list-group
            :value="false"
            :prepend-icon="link.icon"
             :key="i"
          >
            <template v-slot:activator>
              <v-list-item-title>{{ link.name }}</v-list-item-title>
            </template>

            <v-list-item
              v-for="(messageLink, i) in link.items"
              :key="i"
              link
              :to="messageLink.link"
            >
              <v-list-item-title v-text="messageLink.name"> </v-list-item-title>

              <v-list-item-icon>
                <v-icon v-text="messageLink.icon"></v-icon>
              </v-list-item-icon>
            </v-list-item>
          </v-list-group>
            <v-divider  :key="`div-${i}`"/>
          </template>
        </v-list>
      </v-col>
      <v-col cols="9">
        <router-view class="ma-3"></router-view>
      </v-col>
    </v-row>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import apiCallsMixin from '@/mixins/apiCallsMixin';

// import MessageMain from './message/Main.vue';

export default {
  components: {
    // MessageMain,
  },
  mixins: [apiCallsMixin],
  computed: {
    ...mapGetters([]),
    eventId() {
      return this.$route.params.id;
    },
  },
  data() {
    return {
      tab: 1,
      eventOverview: [],
      hasParticipantsPersonal: false,
      hasSubscribeWorkshop: false,
      hasAttributes: false,
      links: [
        {
          name: 'Nachrichten',
          icon: 'mdi-message',
          items: [
            {
              name: 'Liste',
              icon: 'mdi-format-list-bulleted',
              link: '/masterData/message-list',
            },
          ],
        },
        {
          name: 'Themes',
          icon: 'mdi-palette',
          items: [
            {
              name: 'Liste',
              icon: 'mdi-format-list-bulleted',
              link: '/masterData/theme-list',
            },
          ],
        },
      ],
    };
  },
  methods: {
    getData() {},
    loadData() {
      this.getData();
    },
  },
  created() {
    this.loadData();
  },
};
</script>

<style scoped>
.max-width {
  max-width: 300px !important;
}
</style>
