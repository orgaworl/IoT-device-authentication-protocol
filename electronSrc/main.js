// Modules to control application life and create native browser window
const { app, BrowserWindow } = require("electron");
const path = require("node:path");

function createMainWindow() {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    title: "Disk Space Visualizer",
    icon: "/img/icon/logo.ico",
    autoHideMenuBar: true,
    frame:false,
    x: 0,
    y: 0,
    width: 2000,
    minWidth: 800,
    height: 800,
    show: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, "src/preload.js"),
    },
  });

  //
  require("@electron/remote/main").initialize();
  require("@electron/remote/main").enable(mainWindow.webContents);

  //
  mainWindow.loadFile("src/index.html");
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });

}


app.whenReady().then(() => {
  createMainWindow();
  app.on("activate", function () {

    if (BrowserWindow.getAllWindows().length === 0) 
      createMainWindow();
  });
});
