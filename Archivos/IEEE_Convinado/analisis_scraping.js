const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

// __filename y __dirname ya están disponibles en CommonJS, no es necesario declararlos
// Crear una carpeta dinámica con la fecha actual en la raíz del proyecto
const date = new Date();
const folderName = `ArchivosIEEE_${date.getFullYear()}_${date.getMonth() + 1}_${date.getDate()}_${date.getHours()}_${date.getMinutes()}_${date.getSeconds()}`;
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

    await page.goto("https://ieeexplore-ieee-org.crai.referencistas.com/Xplore/home.jsp");

    // Iniciar sesión (manteniendo tu flujo existente)
    await page.click('#btn-google');
    await delay(4000);
    await page.type('::-p-xpath(//*[@id="identifierId"])', "adriaannm.rodriguezr@uqvirtual.edu.co"); // Tu correo electrónico
    await page.click('::-p-xpath(//*[@id="identifierNext"]/div/button/span)');
    await delay(2000);
    await page.type('::-p-xpath(//*[@id="password"]/div[1]/div/div[1]/input)', "cc1006054380"); // Tu contraseña
    await page.click('::-p-xpath(//*[@id="passwordNext"]/div/button/span)');
    await delay(20000);

    // Hacer la búsqueda
    await delay(2000);
    await page.waitForSelector('input.Typeahead-input');
    await page.type('input.Typeahead-input', '"computational thinking"');
    await page.keyboard.press('Enter');
    await delay(10000);
    await page.click('#dropdownPerPageLabel');
    await page.waitForSelector('div[ngbdropdownmenu]');
    await page.click('button.dropdown-item.filter-popover-option:nth-child(5)');
    await page.waitForSelector('.results-actions-selectall-checkbox');

    // Obtener el número total de resultados
    const totalResults = await page.evaluate(() => {
        const totalResultsText = document.querySelector('span.strong:nth-of-type(2)').innerText;
        return parseInt(totalResultsText.replace(/,/g, '')); // Elimina las comas y convierte a número
    });

    const itemsPerPage = 100;
    const totalPages = Math.ceil(totalResults / itemsPerPage);
    console.log(`Total pages: ${totalPages}`);

    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
        console.log(`Processing page ${pageNum}...`);

        // Seleccionar todos los resultados en la página actual
        await page.waitForSelector('.results-actions-selectall-checkbox');
        await page.click('.results-actions-selectall-checkbox');
        await delay(1000);

        // Hacer clic en el botón de exportar
        await page.waitForSelector('li.myproject-export button.xpl-toggle-btn');
        await page.click('li.myproject-export button.xpl-toggle-btn');

        // Descargar los resultados
        await page.waitForSelector('button.stats-SearchResults_Download');
        await page.click('button.stats-SearchResults_Download');
        await delay(10000); // Esperar para que la descarga finalice

        console.log(`Page ${pageNum} results downloaded.`);

        if (pageNum < totalPages) {
            let pageAux = pageNum + 1;
            let element = `button.stats-Pagination_arrow_next_${pageAux}`;
            await page.waitForSelector(element);
            await page.click(element);
        }
    }

    console.log("Downloads should be in: " + downloadFolder);
    await browser.close();
}

function delay(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time);
    });
}

openWebPage();
