import { readFile, writeFile } from 'fs';
import mjml2html from 'mjml';
import { htmlToText } from 'html-to-text';

const ary =  ['matching']

const path = `input/${ary[0]}.mjml`

readFile(path, 'utf8', (err, data) => {
  if (err) {
    console.error(err)
    return
  }

  const htmlOutput = mjml2html(data)

  const plainText = htmlToText(htmlOutput.html, {
    wordwrap: 200
  });

  const outputPathHtml = `output/${ary[0]}.html`

  writeFile(outputPathHtml, htmlOutput.html, (err) => {
    if (err) return console.log(err);
  });

  const outputPathTex = `output/${ary[0]}.txt`

  writeFile(outputPathTex, plainText, (err) => {
    if (err) return console.log(err);
  });
})
