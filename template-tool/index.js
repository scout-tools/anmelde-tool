import { readdir, readFile, writeFile } from 'fs';
import mjml2html from 'mjml';
import { htmlToText } from 'html-to-text';
import path from 'path';

// const ary = ['mosaik_payment_reminder'];
// const path = `input/${ary[0]}.mjml`

const inputPath = './input';

readdir(inputPath, 'utf8', (err, files) => {
  if (err) {
    console.error(err);
    return;
  }

  files.forEach(file => {
    if (path.extname(file).endsWith('.mjml')) {

      let filename = path.join(inputPath, file);

      readFile(filename, 'utf8', (err, data) => {
        if (err) {
          console.error(err);
          return;
        }

        const htmlOutput = mjml2html(data);

        const plainText = htmlToText(htmlOutput.html, {
          wordwrap: 200
        });

        let pureName = path.parse(file).name
        const outputPathHtml = `output/${pureName}.html`;
        const outputPathTex = `output/${pureName}.txt`;

        writeFile(outputPathHtml, htmlOutput.html, (err) => {
          if (err) return console.log(err);
        });

        writeFile(outputPathTex, plainText, (err) => {
          if (err) return console.log(err);
        });
      });
    }
  });
});
