// Modules to control application life and create native browser window
const { app, BrowserWindow } = require("electron");
const path = require("node:path");
const { ipcMain } = require("electron");

function createStartupWindow() {
  const mainWindow = new BrowserWindow({
    autoHideMenuBar: true,
    frame: false,
    x: 200,
    y: 150,
    width: 500,
    minWidth: 500,
    height: 400,
    show: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  //
  require("@electron/remote/main").initialize();
  require("@electron/remote/main").enable(mainWindow.webContents);

  //
  mainWindow.loadFile(path.join(__dirname, "startup.html"));
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });
}

function createClientWindow() {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    autoHideMenuBar: true,
    frame: false,
    x: 250,
    y: 200,
    width: 1200,
    minWidth: 800,
    height: 800,
    show: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  //
  //require("@electron/remote/main").initialize();
  require("@electron/remote/main").enable(mainWindow.webContents);
  mainWindow.loadFile(path.join(__dirname, "app-client.html"));
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });
}

function createServerWindow() {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    autoHideMenuBar: true,
    frame: false,
    x: 300,
    y: 250,
    width: 1000,
    minWidth: 900,
    height: 520,
    minHeight: 520,
    show: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  //
  //require("@electron/remote/main").initialize();
  require("@electron/remote/main").enable(mainWindow.webContents);
  mainWindow.loadFile(path.join(__dirname, "app-server.html"));
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });
}

app.whenReady().then(() => {
  //createMainWindow();
  createStartupWindow();
  app.on("activate", function () {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

// 监控client窗口开启
ipcMain.on("startup client app", (event, arg) => {
  createClientWindow();
});
ipcMain.on("startup server app", (event, arg) => {
  createServerWindow();
});
