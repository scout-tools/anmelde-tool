<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Haus / Lagerplatz hinzufügen</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="data.name"
                  autofocus
                  :counter="20"
                  :error-messages="nameErrors"
                  label="Name der Schlafstätte"
                  required
                  prepend-icon="mdi-earth"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Gib hier den Namen der Schlafstätte ein.' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="8">
                <v-text-field
                  v-model="data.description"
                  :counter="100"
                  :error-messages="descriptionErrors"
                  label="Beschreibung der Schlafstätte"
                  prepend-icon="mdi-card-text"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{
                          'Worum handelt es sich (z.B. Jugendherberge' +
                          ', Stammesheim, Bruchbude etc.)'
                        }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
            <v-subheader class="my-0"> Anzahl Schlafplätze </v-subheader>
            <v-divider class="my-0" />
            <v-row>
              <v-col cols="12" sm="4" md="3">
                <v-text-field
                  v-model="data.capacity"
                  :error-messages="capacityError"
                  label="Im Haus"
                  prepend-icon="mdi-home"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{
                          'Schlafplätze drinnen, in Betten oder auf dem Boden.'
                        }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="4" md="3">
                <v-text-field
                  v-model="data.capacity"
                  :error-messages="capacityError"
                  label="Zeltplatz"
                  prepend-icon="mdi-tent"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ ' Schlafplätze draußen.' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="4" md="3">
                <v-text-field
                  v-model="data.capacity"
                  :error-messages="capacityError"
                  label="Im Haus (Corona)"
                  required
                  prepend-icon="mdi-virus"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{
                          'Wie viele Schlafplätze hattet ihr im September 2020 drinnen.'
                        }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="4" md="3">
                <v-text-field
                  v-model="data.capacity"
                  :error-messages="capacityError"
                  label="Zeltplatz (Corona)"
                  required
                  prepend-icon="mdi-virus"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{
                          'Wie viele Schlafplätze hattet ihr im September 2020 draußen'
                        }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
            <v-subheader class="my-0"> Adresse </v-subheader>
            <v-divider class="my-0" />
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="data.address"
                  :error-messages="addressErrors"
                  label="Straße und Hausnummer"
                  prepend-icon="mdi-map-marker"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'genaue Adresse der Schlafstätte' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <zip-code-field
                  :counter="5"
                  :error-messages="zipCodeErrors"
                  label="Stadt/Postleitzahl"
                  required
                  @blur="$v.data.zipCode.$touch()"
                />
              </v-col>
            </v-row>
            <v-subheader class="my-0"> Kosten </v-subheader>
            <v-divider class="my-0" />
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="data.address"
                  :error-messages="addressErrors"
                  label="Kosten pro Person"
                  prepend-icon="mdi-currency-eur"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Kosten pro Person pro Nacht' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="data.address"
                  :error-messages="addressErrors"
                  label="Fixkosten"
                  prepend-icon="mdi-currency-eur"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Gib hier die Fixkosten ein, die für ein ' +
                        'Wochenende entstehen (Strom, Miete, etc.).' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col>
                <v-switch
                  v-model="switch1"
                  label="Ich kenne keine Preisliste "
                ></v-switch>
              </v-col>
            </v-row>
            <v-subheader class="my-0"> Kontakt Haus-/Zeltplatzvermietung </v-subheader>
            <v-divider class="my-0" />
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  prepend-icon="mdi-account"
                  v-model="data.contactName"
                  :error-messages="contactNameErrors"
                  label="Name der Kontaktperson"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Name der Kontaktperson' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  prepend-icon="mdi-at"
                  v-model="data.contactEmail"
                  :error-messages="contactEmailErrors"
                  label="E-Mail"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'E-Mail der Kontaktperson' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  prepend-icon="mdi-phone"
                  v-model="data.contactPhone"
                  :error-messages="contactPhoneErros"
                  label="Telefonnummer"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Telefonnummer der Kontaktperson' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <v-divider class="my-3" />
          <v-btn color="primary" @click="onClickOkay"> Speichern </v-btn>
        </v-form>
      </v-container>
      <v-divider class="my-4" />

      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Erstellen des Ortes' }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  required,
  maxLength,
  minLength,
  numeric,
} from 'vuelidate/lib/validators';
import ZipCodeField from '@/components/field/ZipCodeField.vue';
import axios from 'axios';

export default {
  props: ['isOpen'],
  components: {
    ZipCodeField,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    switch1: false,
    data: {
      name: '',
      description: '',
      address: '',
      zipCode: 6,
      contactName: '',
      contactEmail: '',
      contactPhone: '',
      capacity: null,
    },
    showError: false,
    showSuccess: false,
    timeout: 7000,
  }),
  validations: {
    data: {
      name: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(20),
      },
      description: {
        maxLength: maxLength(100),
      },
      address: {
        required,
        maxLength: maxLength(30),
      },
      zipCode: {
        required,
        numeric,
      },
      contactName: {
        maxLength: maxLength(30),
      },
      contactEmail: {
        maxLength: maxLength(30),
      },
      contactPhone: {
        maxLength: maxLength(30),
      },
    },
  },
  computed: {
    capacityError() {
      return [];
    },
    contactNameErrors() {
      return [];
    },
    contactPhoneErros() {
      return [];
    },
    contactEmailErrors() {
      return [];
    },
    nameErrors() {
      const errors = [];
      if (!this.$v.data.name.$dirty) return errors;
      if (!this.$v.data.name.required) {
        errors.push('Name is required.');
      }
      if (!this.$v.data.name.maxLength) {
        errors.push('Name must be at most 20 characters long');
      }
      return errors;
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.data.description.$dirty) return errors;
      if (!this.$v.data.description.maxLength) {
        errors.push('description must be at most 100 characters long');
      }
      return errors;
    },
    addressErrors() {
      const errors = [];
      if (!this.$v.data.address.$dirty) return errors;
      if (!this.$v.data.address.required) {
        errors.push('Adresse is required.');
      }
      if (!this.$v.data.address.maxLength) {
        errors.push('Adresse must be at most 20 characters long');
      }
      return errors;
    },
    cityErrors() {
      const errors = [];
      if (!this.$v.data.city.$dirty) return errors;
      if (!this.$v.data.city.required) {
        errors.push('Stadt is required.');
      }
      if (!this.$v.data.city.maxLength) {
        errors.push('Stadt must be at most 30 characters long');
      }
      return errors;
    },
    zipCodeErrors() {
      const errors = [];
      if (!this.$v.data.zipCode.$dirty) return errors;
      if (!this.$v.data.zipCode.required) {
        errors.push('PLZ is required.');
      }
      if (!this.$v.data.zipCode.numeric) {
        errors.push('PLZ muss eine Zahl sein.');
      }
      if (!this.$v.data.zipCode.minLength || !this.$v.data.zipCode.maxLength) {
        errors.push('PLZ muss eine 5-stellige Zahl sein.');
      }
      return errors;
    },
  },
  methods: {
    openDialog() {
      this.active = true;
    },
    closeDialog() {
      this.active = false;
      this.$v.$reset();
      Object.keys(this.data).forEach((key) => {
        this.data[key] = '';
      });
      this.$emit('close');
    },
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    onClickOkay() {
      this.validate();
      if (this.valid) {
        try {
          this.callCreateEventLocationPost();
          this.closeDialog();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    async callCreateEventLocationPost() {
      await axios.post(`${this.API_URL}basic/event-location/`, this.data);
    },
  },
};
</script>
