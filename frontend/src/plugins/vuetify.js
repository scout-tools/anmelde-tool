import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: { customProperties: true },
    themes: {
      default: {
        primary: '#2196f3',
        secondary: '#009688',
        accent: '#ff5722',
        error: '#f44336',
        warning: '#ffc107',
        info: '#4CAF50',
        success: '#4caf50',
      },
      mosaik: {
        accent: '#F8D003',
        error: '#FF5252',
        info: '#4CAF50',
        primary: '#1A4B7E',
        secondary: '#F8D003',
        success: '#4CAF50',
        warning: '#f88C00',
      },
      dpvgold: {
        primary: '#001838',
        secondary: '#e6c619',
        info: '#4CAF50',
        error: '#FF5252',
        success: '#e6c619',
        accent: '#fefefe',
        backgroundGrey: '#fefefe',
        warning: '#f88C00',
      },
    },
  },
});
