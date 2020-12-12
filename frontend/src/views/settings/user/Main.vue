<template>
  <v-container>
    <v-row justify="center">
      <v-flex
        ma-3
        lg9
      >
    <v-layout column>
      <v-card>
        <v-card-text>
            <v-text-field
                v-model="form.firstName"
                label="Pfadfindername"></v-text-field>
            <v-text-field
                v-model="form.contactEmail"
                label="Email Address">
              </v-text-field>
            <v-select
                v-model="form.contactEmail"
                label="Stamm">
            </v-select>
        </v-card-text>

        <v-card-actions>
            <v-btn color="success">
                <v-icon left dark>mdi-check</v-icon>
                Änderungen speichern
            </v-btn>
            <v-btn dark color="red">
                <v-icon left>mdi-delete</v-icon>
                Account Daten löschen
            </v-btn>
        </v-card-actions>
      </v-card>
    </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      form: {
        firstName: 'John',
        lastName: 'Doe',
        contactEmail: 'john@doe.com',
        avatar: 'MALE_CAUCASIAN_BLOND_BEARD',
      },
      showAvatarPicker: false,
    };
  },
};
</script>
