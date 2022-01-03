<template>
  <v-form ref="StepInvitationCode" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Lege für die Aktion einen 6-Stelligen Verifizierungscode fest. <br/>
          Dieser besteht aus Buchstaben und Zahlen und wird bei der Anmeldung
          mitgeschickt, damit sich die Anmelder verifizieren können, dass sie
          eingeladen wurden. <br/>
          Bei leerem Feld gibt es keinen Verifizierungscode.
        </span>
      </v-row>
      <v-row align="center" justify="center">
        <v-col cols="3">
          <v-text-field
            v-model="invitationCode"
            :error-messages="invitationCodeErrors"
            label="Verifizierungscode"
            required
            outlined
            filled
            prepend-inner-icon="mdi-account-key"
            @blur="validate"
          />
        </v-col>
      </v-row>

      <v-divider class="my-3"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        :valid="valid"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
        @update="postData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { alphaNum, minLength, maxLength } from 'vuelidate/lib/validators';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  name: 'StepInvitationCode',
  header: 'Verifizierungscode',
  props: ['position', 'maxPos'],
  mixins: [stepMixin, apiCallsMixin],
  components: {
    PrevNextButton,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    invitationCode: '',
  }),
  validations: {
    invitationCode: {
      alphaNum,
      minLength: minLength(4),
      maxLength: maxLength(10),
    },
  },
  computed: {
    invitationCodeErrors() {
      const errors = [];
      if (!this.$v.invitationCode.$dirty) return errors;
      if (!this.$v.invitationCode.alphaNum) {
        errors.push(
          'Der Einladungscode muss aus Zahlen und Buchstaben bestehen,',
        );
      }
      if (!this.$v.invitationCode.minLength) {
        errors.push('Minimal 4 Zeichen sind nötig.');
      }
      if (!this.$v.invitationCode.maxLength) {
        errors.push('Maximal 10 Zeichen sind möglich.');
      }
      return errors;
    },
  },
  methods: {
    postData() {
      const data = {
        invitationCode: this.invitationCode,
      };
      this.updateEvent(this.$route.params.id, data);
    },
  },
  created() {
    if (!this.$route.params.id) {
      this.$root.globalSnackbar.show({
        message: 'Leider ist ein Problem beim runterladen des Events aufgetreten, bitte probiere es später noch einmal.',
        color: 'error',
      });
      this.$router.back();
    }
    this.getEvent(this.$route.params.id)
      .then((success) => {
        this.invitationCode = success.data.invitationCode;
      })
      .catch(() => {
        this.$root.globalSnackbar.show({
          message: 'Leider ist ein Problem beim runterladen des Events aufgetreten, bitte probiere es später nocheinmal.',
          color: 'error',
        });
        this.$router.back();
      });
  },
};
</script>
