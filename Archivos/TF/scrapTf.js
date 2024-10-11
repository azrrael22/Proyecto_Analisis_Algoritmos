import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config(); // Cargar las variables de entorno

const email = "adriaannm.rodriguezr@uqvirtual.edu.co";
const password = "cc1006054380";

// Obtener la ruta actual en ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Crear una carpeta dinámica con la fecha actual en la raíz del proyecto
const date = new Date();
const folderName = `ArchivosTF_${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`; // Carpeta con fecha actual
const downloadFolder = path.join(__dirname, folderName); // Especifica la carpeta en la raíz

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
    const client = await page.createCDPSession();
    await client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: downloadFolder, // Carpeta en la raíz del proyecto
    });

    console.log("Download folder set to: " + downloadFolder);

    await page.goto("https://www-tandfonline-com.crai.referencistas.com/");

    // Iniciar sesión
    await page.click('#btn-google');
    await delay(4000);
    await page.type('::-p-xpath(//*[@id="identifierId"])', email);
    await page.click('::-p-xpath(//*[@id="identifierNext"]/div/button/span)');
    await delay(2000);
    await page.type('::-p-xpath(//*[@id="password"]/div[1]/div/div[1]/input)', password);
    await page.click('::-p-xpath(//*[@id="passwordNext"]/div/button/span)');
    
    await delay(20000);

    // Hacer la búsqueda
    await page.waitForSelector('#searchText-1d85a42e-ad57-4c0d-a477-c847718bcb5d', { visible: true });
    await page.type('#searchText-1d85a42e-ad57-4c0d-a477-c847718bcb5d', '"computational thinking"');
    await page.keyboard.press('Enter');
    await delay(10000);

    // Seleccionar 50 resultados por página
    const buttonSelector = '#perPage-button';
    await page.waitForSelector(buttonSelector, { visible: true });
    await page.click(buttonSelector);

    const optionSelector = 'ul#resultsOptions li[role="option"] a[href*="pageSize=50"]';
    await page.waitForSelector(optionSelector, { visible: true });
    await page.click(optionSelector);
    await delay(10000);

    // Obtener el número total de resultados
    const resultsSelector = 'ul.num-results li.search-results p strong';
    await page.waitForSelector(resultsSelector, { visible: true });
    const resultsText = await page.$eval(resultsSelector, el => el.textContent);
    const totalResults = resultsText.match(/of ([\d,]+)/)[1].replace(/,/g, '');
    const totalResultsCount = parseInt(totalResults, 10);
    console.log(`Total results: ${totalResultsCount}`);

    const itemsPerPage = 50;
    const totalPages = Math.ceil(totalResultsCount / itemsPerPage);
    console.log(`Total pages: ${totalPages}`);

    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
        console.log(`Processing page ${pageNum}...`);

        // Seleccionar todos los resultados de la página actual
        await page.waitForSelector('input[data-behaviour="toggle-mark-all"]', { visible: true });
        await page.evaluate(() => {
            const checkbox = document.querySelector('input[data-behaviour="toggle-mark-all"]');
            if (!checkbox.checked) {
                checkbox.click(); // Marcar todos los resultados
            }
        });

        await delay(1000);

        // Descargar las citas en formato BibTeX
        await page.waitForSelector('a.download-citations', { visible: true });
        await page.evaluate(() => {
            const downloadLink = document.querySelector('a.download-citations');
            if (downloadLink) {
                downloadLink.click();
            }
        });

        await page.waitForSelector('div#download-citations-modal', { visible: true });
        await page.evaluate(() => {
            const bibtexCheckbox = document.querySelector('input[type="checkbox"][value="bibtex"]');
            if (bibtexCheckbox) {
                bibtexCheckbox.click();
            }
        });

        await page.waitForSelector('a#btn-download-citations', { visible: true });
        await page.click('a#btn-download-citations');

        await delay(10000); // Esperar que la descarga finalice
        renameLatestDownload(downloadFolder, `results_page_${pageNum}.bib`);

        console.log(`Page ${pageNum} results downloaded.`);

        // Navegar a la siguiente página
        if (pageNum < totalPages) {
            await page.waitForSelector('a.nextPage.js__ajaxSearchTrigger', { visible: true });
            await page.click('a.nextPage.js__ajaxSearchTrigger');
            await delay(10000);
        }
    }

    console.log("Downloads should be in: " + downloadFolder);
    await browser.close();
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function renameLatestDownload(downloadPath, newFileName) {
    const files = fs.readdirSync(downloadPath);
    const latestFile = files
        .map(file => ({
            file,
            time: fs.statSync(path.join(downloadPath, file)).mtime.getTime()
        }))
        .sort((a, b) => b.time - a.time)[0].file;  // Archivo más reciente

    const oldPath = path.join(downloadPath, latestFile);
    const newPath = path.join(downloadPath, newFileName);

    fs.renameSync(oldPath, newPath);
    console.log(`Renamed ${latestFile} to ${newFileName}`);
}

