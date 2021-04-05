<template>
  <div>
    <h1 style="margin-top: 80px; margin-left: 40px">PDF generieren</h1>
    <vue-html2pdf
      :show-layout="controlValue.showLayout"
      :float-layout="controlValue.floatLayout"
      :enable-download="controlValue.enableDownload"
      :preview-modal="controlValue.previewModal"
      :filename="controlValue.filename"
      :paginate-elements-by-height="controlValue.paginateElementsByHeight"
      :pdf-quality="controlValue.pdfQuality"
      :pdf-format="controlValue.pdfFormat"
      :pdf-orientation="controlValue.pdfOrientation"
      :pdf-content-width="controlValue.pdfContentWidth"
      :manual-pagination="controlValue.manualPagination"
      :html-to-pdf-options="htmlToPdfOptions"
      ref="html2Pdf"
    >
      <pdf-content slot="pdf-content" />
    </vue-html2pdf>
    <v-btn @click="$refs.html2Pdf.generatePdf()">generate</v-btn>
  </div>
</template>

<script>
import pdfContent from '@/views/pdfGeneration/PdfContent.vue';

export default {
  name: 'pdfGeneration',
  components: { pdfContent },
  data: () => ({
    controlValue: {
      showLayout: false,
      floatLayout: true,
      enableDownload: true,
      previewModal: true,
      paginateElementsByHeight: 1100,
      manualPagination: true,
      filename: 'Hee Hee',
      pdfQuality: 2,
      pdfFormat: 'a4',
      pdfOrientation: 'portrait',
      pdfContentWidth: '800px',
    },
  }),
  computed: {
    htmlToPdfOptions() {
      return {
        margin: 0,

        filename: 'hee hee.pdf',

        image: {
          type: 'jpeg',
          quality: 0.98,
        },

        enableLinks: true,

        html2canvas: {
          scale: this.controlValue.pdfQuality,
          useCORS: true,
        },

        jsPDF: {
          unit: 'in',
          format: this.controlValue.pdfFormat,
          orientation: this.controlValue.pdfOrientation,
        },
      };
    },
  },
};
</script>
