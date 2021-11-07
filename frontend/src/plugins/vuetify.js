import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#001838',
        secondary: '#FFA300',
        success: '#e6c619',
        accent: '#fefefe',
        backgroundGrey: '#fefefe',
      },
    },
  },
});
