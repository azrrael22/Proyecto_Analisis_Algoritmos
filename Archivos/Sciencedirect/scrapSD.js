/*
import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config(); // Esto cargará las variables de tu archivo .env
const email = "adriaannm.rodriguezr@uqvirtual.edu.co";
const password = "cc1006054380";

// Obtener la ruta actual en ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Crear una carpeta dinámica con la fecha actual en la raíz del proyecto
const date = new Date();
const folderName = `ArchivosScienceDirect`;
const downloadFolder = path.join(__dirname, folderName); // La carpeta dinámica estará en la raíz

// Asegúrate de que el directorio de descargas existe
if (!fs.existsSync(downloadFolder)) {
    fs.mkdirSync(downloadFolder, { recursive: true });
}

async function openWebPage() {
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 100,
    });

    const page = await browser.newPage();

    // Configurar la carpeta de descargas
    const client = await page.createCDPSession(); // Nueva forma de crear la sesión CDP
    await client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: downloadFolder, // Especifica la carpeta en la raíz
    });

    console.log("Download folder set to: " + downloadFolder);

    await page.goto("https://www-sciencedirect-com.crai.referencistas.com");

    // Iniciar sesión (manteniendo tu flujo existente)
    await page.click('#btn-google');
    await delay(4000);
    await page.type('::-p-xpath(//*[@id="identifierId"])', email);
    await page.click('::-p-xpath(//*[@id="identifierNext"]/div/button/span)');
    await delay(2000);
    await page.type('::-p-xpath(//*[@id="password"]/div[1]/div/div[1]/input)', password);
    await page.click('::-p-xpath(//*[@id="passwordNext"]/div/button/span)');
    
    await delay(20000);

    // Hacer la búsqueda
    await delay(2000);
    await page.waitForSelector('#qs');
    await page.type('#qs', '"computational thinking"');

    await page.keyboard.press('Enter');
    await delay(10000);
    //seleccionar 100 elementos por pagina
    await page.waitForSelector('a[data-aa-name="srp-100-results-per-page"]');
    await page.click('a[data-aa-name="srp-100-results-per-page"]');
    

   // Esperar a que el elemento esté presente en la página
    await page.waitForSelector('div.ResultsFound .search-body-results-text');

    // Extraer el texto y procesarlo para obtener el número
    const totalResults = await page.evaluate(() => {
    const resultsText = document.querySelector('div.ResultsFound .search-body-results-text').innerText;
    return parseInt(resultsText.replace(/,/g, '').match(/\d+/)[0]); // Elimina las comas y extrae el número
    });

    console.log(`Total results: ${totalResults}`);


    const itemsPerPage = 100;
    const totalPages = Math.ceil(totalResults / itemsPerPage);
    console.log(`Total pages: ${totalPages}`);

    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
        console.log(`Processing page ${pageNum}...`);

        // seleccionar todos los elementos
        await page.waitForSelector('#select-all-results');
        await page.click('#select-all-results');
    
        await delay(1000);

        // Hacer clic en el botón de exportar
        await page.waitForSelector('.export-all-link-text');
        await page.click('.export-all-link-text');


        // Descargar los resultados
        await page.waitForSelector('button[data-aa-button="srp-export-multi-bibtex"]');
        await page.click('button[data-aa-button="srp-export-multi-bibtex"]');

        await delay(10000); // Esperar para que la descarga finalice

        console.log(`Page ${pageNum} results downloaded.`);

        if (pageNum < totalPages) {
            let pageAux = pageNum + 1;
            let element = `a[data-aa-name="srp-next-page"]`;
            await page.waitForSelector(element);
            await page.click(element);
            await delay(3000);
        }
    }

    console.log("Downloads should be in: " + downloadFolder);
    await browser.close();
}

function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
}

openWebPage();
*/

import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config(); // Cargar las variables del archivo .env
const email = "adriaannm.rodriguezr@uqvirtual.edu.co";
const password = "cc1006054380";

// Obtener la ruta actual en ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Crear una carpeta dinámica con la fecha actual en la raíz del proyecto
const date = new Date();
const folderName = `ArchivosScienceDirect`;
const downloadFolder = path.join(__dirname, folderName);

// Asegurarse de que el directorio de descargas exista
if (!fs.existsSync(downloadFolder)) {
    fs.mkdirSync(downloadFolder, { recursive: true });
}

async function openWebPage() {
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 100,
        defaultViewport: null,  // Para evitar problemas de tamaño de ventana
    });

    const page = await browser.newPage();
    page.setDefaultTimeout(60000);  // Aumentar el tiempo de espera predeterminado

    // Configurar la carpeta de descargas
    const client = await page.createCDPSession();
    await client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: downloadFolder,
    });

    console.log("Download folder set to: " + downloadFolder);

    await page.goto("https://www-sciencedirect-com.crai.referencistas.com", { waitUntil: 'networkidle2' });

    // Iniciar sesión
    await page.click('#btn-google');
    await delay(4000);
    await page.type('::-p-xpath(//*[@id="identifierId"])', email);
    await page.click('::-p-xpath(//*[@id="identifierNext"]/div/button/span)');
    await delay(2000);
    await page.type('::-p-xpath(//*[@id="password"]/div[1]/div/div[1]/input)', password);
    await page.click('::-p-xpath(//*[@id="passwordNext"]/div/button/span)');
    
    await delay(20000);

    // Realizar la búsqueda
    await delay(2000);
    await page.waitForSelector('#qs', { timeout: 60000 });  // Aumentar el tiempo de espera
    await page.type('#qs', '"computational thinking"');

    await page.keyboard.press('Enter');
    await page.waitForNavigation({ waitUntil: 'networkidle2' });

    // Seleccionar 100 resultados por página
    await page.waitForSelector('a[data-aa-name="srp-100-results-per-page"]', { timeout: 60000 });
    await page.click('a[data-aa-name="srp-100-results-per-page"]');
    
    await page.waitForSelector('div.ResultsFound .search-body-results-text', { timeout: 60000 });

    // Obtener el número total de resultados
    const totalResults = await page.evaluate(() => {
        const resultsText = document.querySelector('div.ResultsFound .search-body-results-text').innerText;
        return parseInt(resultsText.replace(/,/g, '').match(/\d+/)[0]);
    });

    console.log(`Total results: ${totalResults}`);

    const itemsPerPage = 100;
    const totalPages = Math.ceil(totalResults / itemsPerPage);
    console.log(`Total pages: ${totalPages}`);

    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
        console.log(`Processing page ${pageNum}...`);

        // Seleccionar todos los resultados
        await page.waitForSelector('#select-all-results', { timeout: 60000 });
        await page.click('#select-all-results');
        await delay(1000);

        // Hacer clic en el botón de exportar
        await page.waitForSelector('.export-all-link-text', { timeout: 60000 });
        await page.click('.export-all-link-text');

        // Descargar los resultados
        await page.waitForSelector('button[data-aa-button="srp-export-multi-bibtex"]', { timeout: 60000 });
        await page.click('button[data-aa-button="srp-export-multi-bibtex"]');

        await delay(10000); // Esperar para que la descarga finalice

        console.log(`Page ${pageNum} results downloaded.`);

        if (pageNum < totalPages) {
            let pageAux = pageNum + 1;
            let element = `a[data-aa-name="srp-next-page"]`;
            await page.waitForSelector(element, { timeout: 60000 });
            await page.click(element);
            await delay(3000);
        }
    }

    console.log("Downloads should be in: " + downloadFolder);
    await browser.close();
}

function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
}

openWebPage();
