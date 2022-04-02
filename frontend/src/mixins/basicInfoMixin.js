import axios from 'axios';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
  }),
  computed: {
    logoPath() {
      if (process.env.VUE_APP_ENV === 'DEV') {
        return require(`@/assets/${this.theme}/logo-dev.png`); // eslint-disable-line
      }
      return require(`@/assets/${this.theme}/logo.png`); // eslint-disable-line
    },
    getUserName() {
      if (this.userinfo) {
        if (this.userinfo.fahrtenname && this.userinfo.fahrtenname.length > 0) {
          return this.userinfo.fahrtenname;
        }
        return this.userinfo.name;
      }
      return '';
    },
  },
  methods: {
    async getZipcodeInfo(zipcode) {
      const url = `${this.API_URL}/basic/zip-code/${zipcode}/`;
      const response = await axios.get(url);
      return response.data;
    },
  },
};
