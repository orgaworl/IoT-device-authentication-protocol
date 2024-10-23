const { BrowserWindow, getCurrentWindow } = require("@electron/remote");
const path = require("path");
const { ipcRenderer } = require("electron");

let mainWindow = getCurrentWindow();

// 点击事件
window.addEventListener("DOMContentLoaded", () => {
  // 菜单栏操作
  const option_minimize = document.getElementById("option-minimize");
  option_minimize.addEventListener("click", () => {
    mainWindow.minimize();
  });

  const option_maximize = document.getElementById("option-maximize");
  option_maximize.addEventListener("click", () => {
    if (!mainWindow.isMaximized()) {
      mainWindow.maximize();
    } else {
      mainWindow.restore();
    }
  });

  const option_close = document.getElementById("option-close");
  option_close.addEventListener("click", () => {
    console.log("option-close");
    mainWindow.close();
  });

  // 选择程序类型
  const selectServer = document.getElementsByClassName("select-button")[0];
  selectServer.addEventListener("click", () => {
    ipcRenderer.send("startup server app");
  });
  const selectClient = document.getElementsByClassName("select-button")[1];
  selectClient.addEventListener("click", () => {
    // 发送请求
    ipcRenderer.send("startup client app");
  });
});