openWebPage();
/*

import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config(); // Cargar las variables de entorno

const email = "adriaannm.rodriguezr@uqvirtual.edu.co";
const password = "cc1006054380";

// Obtener la ruta actual en ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Crear una carpeta dinámica con la fecha actual en la raíz del proyecto
const date = new Date();
const folderName = `ArchivosTF_${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`; // Carpeta con fecha actual
const downloadFolder = path.join(__dirname, folderName); // Especifica la carpeta en la raíz

// Asegúrate de que el directorio de descargas existe
if (!fs.existsSync(downloadFolder)) {
    fs.mkdirSync(downloadFolder, { recursive: true });
}

async function openWebPage() {
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 100,
        defaultViewport: null,  // Asegura que no haya restricciones de tamaño de pantalla
    });

    const page = await browser.newPage();
    page.setDefaultTimeout(60000);  // Aumentar el tiempo de espera global a 60 segundos

    // Configurar la carpeta de descargas
    const client = await page.createCDPSession();
    await client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: downloadFolder, // Carpeta en la raíz del proyecto
    });

    console.log("Download folder set to: " + downloadFolder);

    await page.goto("https://www-tandfonline-com.crai.referencistas.com/", { waitUntil: 'networkidle2' });

    // Iniciar sesión
    await page.click('#btn-google');
    await delay(4000);
    await page.type('::-p-xpath(//*[@id="identifierId"])', email);
    await page.click('::-p-xpath(//*[@id="identifierNext"]/div/button/span)');
    await delay(2000);
    await page.type('::-p-xpath(//*[@id="password"]/div[1]/div/div[1]/input)', password);
    await page.click('::-p-xpath(//*[@id="passwordNext"]/div/button/span)');
    
    await delay(20000);

    // Hacer la búsqueda
    await page.waitForSelector('#searchText-1d85a42e-ad57-4c0d-a477-c847718bcb5d', { visible: true, timeout: 60000 });
    await page.type('#searchText-1d85a42e-ad57-4c0d-a477-c847718bcb5d', '"computational thinking"');
    await page.keyboard.press('Enter');
    await page.waitForNavigation({ waitUntil: 'networkidle2' });

    // Seleccionar 50 resultados por página
    const buttonSelector = '#perPage-button';
    await page.waitForSelector(buttonSelector, { visible: true, timeout: 60000 });
    await page.click(buttonSelector);

    const optionSelector = 'ul#resultsOptions li[role="option"] a[href*="pageSize=50"]';
    await page.waitForSelector(optionSelector, { visible: true, timeout: 60000 });
    await page.click(optionSelector);
    await delay(10000);

    // Obtener el número total de resultados
    const resultsSelector = 'ul.num-results li.search-results p strong';
    await page.waitForSelector(resultsSelector, { visible: true, timeout: 60000 });
    const resultsText = await page.$eval(resultsSelector, el => el.textContent);
    const totalResults = resultsText.match(/of ([\d,]+)/)[1].replace(/,/g, '');
    const totalResultsCount = parseInt(totalResults, 10);
    console.log(`Total results: ${totalResultsCount}`);

    const itemsPerPage = 50;
    const totalPages = Math.ceil(totalResultsCount / itemsPerPage);
    console.log(`Total pages: ${totalPages}`);

    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
        console.log(`Processing page ${pageNum}...`);

        // Seleccionar todos los resultados de la página actual
        await page.waitForSelector('input[data-behaviour="toggle-mark-all"]', { visible: true, timeout: 60000 });
        await page.evaluate(() => {
            const checkbox = document.querySelector('input[data-behaviour="toggle-mark-all"]');
            if (!checkbox.checked) {
                checkbox.click(); // Marcar todos los resultados
            }
        });

        await delay(1000);

        // Descargar las citas en formato BibTeX
        await page.waitForSelector('a.download-citations', { visible: true, timeout: 60000 });
        await page.evaluate(() => {
            const downloadLink = document.querySelector('a.download-citations');
            if (downloadLink) {
                downloadLink.click();
            }
        });

        await page.waitForSelector('div#download-citations-modal', { visible: true, timeout: 60000 });
        await page.evaluate(() => {
            const bibtexCheckbox = document.querySelector('input[type="checkbox"][value="bibtex"]');
            if (bibtexCheckbox) {
                bibtexCheckbox.click();
            }
        });

        await page.waitForSelector('a#btn-download-citations', { visible: true, timeout: 60000 });
        await page.click('a#btn-download-citations');

        await delay(10000); // Esperar que la descarga finalice
        renameLatestDownload(downloadFolder, `results_page_${pageNum}.bib`);

        console.log(`Page ${pageNum} results downloaded.`);

        // Navegar a la siguiente página
        if (pageNum < totalPages) {
            await page.waitForSelector('a.nextPage.js__ajaxSearchTrigger', { visible: true, timeout: 60000 });
            await page.click('a.nextPage.js__ajaxSearchTrigger');
            await delay(10000);
        }
    }

    console.log("Downloads should be in: " + downloadFolder);
    await browser.close();
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function renameLatestDownload(downloadPath, newFileName) {
    const files = fs.readdirSync(downloadPath);
    const latestFile = files
        .map(file => ({
            file,
            time: fs.statSync(path.join(downloadPath, file)).mtime.getTime()
        }))
        .sort((a, b) => b.time - a.time)[0].file;  // Archivo más reciente

    const oldPath = path.join(downloadPath, latestFile);
    const newPath = path.join(downloadPath, newFileName);

    fs.renameSync(oldPath, newPath);
    console.log(`Renamed ${latestFile} to ${newFileName}`);
}

openWebPage();
*/
