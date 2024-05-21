function str2ab(str) {
    const buf = new ArrayBuffer(str.length);
    const bufView = new Uint8Array(buf);
    for (let i = 0, strLen = str.length; i < strLen; i++) {
        bufView[i] = str.charCodeAt(i);
    }
    return buf;
}

function ab2str(buf) {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
}

async function importPublicKey(spkiPem) {
    const pemHeader = "-----BEGIN PUBLIC KEY-----";
    const pemFooter = "-----END PUBLIC KEY-----";
    var pemContents = spkiPem.substring(pemHeader.length, spkiPem.length - pemFooter.length - 1);
    var binaryDerString = window.atob(pemContents);
    spkiPem = str2ab(binaryDerString);

    return await window.crypto.subtle.importKey(
        "spki",
        spkiPem,
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["encrypt"]
    );
}

async function importPrivateKey(pkcs8Pem) {   
    const pemHeader = "-----BEGIN PRIVATE KEY-----";
    const pemFooter = "-----END PRIVATE KEY-----";
    var pemContents = pkcs8Pem.substring(pemHeader.length, pkcs8Pem.length - pemFooter.length - 1);
    var binaryDerString = window.atob(pemContents);
    pkcs8Pem = str2ab(binaryDerString); 

    return await window.crypto.subtle.importKey(
        "pkcs8",
        pkcs8Pem,
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["decrypt"]
    );
}

async function Encrypt(plaintext, publicKey) {
    try {
        const encrypted = await encryptRSA(publicKey, new TextEncoder().encode(plaintext));
        const encryptedBase64 = window.btoa(ab2str(encrypted));
        return encryptedBase64;
    } catch(error) {
        console.log(error);
    }
}

async function encryptRSA(key, plaintext) {
    let encrypted = await window.crypto.subtle.encrypt(
        {
            name: "RSA-OAEP"
        },
        key,
        plaintext
    );
    return encrypted;
}

async function Decrypt(ciphertextB64, privateKey) {
    try {
        const decrypted = await decryptRSA(privateKey, str2ab(window.atob(ciphertextB64)));
        return decrypted;
    } catch(error) {
        console.log(error);
    }
}

async function decryptRSA(key, ciphertext) {
    let decrypted = await window.crypto.subtle.decrypt(
        {
            name: "RSA-OAEP"
        },
        key,
        ciphertext
    );
    return new TextDecoder().decode(decrypted);
}
