/*
import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { Console } from 'console';

dotenv.config(); // Cargar las variables de entorno

const email = "adriaannm.rodriguezr@uqvirtual.edu.co";
const password = "cc1006054380";

// Obtener la ruta actual en ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Crear la carpeta para las descargas
const folderName = `ArchivosSage`;
const downloadFolder = path.join(__dirname, folderName);

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
        downloadPath: downloadFolder, 
    });

    console.log("Download folder set to: " + downloadFolder);

    await page.goto("https://journals-sagepub-com.crai.referencistas.com/", { waitUntil: 'networkidle2' });

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
    await page.waitForSelector('#AllField35ea26a9-ec16-4bde-9652-17b798d5b6750', { visible: true });
    await page.type('#AllField35ea26a9-ec16-4bde-9652-17b798d5b6750', '"computational thinking"');
    
    await page.keyboard.press('Enter');
    await delay(10000);

    const resultsSelector = 'span.result__count';
    await page.waitForSelector(resultsSelector, { visible: true });
    const resultsText = await page.$eval(resultsSelector, el => el.textContent.trim());
    const totalResultsCount = parseInt(resultsText.replace(/,/g, ''), 10);

    console.log(`Total results: ${totalResultsCount}`);

    const itemsPerPage = 10;
    const totalPages = Math.ceil(totalResultsCount / itemsPerPage);
    console.log(`Total pages: ${totalPages}`);

    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
        console.log(`Processing page ${pageNum}...`);
        
        await page.waitForSelector('#action-bar-select-all', { visible: true });
        await page.click('#action-bar-select-all');
        await delay(1000);

        const exportSelector = 'a[data-id="srp-export-citations"]';
        await page.waitForSelector(exportSelector, { visible: true });
        await page.click(exportSelector);

        await page.waitForSelector('#citation-format', { visible: true });
        await page.select('#citation-format', 'bibtex');
        await delay(2000);

        await page.waitForSelector('a[href^="data:Application/x-bibtex"]');
        await page.click('a[href^="data:Application/x-bibtex"]');
        
        // Esperar a que se descargue el archivo y luego renombrarlo
        await delay(5000); 
        renameLatestDownload(downloadFolder, `results_page_${pageNum}.bib`);

        console.log(`Page ${pageNum} results downloaded.`);
        
        const nextPageUrl = `https://journals-sagepub-com.crai.referencistas.com/action/doSearch?AllField=computational+thinking&startPage=${pageNum + 1}&pageSize=10`;
        await page.goto(nextPageUrl);
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

import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { Console } from 'console';

dotenv.config(); // Cargar las variables de entorno

const email = "adriaannm.rodriguezr@uqvirtual.edu.co";
const password = "cc1006054380";

// Obtener la ruta actual en ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Crear la carpeta para las descargas
const folderName = `ArchivosSage`;
const downloadFolder = path.join(__dirname, folderName);

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
        downloadPath: downloadFolder,
    });

    console.log("Download folder set to: " + downloadFolder);

    await page.goto("https://journals-sagepub-com.crai.referencistas.com/", { waitUntil: 'networkidle2' });

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
    await page.waitForSelector('#AllField35ea26a9-ec16-4bde-9652-17b798d5b6750', { visible: true, timeout: 60000 });
    await page.type('#AllField35ea26a9-ec16-4bde-9652-17b798d5b6750', '"computational thinking"');
    
    await page.keyboard.press('Enter');
    await page.waitForNavigation({ waitUntil: 'networkidle2' });

    const resultsSelector = 'span.result__count';
    await page.waitForSelector(resultsSelector, { visible: true, timeout: 60000 });
    const resultsText = await page.$eval(resultsSelector, el => el.textContent.trim());
    const totalResultsCount = parseInt(resultsText.replace(/,/g, ''), 10);

    console.log(`Total results: ${totalResultsCount}`);

    const itemsPerPage = 10;
    const totalPages = Math.ceil(totalResultsCount / itemsPerPage);
    console.log(`Total pages: ${totalPages}`);

    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
        console.log(`Processing page ${pageNum}...`);
        
        await page.waitForSelector('#action-bar-select-all', { visible: true, timeout: 60000 });
        await page.click('#action-bar-select-all');
        await delay(1000);

        const exportSelector = 'a[data-id="srp-export-citations"]';
        await page.waitForSelector(exportSelector, { visible: true, timeout: 60000 });
        await page.click(exportSelector);

        await page.waitForSelector('#citation-format', { visible: true, timeout: 60000 });
        await page.select('#citation-format', 'bibtex');
        await delay(2000);

        await page.waitForSelector('a[href^="data:Application/x-bibtex"]', { visible: true, timeout: 60000 });
        await page.click('a[href^="data:Application/x-bibtex"]');
        
        // Esperar a que se descargue el archivo y luego renombrarlo
        await delay(5000); 
        renameLatestDownload(downloadFolder, `results_page_${pageNum}.bib`);

        console.log(`Page ${pageNum} results downloaded.`);
        
        const nextPageUrl = `https://journals-sagepub-com.crai.referencistas.com/action/doSearch?AllField=computational+thinking&startPage=${pageNum + 1}&pageSize=10`;
        await page.goto(nextPageUrl, { waitUntil: 'networkidle2' });
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
