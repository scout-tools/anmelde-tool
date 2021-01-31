// const forge = require("node-forge");

// console.log('Hallo');

let messageBase64 = 'SrUInuM6rTlKEtYpxZRxZHdJ2qK540jdQqUvhXPiZMgvfQRnO/T/xztexpVuSY3Mv/dh88O8fhy36OIHtSqMHVrp+S/gPCT5jK4kbVvebo3u4Kj0gOE3T3a9wqyCMRAUrcwDpk5Ex2qIiCPQi/2+dUV1x2RZ65I4g7bxaUK/Apg3U3BB6sur9KuGW3dDn2y75LbeAMo6MMvURKAAVgBzJ2T51l1kYaGncwKBkCXvnznv7WJA54yMl0xnZbH4Mrt7O0nvJFo9VN6dCFil3GI0Ok4X9uXoMK3OqxhvTBeHvunr/IrQbbvG7+F/Pw3WjJttsvByq2XG9vSjV5ptM6swQQ=='

const privateKeyPem = '-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCNFR+3vC8f5W5GqPa3sBk37Wg1LGz/rBoNXmuCSguDCv/Azcd8\nMzFajQoma7kv3xmT7lTthDW3ZB6KU38ZC42df15Z20eQAHHTXo+H5rjV40gvFb7b\nZbgGInlRtQwqmHJBEI5AEXusQGZ3bWkGUTxpqZ+I02ugV0XGFrla4jyD7QIDAQAB\nAoGAFxRKkQMO7nfY12RSn/AF4BlNP82ZsyWTSXaVvcWhJnnJJuBC7vVs8HQ8Idbj\nf4pOo92MNSK4qtyNBnHsS8uRCeGOoT8ulyHkbhJp/5PUWxTU50tRGCIuVeC8AyN9\n0Wi5MPFh3DOecBxv5654ck5rNldbhG+fQ4DvRuke73SjOEECQQC2lCiFhszls7JY\nC2UVezzgQ+0IgdQKlTEXGVEfxhirG19Y6ZjBw+oXgNpFVcNvDC8PhQx2ZjA3pz1j\nxNjzD769AkEAxdETCa4tYCTIcL/VBpYkDRHdnTEaSPQTsxlrvLjIuhsfQxj5m9On\nokUyOGGQUwZyjyuoxhfefA7EGVNKeZsE8QJAKXIWhMEl8BrLqFrl1muEVTB2NVEr\nbj+RxjmUBc91OBpdmZRlfc7Ya/9vDQA7/hBY+n/sZVArL+cB84zy5rIzTQJAAM8W\nENgRf28nEq72JAzBIPyNt3LX9Kxq2DSmaCMpTvmFazTS8HwxF0zJI8niWTSRi1xW\nWFkIo+E7lA7vIwgrQQJBAJxBiEUFwqP+z/jODjBVDy4ddD+Cdht9/yZgNiMDeScM\nq73lWxSWDrTk6OSZtHfwQCUonaxQbkeVaBW1SK6bero=\n-----END RSA PRIVATE KEY-----'

// const publicKeyPem = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCNFR+3vC8f5W5GqPa3sBk37Wg1\nLGz/rBoNXmuCSguDCv/Azcd8MzFajQoma7kv3xmT7lTthDW3ZB6KU38ZC42df15Z\n20eQAHHTXo+H5rjV40gvFb7bZbgGInlRtQwqmHJBEI5AEXusQGZ3bWkGUTxpqZ+I\n02ugV0XGFrla4jyD7QIDAQAB\n-----END PUBLIC KEY-----'

// const priv = forge.pki.privateKeyFromPem(privateKeyPem);

// const pub = forge.pki.publicKeyFromPem(publicKeyPem)

// const messageByte = pub.encrypt("Hello World!");



// // messageBase64 = forge.util.encode64(messageByte)

// //
// console.log(messageBase64)
// // 


// const encrypted = forge.util.decode64(messageBase64)

// console.log(encrypted)
// const decrypted = priv.decrypt(encrypted);

// console.log("decrypted(by PEM):", decrypted);

const NodeRSA = require('node-rsa');
const key = new NodeRSA(privateKeyPem);
 
console.log(key.getMaxMessageSize())
console.log(key.isPrivate())
console.log(key.getKeySize())

const decrypted = key.decrypt(messageBase64, 'utf8', 'base64');
console.log('decrypted: ', decrypted);