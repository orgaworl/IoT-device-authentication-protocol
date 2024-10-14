const { BrowserWindow, getCurrentWindow, dialog } = require("@electron/remote");
const fs = require("fs");
const path = require("path");

let mainWindow = getCurrentWindow();

// 监视提交表单事件
const configButton = document.querySelector("#config");
configButton.addEventListener("submit", function (event) {
    event.preventDefault(); // stop the form from submitting
    let host = document.getElementById("config-host").value;
    if(host== ""){host="127.0.0.1";}
    let port = document.getElementById("config-port").value;
    if(port== ""){port="4398";}
    let passwd= document.getElementById("config-passwd").value;
    if(passwd== ""){passwd="passwd";}
    //require("child_process").spawn("C:\\Program Files\\010 Editor.exe");
    var python = require("child_process").spawn("python", [
        path.join(__dirname, "/../../Kelapa/src/progClient.py"),
        "--ip="+host,
        "--port="+port,
        "--passwd="+passwd,
    ]);
    python.stdout.on("data", function (data) {
        let display_window=document.getElementById("display-window");
        var contentPart = document.createElement("<p>");
        contentPart.innerHTML = data.toString("utf8");
        display_window.appendChild(contentPart);
    });

    python.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
    });

    python.on("close", (code) => {
        console.log(`child process exited with code ${code}`);
    });
});

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
});
