<template>
  <v-data-table
    :headers="headers"
    :items="examples"
    :items-per-page="5"
    class="elevation-1"
  ></v-data-table>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {
          text: 'Fahrt/Lager',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        { text: 'Beschreibung', value: 'description' },
        { text: 'Actions', value: 'fat' },
      ],
      examples: [
        {
          name: 'Ringfahrt',
          description: 'Dies ist eine Ringfahrt.',
        },
        {
          name: 'Ringfahrt2',
          description: 'Dies ist eine Ringfahrt2.',
        },
        {
          name: 'Ringfahrt3',
          description: 'Dies ist eine Ringfahrt3.',
        },
      ],
    };
  },
};
</script>
